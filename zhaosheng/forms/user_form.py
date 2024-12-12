from wtforms import Form, StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length

class UserForm(Form):
    username = StringField('用户名', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    email = EmailField('邮箱', validators=[DataRequired()])
    phone = StringField('电话', validators=[DataRequired(), Length(min=10, max=15)])
