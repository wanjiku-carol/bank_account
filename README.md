### Bank Account API

#### Description
It is an API that enables creating a bank account, checking balance and depositing.

### Development
Navigate to the cloned repo. 

Ensure you have the following:

```
1. postgres
2. python3 & a virtualenv
3. Flask
4. Postman
```

Create a virtualenv and activate it. [Refer here](https://docs.python.org/3/tutorial/venv.html)

### Dependencies
- Install the project dependencies:
> $ pip install -r requirements.txt


### Set up Database
- Create a database:
> $ createdb bankaccounts

- Run migrations:
> $ python manage.py db upgrade

After setting up the above. Run:

```python -m app```

### Endpoints
- Create account: 

POST: `/account`
> {
> "name": "some_name",
> "pin": pin
> }

- Login account: 

POST: `/login`
> {
> "name": "your_name",
> "pin": pin
> }
Get the authorization token and use it for the other requests

- Get balance: 

GET: `/account/<acc_id>/balance`

- Deposit: 

POST: `/account/<acc_id>/deposit`
> {
> "amount": 1000,
> "deposit": true
> }


Test the endpoints registered on `app.py` on Postman/curl on the port the app is running on. 

