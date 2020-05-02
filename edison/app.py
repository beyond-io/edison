import edison
import edison.models as models

from flask import render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager


app = edison.app
db = edison.db
api = Api(app)

# Creates all tables defined in the database models and the only ones that are not created yet.
# If there's any change in the database models you should perform a migration to apply this change in the database itself.
# More about database migrations can be found in /edison/migrations/README.
db.create_all()

# Creation of Json-Web-Token manager.
# In order to reach secured endpoints client should add an authorization header with the value Bearer <token>.
jwt = JWTManager(app)

# This decorator is a callback and it is called every time user is trying to access secured endpoints. 
# The function under the decorator should return true or false depending on if the passed token is blacklisted.
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.Token.query.filter_by(jti=jti).first() is not None

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
