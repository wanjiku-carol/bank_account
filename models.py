from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class BankAccountUser(db.Model):
  __tablename__ = 'bank_accounts'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  balance = db.Column(db.Float, nullable=True)
  pin = db.Column(db.String, nullable=False)
  when_created = db.Column(db.DateTime, server_default=db.func.current_timestamp())
  transactions = db.relationship(
                            'Transactions', lazy='select', 
                            backref=db.backref('transactions', 
                            lazy='joined')
                            )

  def json_dumps(self):
    return dict(
      name=self.name,
      balance=self.balance
    )

  def save(self):
    db.session.add(self)
    db.session.commit()

  def check_password(self, pin):
    return check_password_hash(self.pin, pin)

  @classmethod
  def get_account_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  @classmethod
  def get_account_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
  

class Transactions(db.Model):
  __tablename__ = 'transactions'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  deposit = db.Column(db.Boolean, nullable=False)
  when_created = db.Column(db.DateTime, server_default=db.func.current_timestamp())
  account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id', ondelete='CASCADE'), 
                          nullable=False)

  def json_dumps(self):
    return dict(
      transaction_id=self.id,
      amount=self.amount
    )

  def save(self):
    db.session.add(self)
    db.session.commit()

  def adjust_balance(self, action):
    account = BankAccountUser.get_account_by_id(self.account_id)
    if action == 'deposit':
      account.balance = account.balance + self.amount
    elif action == 'withdraw':
      account.balance  = account.balance - self.amount
    db.session.commit()
