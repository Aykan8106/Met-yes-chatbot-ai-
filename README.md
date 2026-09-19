[README.md](https://github.com/user-attachments/files/32416794/README.md)
# Metæyes AI

Güvenlik sistemleri sektöründe, ziyaretçilerle yapay zekâ destekli bir sohbet asistanı üzerinden iletişime geçen ve iletişim bilgilerini (lead) toplayan bir sistem. Proje, Python/Flask backend, SQLite veritabanı, Groq yapay zekâ API'si ve Wix Velo frontend katmanlarından oluşacak şekilde tasarlanmıştır.

## Kullanılan Teknolojiler

- **Backend:** Python, Flask
- **Veritabanı:** SQLite
- **Yapay Zekâ:** Groq API
- **Frontend:** Wix Velo
- **Barındırma:** Render (backend), Wix (frontend)
- **Sürüm kontrolü:** Git / GitHub

## Mimari Yaklaşım

Proje, *Separation of Concerns* (Sorumlulukların Ayrılığı) ilkesine göre katmanlı bir yapıda kurulmaktadır:

```
metyes_ai/
├── run.py              → Sunucuyu başlatan giriş noktası
├── config.py            → Tüm ayarlar ve anahtarlar (.env okur)
├── requirements.txt      → Bağımlılık listesi
├── .env                 → Gizli anahtarlar (Git'e eklenmez)
├── .gitignore
└── app/
    ├── __init__.py        → Uygulama fabrikası (create_app)
    ├── database.py        → Veritabanı işlemleri
    ├── routes.py          → HTTP rotaları
    ├── templates/         → HTML sayfaları
    └── services/
        └── ai_service.py  → Yapay zekâ API çağrıları
```

Her katmanın tek bir sorumluluğu vardır: veritabanı işlemleri yalnızca `database.py` içinde, yapay zekâ çağrıları yalnızca `ai_service.py` içinde, rotalar ise sadece bu katmanları çağırıp yönlendirme yapar.

## Şimdiye Kadar Tamamlananlar

- [x] Geliştirme ortamı kuruldu (Python, VS Code, Git)
- [x] Gerekli hesaplar oluşturuldu (GitHub, Render, Wix, Groq)
- [x] Groq API anahtarı alındı
- [x] Proje klasör iskeleti, hedef mimariye uygun şekilde oluşturuldu
- [x] Sanal ortam (venv) kuruldu ve temel bağımlılıklar (`flask`, `flask-cors`, `python-dotenv`, `requests`, `gunicorn`) yüklendi
- [x] Yerel ortamda Flask ile bir "duman testi" (smoke test) yapılarak ortamın çalıştığı doğrulandı
- [x] GitHub deposu oluşturuldu ve proje iskeleti `.env` ve `venv/` dosyaları hariç tutularak (`.gitignore` ile) push edildi
- [x] Render üzerinde bir Web Service oluşturulup GitHub deposuna bağlandı
- [x] Basit bir Flask uygulaması (`run.py`) Render'a başarıyla deploy edilerek canlı bir mesaj yayınlandı — GitHub → Render otomatik dağıtım hattının (CI/CD) çalıştığı doğrulandı

## Sırada Ne Var

Backend'in gerçek katmanlarının (yapılandırma, veritabanı, yapay zekâ servisi, rotalar, uygulama fabrikası) yazılması, ardından Wix Velo frontend'inin bu backend'e bağlanması.

## Kurulum (Yerel Geliştirme)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python run.py
```

## Canlı Adres

Backend, Render üzerinde barındırılmaktadır: `https://<render-servis-adresin>.onrender.com`
