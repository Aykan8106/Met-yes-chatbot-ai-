# app/__init__.py - Uygulama fabrikasi: tum parcalari bir araya getirir.
import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import config


def create_app(config_name=None):
    """Sirasiyla: ayarlari yukle -> CORS ac -> veritabani -> blueprint'ler."""
    # Hangi ayarin kullanilacagi: APP_ENV=production ise canli ayarlar
    config_name = config_name or os.environ.get('APP_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # CORS: Wix sitesinin API'ye erisebilmesi icin. Sadece /api/* acik.
    izinli = app.config['CORS_ORIGINS']
    origins = '*' if izinli == '*' else [o.strip() for o in izinli.split(',')]
    CORS(app, resources={r"/api/*": {"origins": origins}})

    # Bu importlar fonksiyon icinde: dongusel import sorununu onler
    from app.database import init_db
    from app.routes import api_bp, pages_bp

    init_db(app)  # leads tablosu yoksa olusturur

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health')
    def health():
        """Sunucu canlilik kontrolu (Render da bunu kullanabilir)."""
        return jsonify({"durum": "aktif"}), 200

    return app
