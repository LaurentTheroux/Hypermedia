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
        if not request.form['username'] or not request.form['password']:
            error = "Votre username ou mot de passe est manquant"
            return render_template('index.html', error=error)
        else:
            userpass = db.cursor()
            userpass.execute("select password from user where username ='%s'" % request.form['username'])
            pwd = userpass.fetchone()
            if pwd is not None and request.form['password'] == pwd[0]:
                session["username"] = request.form['username']
                userpermission = db.cursor()
                userpermission.execute("Select permission from user where username ='%s'" % session['username'])
                if userpermission.fetchone()[0] == 1:
                    session['permission'] = "admin"
                else:
                    session['permission'] = "user"
                return render_template('index.html', message="Bienvenue, %s" % request.form['username'])
            else:
                error = "Echec de connexion"
                return render_template('index.html', error=error)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    error = None
    message = "USER " + session['username'] + " successfully logged out."
    session['username'] = None
    session['permission'] = None
    return render_template('index.html', message=message)


@app.route('/livres/Enfants', methods=['GET'])
def livres_Enfants():
    titre = 'Livres pour enfants:'
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Enfant")
    return render_template('basecat.html', livres=livres, titre=titre)


@app.route('/livres/Cuisine', methods=['GET'])
def livres_Cuisine():
    titre = 'Livres de cuisine:'
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Cuisine")
    return render_template('basecat.html', livres=livres, titre=titre)


@app.route('/livres/Ecole', methods=['GET'])
def livres_Ecole():
    titre = 'Livres pour la rentre:'
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Ecole")
    return render_template('basecat.html', livres=livres, titre=titre)


@app.route('/livres/Sciencefiction', methods=['GET'])
def livres_Sciencefiction():
    titre = 'Livres de science-fiction:'
    livres = db.cursor()
    livres.execute("select * from livre where categorie='%s'" % "Sciencefiction")
    return render_template('basecat.html', livres=livres, titre=titre)


@app.route('/livres/panier/ajout', methods=['POST'])
def panier_ajout():
    error = None
    if session['username'] is None:
        error= "Vous devez vous connecter pour ajouter un item au panier."
        return render_template('index.html', error=error)
    else:
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
def panier(message=None, error=None):
    panier = db.cursor()
    panier.execute(
        "Select ISBN from panier where username='%s'" % session['username'])
    listeLivres = panier.fetchall();
    listePanier =[]
    prixpanier = 0

    for i in range(0, len(listeLivres)):
        panier.execute("Select prix from livre where ISBN='%s'" % listeLivres[i][0])
        prixpanier += panier.fetchone()[0]

    for i in range(0, len(listeLivres)):
        panier.execute("Select * from livre where ISBN='%s'" % listeLivres[i][0])
        listePanier.append(panier.fetchone())
    db.commit()
    return render_template('panier.html', listePanier=listePanier, message=message, error=error, prixpanier=prixpanier)


@app.route('/panier/delete', methods=['POST'])
def panier_delete():
    ISBN = request.values['ISBN']
    delete = db.cursor()
    delete.execute("DELETE FROM panier WHERE ISBN='%s'" % ISBN)
    db.commit()
    return flask.redirect('livres/panier')


@app.route('/panier/achat', methods=['POST'])
def panier_achat():
    error = None
    message = None
    soldeuser = db.cursor()
    soldeuser.execute("Select solde from user WHERE username='%s'" % session['username'])
    solde = soldeuser.fetchone()[0]
    prixpanier = 0
    p = db.cursor()
    p.execute(
        "Select ISBN from panier where username='%s'" % session['username'])
    listeLivres = p.fetchall();
    listePanier =[]
    for i in range(0, len(listeLivres)):
        p.execute("Select prix from livre where ISBN='%s'" % listeLivres[i][0])
        prixpanier += p.fetchone()[0]
    if prixpanier>solde:
        error = "Solde insuffisant"

    else:
        message = "Achat effectuer! "
        prixuser = {'username': session['username'],'prixpanier': prixpanier}
        achat = db.cursor()
        achat.execute("Update user SET solde=(solde-%(prixpanier)s) where username='%(username)s'" % prixuser )
        delete = db.cursor()
        delete.execute("DELETE FROM panier WHERE username='%s'" % session['username'])
        db.commit()
    return panier(message=message, error=error)
    # return flask.redirect('livres/panier')


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    registration = db.cursor()
    if 'permission' in session.keys() and session['permission'] == 'admin':
         registration.execute(
        "insert into user(username, password, nom, prenom, courriel, codePostal, adresse, permission, solde) "
        "values('%(username)s','%(password)s','%(nom)s','%(prenom)s','%(courriel)s','%(codePostal)s','%(adresse)s',%(permission)s, 0)"
        % request.values)
    else:
         registration.execute(
             "insert into user(username, password, nom, prenom, courriel, codePostal, adresse, permission, solde)"+
             "values('%(username)s','%(password)s','%(nom)s','%(prenom)s','%(courriel)s','%(codePostal)s','%(adresse)s',2, 0) " % request.values)
         db.commit()

    return render_template('loginsuccess.html')


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
        " permission='%(permission)s' " % request.values
    update += "where username='%s'" % username
    user.execute(update)
    return flask.redirect('/membres')


@app.route('/livres/<ISBN>', methods=['GET'])
def livre1_get(ISBN):
    livre = db.cursor()
    livre.execute("select * from livre where ISBN='%s'" % ISBN)
    return render_template('livre.html', livre=livre.fetchone())


@app.route('/livre', methods=['GET'])
def livre_get():
    return render_template('newlivre.html',)


@app.route('/livres/<ISBN>/modification', methods=['POST'])
def livres_modification(ISBN):
    livre = db.cursor()
    update = \
        "update livre " \
        "set titre='%(titre)s', auteur='%(auteur)s', " \
        "nombrePage='%(nombrePage)s', prix='%(prix)s'," \
        " categorie='%(categorie)s', quantite='%(quantite)s'," \
        " datePublication='%(datePublication)s' " % request.values
    update += "where ISBN='%s'" % ISBN
    livre.execute(update)
    return flask.redirect('/livres')


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
    return flask.redirect('/livres')


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
