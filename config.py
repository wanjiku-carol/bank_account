import os

class Config:
  TESTING=True
  DEBUG=True
  FLASK_APP='app.py'
  SECRET_KEY='secret-key'
  DATABASE_URI='postgresql:///bankaccounts'
  SQLALCHEMY_DATABASE_URI='postgresql:///bankaccounts'
  SQLALCHEMY_TRACK_MODIFICATIONS=True
  PROPAGATE_EXCEPTIONS=True
  
class TestConfig(Config):
  TESTING=True
  DEBUG=True
  DATABASE_URI='postgresql:///test_db'

app_config = {
    'testing': TestConfig,
}
