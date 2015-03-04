from flask import g
from flask.ext import restful

from .serializers import UserSerializer
from .forms import UserCreateForm, SessionCreateForm
from .. import db, api, auth
from ..models import User
from ..email import send_email

'''
curl -X POST -d "email=test@example.com&password=password" http://localhost:5000/api/v1/users
curl -u email:password -X GET http://localhost:5000/api/v1/confirm/<token>
'''


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@api.resource('/users')
class UserView(restful.Resource):
    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(email=form.email.data, password=form.password.data, lname=(form.lname.data).upper(), fname=(form.fname.data).upper())
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'email/auth_confirm', user=user, token=token)
        return UserSerializer(user).data

@api.resource('/sessions', endpoint='auth.login')
class SessionView(restful.Resource):
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            print ('User login successfully!')
            return UserSerializer(user).data, 201
        return '', 401

@api.resource('/confirm/<token>', endpoint='auth.confirm')
class UserConfirm(restful.Resource):
    @auth.login_required
    def get(self, token):
        if g.current_user.confirmed:
            return 'ALREADY CONFIRED'
        if g.current_user.confirm(token):
            return 'You have confirmed your account. Thanks!'
        else:
            return 'The confirmation link is invalid or has expired.'
        return '', 401

# api.add_resource(UserView, '/users')
# api.add_resource(UserConfirm, '/confirm/<token>', endpoint='auth.confirm')
# api.add_resource(SessionView, '/sessions', endpoint='auth.login')
