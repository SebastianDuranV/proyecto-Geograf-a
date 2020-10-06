import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import datetime
import zipfile


"""
    Tareas a realizar en servidor:
        -Rastreador de país de origen de ip 
        -Buscador
        -Autenticación para editar, crear y eliminar datos.
        -Terminar de pulir el sistema de subida de archivos. (ZIP)
"""


app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'el perro se llama manjar'
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'proyectoGeografia'



mysql.init_app(app)



def extractallZip(directory, namefile):
    fantasy_zip = zipfile.ZipFile(directory + '/' + namefile)
    fantasy_zip.extractall(directory) 
    fantasy_zip.close()
    os.remove(directory + '/' + namefile)
     


##   i   n   d   e   x -----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administrador')
def adminLogin():
    return render_template('Admin.html')

@app.route('/administrador/lista',methods = ['POST'])
def admnin():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('select contraseña from administrador;')
        password = cur.fetchall()
        entry = request.form['password']
        if entry == password[0][0]:
            return redirect(url_for('listContend'))
        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('adminLogin'))


@app.route('/administrador',methods = ['GET'], defaults={'post_id': None})
@app.route('/administrador/lista',methods = ['GET'])
def listContend():
    return render_template('new/author/newAuthor.html')


#####   A   U   T   O   R   ######  

@app.route('/new/author')
def newAuthor():
    return render_template('new/author/newAuthor.html')


@app.route('/list/author')
def listAuthor():
    cur = mysql.connection.cursor()
    cur.execute('select * from author;')
    authors = cur.fetchall()
    return render_template('new/author/deleteEditAuthor.html', data = authors)


@app.route('/edit/author/<idAuthor>')
def editAuthor(idAuthor):
    cur = mysql.connection.cursor()
    cur.execute('select * from author where idAuthor = ' +idAuthor)
    author = cur.fetchall()
    print(author)
    return render_template('new/author/editAuthor.html', data = author)


@app.route('/delete/author/<idAuthor>')
def deleteAuthor(idAuthor):
    cur = mysql.connection.cursor()
    cur.execute('delete from author where idAuthor = ' + idAuthor)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("listAuthor"))
    
    

@app.route('/update/add_author/<idAuthor>', methods = ['POST'])
def updateAuthor(idAuthor):
    if request.method == 'POST':
        names = request.form['names']
        lastname = request.form['lastnames']
        gradeAcademy = request.form['gradeAcademy'] 
        descripttion = request.form['descripttion']
        contact = request.form['contact']
        
        if request.files['photo']:
            photo = 1 # 1 : hay foto
                      # 0 : no hay foto 
        else:
            photo = 0

        # Agregar foto
        try:
            cur = mysql.connection.cursor()
            cur.execute('update author set (names,lastnames, gradeAcademy, descripttion,contact,photo)'
                        +' VALUES(%s,%s,%s,%s,%s,%s) where idAuthor = %s',(names, lastname, gradeAcademy,descripttion,contact,photo,idAuthor))
            mysql.connection.commit()
        except:
            flash("El autor no fue editado exitosamente, asegurese de que ingresó todos los datos.")
            return redirect(url_for('listAuthor'))

        if request.files['photo']:
            cur.execute('SELECT * FROM author WHERE names = %s AND  lastnames'
                        +'= %s' ,(names, lastname))
            data = cur.fetchall()
            cur.close()
        
            directory = os.path.join('./static/uploaders/author', str(data[0][0]))
            os.mkdir(directory)
            app.config['UPLOAD_FOLDER'] = "./static/uploaders/author/"+ str(data[0][0])
            f = request.files['photo']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash("El autor fue editado exitosamente")
        return redirect(url_for('listAuthor'))



@app.route('/new/add_author', methods = ['POST'])
def addAuthor():
    if request.method == 'POST':
        names = request.form['names']
        lastname = request.form['lastnames']
        gradeAcademy = request.form['gradeAcademy'] 
        descripttion = request.form['descripttion']
        contact = request.form['contact']
        
        if request.files['photo']:
            photo = 1 # 1 : hay foto
                      # 0 : no hay foto 
        else:
            photo = 0

        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO author (names,lastnames, gradeAcademy, descripttion,contact,photo)'
                        +' VALUES(%s,%s,%s,%s,%s,%s)',(names, lastname, gradeAcademy,descripttion,contact,photo))
            mysql.connection.commit()
        except:
            flash("El autor no fue añadido exitosamente, asegurese de que ingresó todos los datos.")
            return redirect(url_for('newAuthor'))

        if request.files['photo']:
            cur.execute('SELECT * FROM author WHERE names = %s AND  lastnames'
                        +'= %s' ,(names, lastname))
            data = cur.fetchall()
            cur.close()
            directory = os.path.join('./static/uploaders/author', str(data[0][0]))
            os.mkdir(directory)
            app.config['UPLOAD_FOLDER'] = "./static/uploaders/author/"+ str(data[0][0])
            f = request.files['photo']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash("El autor fue añadido exitosamente")
        return redirect(url_for('newAuthor'))



######   C   O   N   T   E   N   I   D   O   :::::: ######  

@app.route('/<types>')
def getListOfType(types):
    cur = mysql.connect.cursor()
    try:
        cur.execute('SELECT ' + types + '.*, author.names, author.lastNames FROM ' + types 
                    + ' LEFT JOIN author  ON ' + types + '.idAuthor = author.idAuthor;')
    except:
        return '<h2> NOT FOUND 404 <h2>'
    data = cur.fetchall()
    print(data)

    cur.execute('select  nameCategory from category')
    category = cur.fetchall()
    print(category)

    cur.close()
    return render_template("news/listNews.html", manyNews = data , type = types,  category=category)


@app.route('/<types>/<idType>')
def getOneType(types,idType):
    cur = mysql.connect.cursor()
    cur.execute('SELECT * FROM '+ types +' WHERE id'+ types.capitalize() +' =' + idType)
    data = cur.fetchall()
    cur.close()
    if data:
        return render_template('news/oneNews.html', date = data, type = types, id = idType)
    else:
        return "<h2>NOT FOUND</h2>"


@app.route('/new/<nameType>')
def newRegisterType(nameType):
    cur = mysql.connect.cursor()
    try:
        cur.execute('select * from '+ nameType + ' limit 1;')
    except:
        return '<h2> NOT FOUND 404 : name type not found  <h2>'

    # extraer autores
    cur.execute('select  idAuthor, names, lastnames from author')
    authores = cur.fetchall()
    cur.execute('select  idFilecategory, nameCategory from category')
    category = cur.fetchall()
    cur.close()
    #num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    #print(field_names)
    return render_template('new/newNews.html', type = nameType 
            ,description = field_names, authores=authores, category=category)


@app.route('/new/add_<types>', methods = ['POST','GET'])
def addRegisterType(types):
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        if request.form['article']:
            article = request.form['article']
        else:
            article = None
        idAutor = request.form.get('autor')
        idCategory = request.form.get('category')
        if request.form['Imagen-url']:
            imagen = request.form['Imagen-url']
        else:
            imagen = None

        cur = mysql.connection.cursor()
        if types != "map":
            cur.execute('INSERT INTO '+ types + ' (title'+ types +',subtitle'+ types 
                        +'article'+ types +', idAuthor , dateTime'+ types +', dateTime'+ types +'_update,idFilecategory, imagen'+ types +')'
                        +' VALUES(%s,%s,%s,%s,NOW(),NOW(),%s,%s)',(title, subtitle,article, idAutor,idCategory,imagen))
        else:
            cur.execute('INSERT INTO map (titlemap,subtitlemap, filemap'
                    + ', idAuthor , dateTimemap, dateTimemap_update,idFilecategory, imagenmap)'
                    +' VALUES(%s,%s,%s,%s,NOW(),NOW(),%s,%s)',(title, subtitle, article,idAutor,idCategory,imagen))

        # Subir archivos
        if request.files['files']:
            # Cambiar esto::
            cur.execute('SELECT * FROM '+ types + ' WHERE title'+ types +' = %s AND  subtitle'
                        + types +' = %s' ,(title, subtitle))
            data = cur.fetchall()
            #print(data[0][0])
            cur.close()
        
            #directory = os.path.join('./static/uploaders/' + types, str(data[0][0]))
            directory = './static/uploaders/' + types+'/' + str(data[0][0])
            print(directory)
            os.mkdir(directory)
        
            app.config['UPLOAD_FOLDER'] = "./static/uploaders/" + types +'/'+ str(data[0][0])
            f = request.files['files']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            directory = "./static/uploaders/" + types +'/'+ str(data[0][0])
            extractallZip(directory, filename)
        mysql.connection.commit()
        flash(types +" added succesfully")
        if types == "map" :

            cur = mysql.connection.cursor()
            cur.execute('SELECT idMap FROM '+ types + ' WHERE title'+ types +' = %s AND  subtitle'
                        + types +' = %s' ,(title, subtitle))
            idMap = cur.fetchall()
            cur.close()
            return redirect(url_for('edit',nameType=types,id=idMap))
        return redirect(url_for('newRegisterType',nameType=types ))


@app.route('/deleteEdit/<nameTypes>')
def deleteEdit(nameTypes):
    try:
        cur = mysql.connection.cursor()
        cur.execute('select * from '+ nameTypes)
        data = cur.fetchall()
    except:
        return '<h2> NOT FOUND 404 : name type not found  <h2>'
    return render_template('deleteEdit.html', nameType = nameTypes, data=data)

@app.route('/delete/<nameType>/<id>')
def delete(nameType,id):
    cur = mysql.connection.cursor()
    cur.execute('delete from '+ nameType +' where id'+ nameType +' = ' + str(id))
    directory = "./static/uploaders/" + nameType +'/' + str(id)
    #os.rmdir(directory)
    try:
        os.chmod (directory, 777)
        os.remove(directory)
    except:
        print("no archivo")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("deleteEdit" , nameTypes = nameType))


@app.route('/edit/<nameType>/<id>')
def edit(nameType,id):
    cur = mysql.connection.cursor()
    cur.execute('select * from '+ nameType +' where id'+ nameType +' = ' + str(id))
    data = cur.fetchall()
    #print(data[0])
    cur.close()
    # return render_template('edit.html', type = nameType, data=data[0])
    cur = mysql.connection.cursor()
    cur.execute('select  idAuthor, names, lastnames from author')
    authores = cur.fetchall()
    cur.execute('select  idFilecategory, nameCategory from category')
    category = cur.fetchall()
    cur.close()
    #num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    #print(field_names)
    return render_template('edit.html', type = nameType , data=data[0]
            ,description = field_names, authores=authores, category=category)


@app.route('/update/<types>/<idA>',methods = ['POST'])
def update(types,idA):
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        article = request.form['article']
        imagen = request.form['Imagen-url']
        idAutor = request.form.get('autor')
        idCategory = request.form.get('category')
        cur = mysql.connection.cursor()
        #  idCategory
        types = types[1::]
        if types != "map":
            cur.execute('update '+ types + ' set title'+ types +' = %s,subtitle'
                        + types +' = %s, idAuthor = %s , dateTime'+ types +', dateTime'+ types +'_update = NOW(), idFilecategory = %s, imagen'+ types +' = %s'
                        ,(title, subtitle, idAutor,idCategory,imagen))
        else:
            cur.execute('update map set titlemap = %s , subtitlemap = %s, filemap = %s'
                    + ', idAuthor = %s , dateTimemap_update = NOW(),idFilecategory = %s, imagenmap = %s'
                    ,(title, subtitle, article,idAutor,idCategory,imagen))
        
        if request.files['files']:
            # Cambiar esto::
            cur.execute('SELECT * FROM '+ types + ' WHERE title'+ types +' = %s AND  subtitle'
                        + types +' = %s' ,(title, subtitle))
            data = cur.fetchall()
            cur.close()
            try:
                os.remove( './static/uploaders/' + types+'/' + str(data[0][0]))
            except:
                print("No encontrado")
            # directory = os.path.join('./static/uploaders/' + types, str(data[0][0]))
            directory = './static/uploaders/' + types+'/' + str(data[0][0])
            try:
                os.mkdir(directory)
            except:
                print("Carpeta creada")
            
            app.config['UPLOAD_FOLDER'] = "./static/uploaders/" + types +'/'+ str(data[0][0])
            f = request.files['files']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            directory = "./static/uploaders/" + types +'/'+ str(data[0][0])
            extractallZip(directory, filename)
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("deleteEdit" , nameTypes = types))


#### Buscador
@app.route('/search')
def search():
    searchWords = request.form['searchWords']
    


if __name__== '__main__':
    app.run(port = 2000, debug=True)