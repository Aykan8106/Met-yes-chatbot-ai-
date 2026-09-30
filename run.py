# run.py - Sunucuyu baslatan giris noktasi
from app import create_app

# gunicorn "run:app" ile bu degiskeni arar
app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=app.config['DEBUG'])
