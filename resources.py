import config
from flask import make_response, json, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
  create_access_token, create_refresh_token, jwt_refresh_token_required,
  get_jwt_identity, fresh_jwt_required, jwt_required
  )
from flask_restful import Resource, reqparse
from models import db, BankAccountUser, Transactions

_account_parser = reqparse.RequestParser()
_login_parser = reqparse.RequestParser()

_account_parser.add_argument(
  "name",
  type=str,
  required=True,
  help="This field cannot be blank"
)

_account_parser.add_argument(
  "pin",
  type=str,
  required=True,
  help="This field cannot be blank"
)

_account_parser.add_argument(
  "pin",
  type=str,
  required=True,
  help="This field cannot be blank"
)

_login_parser.add_argument(
  "name",
  type=str,
  required=True,
  help="This field cannot be blank"
)

_login_parser.add_argument(
  "pin",
  type=str,
  required=True,
  help="This field cannot be blank"
)

class BankAccountResource(Resource):
  def get(self, id):
    account = BankAccountUser.get_account_by_id(id)
    if account:
      json_account = account.json_dumps()
      return make_response({"status": "success","data": json_account}, 200)
    return make_response({"error": "Account not found"}, 404)

  def post(self):
    data = _account_parser.parse_args()
    bank_acc = BankAccountUser.query.filter_by(name=data['name']).all()
    if bank_acc:
      return make_response({"error": "Account already exists"}, 400)
    hashed_pin = generate_password_hash(data['pin'], method='sha256')
    new_acc = BankAccountUser(
      name=data['name'], 
      balance=0,
      pin=hashed_pin
      )
    new_acc.save()
    json_data = new_acc.json_dumps()
    return make_response({"status": "success","data": json_data}, 200)


class LoginResource(Resource):
  def post(self):
    data = _login_parser.parse_args()
    user = BankAccountUser.get_account_by_name(data['name'])
    if user and user.check_password(data['pin']):
      access_token = create_access_token(identity=user.id, fresh=True)
      refresh_token = create_refresh_token(identity=user.id)
      token_info = {"access_token": access_token, "refresh_token": refresh_token}
      return make_response({"status": "success", "data": token_info}, 200)
    else:
      return make_response({"error": "Invalid credentials"}, 400)


class BalanceResource(Resource):
  @jwt_required
  def get(self, id):
    account =  BankAccountUser.get_account_by_id(id)
    if account:
      balance = account.balance
      json_data = {"balance": balance}
      return make_response({"status": "success", "data": json_data}, 200)
    return make_response({"error": "bank acc not found"}, 404)
    
class DepositResource(Resource):
  @jwt_required
  def post(self, id):
    """Allows for depositing to an account"""
    account = BankAccountUser.get_account_by_id(id)
    json_input = json.loads(request.data)
    if account:
      amount = json_input.get('amount')
      deposit = json_input.get('deposit')
      new_transaction = Transactions(
        amount=amount,
        deposit=deposit,
        account_id=id
      )
      new_transaction.save()

      new_transaction.adjust_balance(action='deposit')
      json_data = {"balance": account.balance}
      return make_response({"status": "success", "New Balance": json_data}, 200)
    return make_response({"status": "Acc not found"}, 404)

class TokenRefreshResource(Resource):
  @jwt_refresh_token_required
  def post(self):
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return make_response({"access_token": access_token}, 200)
