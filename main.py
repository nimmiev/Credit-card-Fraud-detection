from flask import Flask 
from public import public
from admin import admin
from user import user
from api import api
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail


app=Flask(__name__)

app.secret_key='key'

app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(api,url_prefix='/api')
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hariharan0987pp@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjcbcumvkpqynpep'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.run(debug=True,port=5002,host="0.0.0.0")