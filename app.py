from flask import Flask
from blueprint.user import bp as lg_bp
from blueprint.index import bp as ix_bp

app = Flask(__name__)

app.register_blueprint(ix_bp)
app.register_blueprint(lg_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
