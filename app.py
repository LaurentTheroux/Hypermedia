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


@app.route('/livres/Enfants', methods=['GET'])
def livres_Enfants():
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Enfant")
    return render_template('enfant.html', livres=livres)


@app.route('/livres/Cuisine', methods=['GET'])
def livres_Cuisine():
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Cuisine")
    return render_template('cuisine.html', livres=livres)


@app.route('/livres/Ecole', methods=['GET'])
def livres_Ecole():
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Ecole")
    return render_template('ecole.html', livres=livres)


@app.route('/livres/Sciencefiction', methods=['GET'])
def livres_Sciencefiction():
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Sciencefiction")
    return render_template('sciencefiction.html', livres=livres)


@app.route('/panier/ajout', methods=['POST'])
def panier_ajout():
    ajoutpanier = db.cursor()
    ajoutpanier.execute(
        "insert into panier(username, ISBN) "
        "values('%(username)s','%(ISBN)s'" % request.values)
    db.commit()
    return flask.redirect('/panier')


@app.route('/panier', methods=['POST'])
def panier():
    panier = db.cursor()
    panier.execute(
        "Select * from panier where username='%s'" % "roger")
    db.commit()
    return render_template("panier.html", panier=panier)


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    registration = db.cursor()
    registration.execute(
        "insert into user(username, password, nom, prenom, courriel, codePostal, adresse, permission, dette) "
        "values('%(username)s','%(password)s','%(nom)s','%(prenom)s','%(courriel)s','%(codePostal)s','%(adresse)s',1,0) "
        % request.values
    )
    db.commit()
    return "Registration reussie <a href='/'>OK</a>"


@app.route('/membres/<username>', methods=['GET'])
def membre_get(username):
    user = db.cursor()
    user.execute("select * from user where username='%s'" % username)
    return render_template('membre.html', user=user.fetchone())


@app.route('/membres/<username>/modification', methods=['POST'])
def membre_modification(username):
    user = db.cursor()
    update = \
        "update user " \
        "set username='%(username)s', password='%(password)s', nom='%(nom)s', " \
        "prenom='%(prenom)s', courriel='%(courriel)s'," \
        " codePostal='%(codePostal)s', adresse='%(adresse)s'," \
        " permission='%(permission)s', dette='%(dette)s' " % request.values
    update += "where username='%s'" % username
    user.execute(update)
    return flask.redirect('/membres')


@app.route('/livre', methods=['GET'])
def livre():
    return render_template('livre.html')


@app.route('/livre/ajout', methods=['POST'])
def livre_ajout():
    ajout = db.cursor()
    ajout.execute(
        "insert into livre(titre, auteur, nombrePage, prix, categorie, rating, datePublication) "
        "values('%(titre)s','%(auteur)s','%(nombrePage)s',"
        "'%(prix)s','%(categorie)s','%(rating)s','%(datePublication)s')"
        % request.values
    )
    db.commit()
    return "Nouveau livre ajouter <a href='/'>OK</a>"


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


@app.route('/membres/delete', methods=['POST'])
def membres_delete():
    username = request.values['username']

    delete = db.cursor()
    delete.execute("DELETE FROM user WHERE username='%s'" % username)
    db.commit()

    return flask.redirect('/membres')


if __name__ == '__main__':
    # Start Flask
    app.run(debug=True)
