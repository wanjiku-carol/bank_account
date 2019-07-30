import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import config
from models import db
from resources import BalanceResource, DepositResource, LoginResource, BankAccountResource

def create_app():
  app = Flask('__name__')
  app.config.from_object('config.Config')

  api = Api(app)
  jwt = JWTManager(app)
  db.init_app(app)
  jwt.init_app(app)
  
  with app.app_context():
    # add resources here
    api.add_resource(BankAccountResource, '/account', '/account/', '/account/<int:id>/', '/account/<int:id>', )
    api.add_resource(LoginResource, '/login', '/login/')
    api.add_resource(BalanceResource, '/account/<int:id>/balance/', '/account/<int:id>/balance')
    api.add_resource(DepositResource, '/account/<int:id>/deposit', '/account/<int:id>/deposit/')                     
    db.create_all()

  return app

if __name__ == '__main__':
  app = create_app()
  app.run()
