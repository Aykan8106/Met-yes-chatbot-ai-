# app/database.py — SQL SADECE bu dosyada bulunur
import sqlite3
from flask import current_app


def get_db():
    """Veritabanına bağlanır; satırlara sütun adıyla erişim sağlar."""
    db = sqlite3.connect(current_app.config['DATABASE_URL'])
    db.row_factory = sqlite3.Row  # row['isim'] şeklinde erişim
    return db


def init_db(app):
    """'leads' tablosunu oluşturur (yoksa)."""
    with app.app_context():
        db = get_db()
        try:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    isim    TEXT NOT NULL,
                    telefon TEXT NOT NULL,
                    mesaj   TEXT,
                    tarih   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            db.commit()
        finally:
            db.close()


def lead_ekle(isim, telefon, mesaj=''):
    """Yeni lead ekler ve eklenen kaydın id'sini döndürür."""
    db = get_db()
    try:
        # ? yer tutucusu: SQL Injection'a karşı zorunlu koruma
        cursor = db.execute(
            "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
            (isim, telefon, mesaj),
        )
        db.commit()
        return cursor.lastrowid
    finally:
        db.close()


def tum_leadler():
    """Tüm kayıtları en yeniden eskiye, sözlük listesi olarak döndürür."""
    db = get_db()
    try:
        satirlar = db.execute(
            "SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY id DESC"
        ).fetchall()
        # Row nesnelerini sözlüğe çeviriyoruz ki JSON'a kolayca dönüşsün
        return [dict(satir) for satir in satirlar]
    finally:
        db.close()