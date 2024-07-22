from waitress import serve

from app import create_app

app = create_app()
wsgi_app = app.wsgi_app

if __name__ == "__main__":
    serve(wsgi_app, host="0.0.0.0", port=8000, url_scheme="https")
