from flask import Flask
from .config import Config
from .extensions import db, migrate, mail, jwt

from app.pet.routes import pet_api
from app.produtos.routes import produto_api
from app.servico.routes import servico_api
from app.usuario.routes import usuario_api
from app.van.routes import van_api

'''
from .pet.model import Pet
from .produtos.model import Produtos
from .servico.model import Servico
from .usuario.model import Usuario
from .van.model import Van
'''

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(pet_api)
    app.register_blueprint(produto_api)
    app.register_blueprint(servico_api)
    app.register_blueprint(usuario_api)
    app.register_blueprint(van_api)


    return app