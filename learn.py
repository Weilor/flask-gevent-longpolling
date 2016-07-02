# coding = utf-8

from gevent.pywsgi import WSGIServer
from gevent.queue import Queue, Empty
from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm
from flask_bootstrap import Bootstrap
import simplejson

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'HARD'
messages = []
user_dict = {}


@app.route('/put_post/<user>', methods=["POST"])
def put_post(user):
    post = request.form['message']
    for u in user_dict:
         user_dict[u].put_nowait(post)
    return ""


@app.route('/get_post/<user>', methods=["GET", "POST"])
def get_post(user):
    q = user_dict[user]
    try:
        p = q.get(timeout=10)
    except Empty:
        p = ''
    return simplejson.dumps(p)


@app.route('/chatroom/<user>/')
def chatroom(user):
    user_con = user_dict.setdefault(user, Queue())
    return render_template("chatroom.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("chatroom", user=form.name.data))
    return render_template("login.html", form=form)


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
