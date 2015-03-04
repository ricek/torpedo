from flask.ext.wtf import Form

from wtforms_alchemy import model_form_factory
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from .. import db
from ..models import User

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class UserCreateForm(ModelForm):
    class Meta:
        model = User

    password = PasswordField()

class SessionCreateForm(Form):
    email = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
