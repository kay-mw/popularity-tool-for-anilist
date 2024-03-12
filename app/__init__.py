from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


# mode = "dev"

# if __name__ == '__main__':
#     if mode == "dev":
#         main.run(host='0.0.0.0', debug=False)
#     else:
#         serve(main)