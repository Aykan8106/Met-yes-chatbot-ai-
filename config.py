import os
from dotenv import load_dotenv

# .env dosyasını okur; bunu çağırmazsak os.environ.get() .env'deki değerleri göremez
load_dotenv()


class Config:
    """Geliştirme ve üretim için ortak ayarlar."""

    # Flask oturum güvenliği için gizli anahtar
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gelistirme-icin-gecici-anahtar')

    # SQLite dosya adı
    DATABASE_URL = os.environ.get('DATABASE_URL', 'leads.db')

    # Yapay zekâ ayarları
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')

    # Hangi sitelerin API'ye erişebileceği (Wix için sonra daraltacağız)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    DEBUG = False

    # Yapay zekânın kişiliği — burası projeye özel tek yerdir
    BUSINESS_CONTEXT = """Sen MetYes'in yapay zeka asistanisin. MetYes, guvenlik
sistemleri alaninda hizmet veren bir isletmedir (kamera sistemleri, alarm
sistemleri, erisim kontrolu). Ziyaretcilerin guvenlik sistemleri hakkindaki
sorularini kibar, guven veren ve sade bir dille yanitla. Turkce konus.
Bilmedigin bir konuda tahmin yurutme; uzman ekibimizin donecegini soyle.
Musteriyi ucretsiz kesif/danismanlik icin isim ve telefon birakmaya nazikce yonlendir."""


class DevelopmentConfig(Config):
    """Yerel geliştirme: hata ayıklama açık."""
    DEBUG = True


class ProductionConfig(Config):
    """Render (canlı ortam): hata ayıklama kapalı."""
    DEBUG = False


# create_app() bu sözlükle doğru ayarı seçecek
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}