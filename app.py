#!flask/bin/python
from flask import Flask
from flask import render_template
from flask import request
from flask import session
import flask
from connexion import db

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        userpass = db.cursor()
        userpass.execute("select password from user where username ='%s'" % request.form['username'])
        pwd = userpass.fetchone()
        if request.form['password'] == pwd[0]:
            session["username"] = request.form['username']
            return render_template('Welcome.html', username=request.form['username'])
        else:
            error = pwd[0]
            return render_template('index.html', error=error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid



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


@app.route('/livres/panier/ajout', methods=['POST'])
def panier_ajout():
    error = None
    ajoutpanier = db.cursor()
    ajoutpanier.execute("Select * from panier where ISBN='%s'" % request.form['ISBN'])
    if ajoutpanier.fetchone() is None:
        itempanier = {'username': session['username'],'ISBN': request.form['ISBN'], 'Quantite': '1'}
        ajoutpanier.execute(
        "insert into panier(username, ISBN, Quantite) "
        "values('%(username)s','%(ISBN)s', '%(Quantite)s')" % itempanier)
        db.commit()
    else:
        itempanier = {'username': session['username'],'ISBN': request.form['ISBN']}
        ajoutpanier.execute("Select Quantite from livre where ISBN='%s'" %request.form['ISBN'])
        quantiteEnStock = ajoutpanier.fetchone()[0]
        ajoutpanier.execute("Select Quantite from panier where username='%(username)s' AND ISBN='%(ISBN)s'" % itempanier)
        quantiteEnPanier = ajoutpanier.fetchone()[0]

        if quantiteEnStock > quantiteEnPanier:
            ajoutpanier.execute("Update panier SET quantite=quantite+1 where username='%(username)s' AND ISBN='%(ISBN)s'" % itempanier )
            db.commit();
        else:
            error = "Votre panier contient tous les exemplaires en stock"


    return flask.redirect('/livres/panier')


@app.route('/livres/panier', methods=['GET'])
def panier():
    panier = db.cursor()
    panier.execute(
        "Select ISBN from panier where username='%s'" % session['username'])
    listeLivres = panier.fetchall();
    listePanier =[]
    for i in range(0, len(listeLivres)):
        panier.execute("Select * from livre where ISBN='%s'" % listeLivres[i][0])
        listePanier.append(panier.fetchone())
    db.commit()
    return render_template('panier.html', listePanier=listePanier)


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
        "insert into livre(titre, auteur, nombrePage, prix, categorie, quantite, datePublication) "
        "values('%(titre)s','%(auteur)s','%(nombrePage)s',"
        "'%(prix)s','%(categorie)s','%(quantite)s','%(datePublication)s')"
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
