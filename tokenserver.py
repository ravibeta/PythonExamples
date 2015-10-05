# coding: utf-8

from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from tokenprovider import TokenProvider

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql://root:thepassword@127.0.0.1/token',
})
db = SQLAlchemy(app)
oauth = OAuth2Provider(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    salt = db.Column(db.String(4))

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(6), unique=True)
    
def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        return redirect('/')
    user = current_user()
    return jsonify({'msg': 'welcome,'+ str(user), 'success':'success'}), 200

@oauth.tokengetter
def check_token(access_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    return None


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        user_id=request.user.id
    ).all()
    # make sure that every client has only one token connected to a user
    db.session.delete(toks)

    tok = Token(**token)
    tok.user_id = request.user.id
    db.session.add(tok)
    db.session.commit()
    return tok


if __name__ == '__main__':
    db.create_all()
    app.run()




def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None
