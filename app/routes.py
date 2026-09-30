# app/routes.py - HTTP isteklerini karsilar, dogrular, dogru katmana yonlendirir.
# Bu dosyada SQL veya dogrudan AI API kodu OLMAZ; sadece katman fonksiyonlari cagrilir.
from flask import Blueprint, jsonify, render_template, request

from app import database
from app.services.ai_service import ai_service, AIServiceError

# Sayfalar icin blueprint (/ ve /dashboard)
pages_bp = Blueprint('pages', __name__)

# API icin blueprint (create_app icinde url_prefix='/api' verilecek)
api_bp = Blueprint('api', __name__)


# ---------------------------------------------------------------- SAYFALAR

@pages_bp.route('/')
def ana_sayfa():
    """Karsilama sayfasi."""
    return render_template('index.html')


@pages_bp.route('/dashboard')
def dashboard():
    """Yonetim paneli."""
    return render_template('dashboard.html')


# ---------------------------------------------------------------- API

def _hata(mesaj, kod):
    """Tum hata yanitlari ayni bicimde donsun diye tek yardimci."""
    return jsonify({"basari": False, "hata": mesaj}), kod


@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    """Ziyaretcinin mesajini yapay zekaya iletir."""
    veri = request.get_json(silent=True) or {}
    mesaj = str(veri.get('mesaj', '')).strip()
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return _hata("Mesaj bos olamaz.", 400)
    if len(mesaj) > 1000:
        return _hata("Mesaj cok uzun (en fazla 1000 karakter).", 400)
    if not isinstance(gecmis, list):
        gecmis = []

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": cevap}), 200
    except AIServiceError:
        # Teknik ayrintiyi kullaniciya gostermiyoruz (guvenlik)
        return _hata("Asistan su an yanit veremiyor, lutfen biraz sonra tekrar deneyin.", 503)


@api_bp.route('/leads', methods=['POST'])
def lead_kaydet():
    """Yeni musteri adayi kaydeder."""
    veri = request.get_json(silent=True) or {}
    isim = str(veri.get('isim', '')).strip()
    telefon = str(veri.get('telefon', '')).strip()
    mesaj = str(veri.get('mesaj', '')).strip()

    if not isim or not telefon:
        return _hata("Isim ve telefon zorunludur.", 400)
    if len(isim) > 100 or len(telefon) > 30 or len(mesaj) > 1000:
        return _hata("Girilen bilgiler cok uzun.", 400)

    try:
        yeni_id = database.lead_ekle(isim, telefon, mesaj)
        return jsonify({"basari": True, "id": yeni_id}), 201
    except Exception:
        return _hata("Kayit su an yapilamadi, lutfen tekrar deneyin.", 500)


@api_bp.route('/leads', methods=['GET'])
def lead_listele():
    """Tum kayitlari getirir."""
    try:
        kayitlar = database.tum_leadler()
        # Wix Repeater her objede _id ister; ayni kayitlara _id ekliyoruz
        for kayit in kayitlar:
            kayit['_id'] = str(kayit['id'])
        return jsonify({"basari": True, "leadler": kayitlar}), 200
    except Exception:
        return _hata("Kayitlar su an getirilemedi.", 500)
