#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = '1606'


from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # "serveurmysql" sur les machines de l'IUT
            user="kstrub",
            password="mdp",
            database="BDD_kstrub",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# chercher des informations
# mycursor = get_db().cursor()
# sql='''   SELECT      '''
# mycursor.execute(sql)
# liste_enregistrement = mycursor.fetchall()
# un_enregistrement = mycursor.fetchone()

# ajouter, modifier ou supprimer des informations
# mycursor = get_db().cursor()
# sql=""
# mycursor.execute(sql)
# get_db().commit()

####################################################################

@app.route('/')
@app.route('/accueil')
def show_layout():
 return render_template('layout.html')

####################################################################

@app.route('/reparation/show')
def show_reparation():
    mycursor = get_db().cursor()
    sql=''' SELECT Reparation.id_reparation, Reparation.libelle_reparation, Reparation.immat_voiture, Reparation.prix_reparation, Reparation.date_reparation, Type_reparation.id_type, Type_reparation.libelle_type, Reparation.photo
FROM Reparation
INNER JOIN Type_reparation ON Reparation.type_reparation_id = Type_reparation.id_type
ORDER BY id_reparation ASC; '''
    mycursor.execute(sql)
    listeReparation = mycursor.fetchall()
    return render_template('reparation/show_reparation.html', reparations=listeReparation)


@app.route('/add/reparation', methods=['GET'])
def add_reparation():
    mycursor = get_db().cursor()
    sql1 = ''' SELECT id_type, libelle_type FROM Type_reparation; '''
    mycursor.execute(sql1)
    infosReparation1 = mycursor.fetchall()

    sql2 = ''' SELECT photo FROM Reparation; '''
    mycursor.execute(sql2)
    infosReparation2 = mycursor.fetchall()
    return render_template('reparation/add_reparation.html', reparations1=infosReparation1, reparations2=infosReparation2)

@app.route('/reparation/add', methods=['POST'])
def valid_add_reparation():
    libelle_reparation = request.form.get('libelle_reparation')
    immat_voiture = request.form.get('immat_voiture')
    prix_reparation = request.form.get('prix_reparation')
    date_reparation = request.form.get('date_reparation')
    type_reparation_id = request.form.get('type_reparation_id')
    photo = request.form.get('photo')
    tuple_sql = (libelle_reparation, immat_voiture, prix_reparation, date_reparation, type_reparation_id, photo)
    mycursor = get_db().cursor()
    sql= ''' INSERT INTO Reparation(id_reparation, libelle_reparation, immat_voiture, prix_reparation, date_reparation, type_reparation_id, photo) VALUES (NULL, %s, %s, %s, %s, %s, %s); '''
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Reparation ajoutée :  nom de la réparation='+libelle_reparation+' | immatriculation de la voiture = '+immat_voiture+' | prix de la reéaration = '+prix_reparation+' | date de la réparation = '+date_reparation+' | type de la réparation = '+type_reparation_id
    flash(message, 'alert-success')
    return redirect('/reparation/show')


@app.route('/edit/reparation', methods=['GET'])
def edit_reparation():
    mycursor = get_db().cursor()
    id_reparation = request.args.get('id', '')
    sql1 = ''' SELECT libelle_reparation, immat_voiture, prix_reparation, date_reparation, type_reparation_id, photo  FROM Reparation WHERE id_reparation=%s; '''
    mycursor.execute(sql1, (id_reparation,))
    rep = mycursor.fetchone()
    sql = ''' SELECT id_type, libelle_type FROM Type_reparation ; '''
    mycursor.execute(sql)
    infosTypesReparation = mycursor.fetchall()
    sqlPhoto = ''' SELECT photo FROM reparation ; '''
    mycursor.execute(sqlPhoto)
    infosPhoto = mycursor.fetchall()
    return render_template('reparation/edit_reparation.html', typesReparations=infosTypesReparation, reparation=rep, reparationPhoto=infosPhoto, id=id_reparation)

@app.route('/reparation/edit', methods=['POST'])
def valid_edit_reparation():
    mycursor = get_db().cursor()
    libelle_reparation = request.form.get('libelle_reparation')
    immat_voiture = request.form.get('immat_voiture', '')
    prix_reparation = request.form.get('prix_reparation', '')
    date_reparation = request.form.get('date_reparation', '')
    type_reparation_id = request.form.get('type_reparation_id', '')
    photo = request.form.get('photo', '')
    id_reparation = request.form.get('id', '')
    tuple_sql = (libelle_reparation, immat_voiture, prix_reparation, date_reparation, type_reparation_id, photo, id_reparation)
    sql= ''' UPDATE Reparation SET libelle_reparation = %s, immat_voiture = %s, prix_reparation = %s, date_reparation = %s, type_reparation_id =%s, photo=%s WHERE id_reparation = %s; '''
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Reparation modifiée: Id = ' + id_reparation + ' | nom de la réparation = '+libelle_reparation+' | immatriculation de la voiture = '+immat_voiture+' | prix de la reéaration = '+prix_reparation+' | date de la réparation = '+date_reparation+' | type de la réparation = '+type_reparation_id +' | photo de la réparation = '+photo
    flash(message, 'alert-warning')
    return redirect('/reparation/show')

@app.route('/delete/reparation')
def delete_reparation():
    mycursor = get_db().cursor()
    id_reparation = request.args.get('id')
    sql=''' DELETE FROM reparation WHERE id_reparation=%s '''
    mycursor.execute(sql,id_reparation)
    get_db().commit()
    message = u'Reparation ' + id_reparation + ' supprimé!'
    flash(message, 'alert-danger')
    return redirect('/reparation/show')



@app.route('/type-reparation/show')
def show_type_reparation():
    mycursor = get_db().cursor()
    sql=''' SELECT tr.id_type, tr.libelle_type, tr.logo, COUNT(r.id_reparation) AS nombre_reparations
FROM Type_reparation tr
LEFT JOIN Reparation r ON tr.id_type = r.type_reparation_id
GROUP BY tr.id_type, tr.libelle_type
ORDER BY tr.id_type ASC; '''
    mycursor.execute(sql)
    listeTypeReparation = mycursor.fetchall()
    return render_template('type-reparation/show_type_reparation.html', typeReparations=listeTypeReparation)



@app.route('/add/type-reparation', methods=['GET'])
def add_type_reparation():
    mycursor = get_db().cursor()
    sqlInfos = ''' SELECT libelle_type, logo FROM Type_reparation; '''
    mycursor.execute(sqlInfos)
    infoTypeReparation = mycursor.fetchall()
    return render_template('type-reparation/add_type_reparation.html', Type_reparation=infoTypeReparation)

@app.route('/type-reparation/add', methods=['POST'])
def valid_add_type_reparation():
    libelle_type = request.form.get('libelle_type')
    logo = request.form.get('logo')
    tuple_sql = (libelle_type, logo)
    mycursor = get_db().cursor()
    sql= ''' INSERT INTO Type_reparation(id_type, libelle_type, logo) VALUES (NULL, %s, %s); '''
    mycursor.execute(sql,tuple_sql)
    get_db().commit()
    message = u'Type de réparation about:  nom de la réparation='+libelle_type + 'nom du logo='+logo
    flash(message, 'alert-success')
    return redirect('/type-reparation/show')

@app.route('/edit/type-reparation', methods=['GET'])
def edit_type_reparation():
    mycursor = get_db().cursor()
    id_type = request.args.get('id', '')
    sql1 = ''' SELECT id_type, libelle_type, logo  FROM Type_reparation WHERE id_type=%s; '''
    mycursor.execute(sql1, (id_type,))
    type = mycursor.fetchone()
    return render_template('type-reparation/edit_type_reparation.html',  type_reparation=type, id=id_type)

@app.route('/type-reparation/edit', methods=['POST'])
def valid_edit_type_reparation():
    mycursor = get_db().cursor()
    libelle_type = request.form.get('libelle_type')
    logo = request.form.get('logo')
    id_type = request.form.get('id', '')
    tuple_sql = (libelle_type, logo, id_type)
    sql1= ''' UPDATE Type_reparation SET libelle_type = %s, logo=%s WHERE id_type = %s; '''
    mycursor.execute(sql1, tuple_sql)
    get_db().commit()
    message = u'Type de réparation ' + id_type + ' mis à jour: nom de type de réparation=' + libelle_type + ' | logo = ' + logo
    flash(message, 'alert-warning')
    return redirect('/type-reparation/show')




@app.route('/reparation/etat')
def reparationEtat():
    mycursor = get_db().cursor()
    sql1=''' SELECT
    COUNT(DISTINCT r.id_reparation) AS total_reparations,
    SUM(r.prix_reparation) AS total_prix_reparation,
    ROUND(AVG(r.prix_reparation), 2) AS prix_moyen_reparation,
    COUNT(DISTINCT tr.id_type) AS nombre_types_reparation
FROM
    Reparation r
LEFT JOIN
    Type_reparation tr ON r.type_reparation_id = tr.id_type; '''
    mycursor.execute(sql1)
    listeReparation1 = mycursor.fetchall()

    sql2 = '''SELECT tr.id_type, tr.libelle_type, COUNT(r.id_reparation) AS nombre_reparations,SUM(r.prix_reparation) AS total_prix_reparation, ROUND(AVG(r.prix_reparation), 2) AS prix_moyen_reparation
FROM Type_reparation tr
LEFT JOIN Reparation r ON tr.id_type = r.type_reparation_id
GROUP BY tr.id_type, tr.libelle_type
ORDER BY tr.id_type ASC; '''
    mycursor.execute(sql2)
    listeReparation2 = mycursor.fetchall()
    return render_template('reparation/etat_reparation.html', reparations1=listeReparation1, reparations2=listeReparation2)





@app.route('/type-reparation/delete', methods=['GET'])
def delete_type_reparation():
    print('''suppression d'un type de réparation''')
    id = request.args.get('id',0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql = '''SELECT *
        FROM reparation 
        JOIN type_reparation
        ON reparation.type_reparation_id = type_reparation.id_type
        WHERE id_type=%s;'''
    mycursor.execute(sql, tuple_param)
    count = mycursor.fetchall()
    if (str(count) != '()'):
        sql = '''SELECT *
        FROM type_reparation
        WHERE id_type=%s;'''
        tuple_param=(id)
        mycursor.execute(sql,tuple_param)
        type = mycursor.fetchone()

        sql1 = '''SELECT COUNT(id_reparation)  AS nombre_reparations
                FROM Reparation
                WHERE type_reparation_id=%s;'''
        mycursor.execute(sql1, tuple_param)
        type1 = mycursor.fetchall()

        return render_template('/type-reparation/delete_type_reparation.html', reparations=count, typeReparation=type, repa=type1)
    sql = '''DELETE FROM type_reparation WHERE id_type=%s;'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id = request.args.get('id', 0)
    print(u'Un type de réparation supprimé, Id du type :', id)
    message = u'Un Un type de réparation supprimé, Id du type : ' + id
    flash(message, 'alert-warning')
    return redirect('/type-reparation/show')

@app.route('/delete/type-reparation', methods=['GET'])
def delete_reparation_cascade():
    print('''Suppression d'une réparation du type sélectionné''')
    id=request.args.get('id',0)
    print(id)
    mycursor = get_db().cursor()
    tuple_param=(id)
    sql='''SELECT type_reparation_id
    FROM reparation
    WHERE id_reparation=%s;'''
    mycursor.execute(sql,tuple_param)
    type_id = mycursor.fetchone()
    sql="DELETE FROM reparation WHERE id_reparation=%s;"
    mycursor.execute(sql,tuple_param)
    #d
    get_db().commit()
    print(request.args)
    print(request.args.get('id'))
    id=request.args.get('id',0)
    print(u'Une réparation supprimé, Id de la réparation :', id)
    message = u'Une réparation supprimé, Id de la réparation : '+id
    flash(message, 'alert-warning')
    return redirect('/type-reparation/delete?id='+str(type_id['type_reparation_id']))


@app.route('/reparation/filtre', methods=['GET'])
def filtre_reparation():
    # print(auteurs)

    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM type_reparation '''
    mycursor.execute(sql)
    typeReparation = mycursor.fetchall()

    sql = ''' SELECT * FROM reparation '''
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if 'filter_word' in session:
        sql = sql + " libelle_reparation Like %s "
        recherche = "%" + session['filter_word'] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if 'filter_prix_min' in session or 'filter_prix_max' in session:
        sql = sql + condition_and + 'prix_reparation BETWEEN %s AND %s'
        list_param.append(session['filter_prix_min'])
        list_param.append(session['filter_prix_max'])
        condition_and = " AND "
    if 'filter_types' in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "type_reparation_id=%s"
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)
    print(sql)
    mycursor.execute(sql, tuple_sql)
    print(tuple_sql)
    reparations = mycursor.fetchall()

    return render_template('reparation/front_reparation_filtre_show.html', types=typeReparation, reparations=reparations)


@app.route('/reparation/filtre', methods=['POST'])
def valid_filtre_reparation():
    filter_word = request.form.get('filter_word', None)
    filter_types = request.form.getlist('filter_types', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)

    if filter_word or filter_word == '':
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash('Le mot doit être composé de lettres uniquement')
        else:
            if len(filter_word) == 1:
                flash('Le mot doit contenir au moins 2 lettres')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash('Le prix minimum doit être inférieur au prix maximum')
        else:
            flash('Les prix doivent être des nombres entiers')
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types

    return redirect('/reparation/filtre')


@app.route('/reparation/filtre/suppr', methods=['POST'])
def reparation_suppr_filtre():
    session.pop('filter_word', None)
    session.pop('filter_types', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    return redirect('/reparation/filtre')


####################################################################

if __name__ == '__main__':
 app.run()