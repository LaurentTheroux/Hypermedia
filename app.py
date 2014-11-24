#!flask/bin/python
from flask import Flask
from flask import render_template
from flask import request
import flask
from connexion import db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    return "Registration reussie <a href='/'>OK</a>"

@app.route('/membres', methods=['GET'])
def membres_get():
    users = db.cursor()
    users.execute("select * from user")
    return render_template('membres.html', users=users)


@app.route('/livres', methods=['GET'])
def livres_get():
    livres = db.cursor()
    livres.execute("select * from livre")
    return render_template('livres.html', livres=livres)


@app.route('/livre/delete', methods=['POST'])
def livres_delete():
    ISBN = request.values['ISBN']

    delete = db.cursor()
    delete.execute("DELETE FROM livre WHERE ISBN='%s'" % ISBN)
    db.commit()

    return flask.redirect('/livres')


if __name__ == '__main__':
    # Start Flask
    app.run(debug=True)
