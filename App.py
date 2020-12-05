import os
from flask import Flask, request, redirect, url_for, render_template, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'el perro se llama manjar'
mysql = MySQL()
#app.config['MYSQL_HOST'] = 'sebastianDuran.mysql.pythonanywhere-services.com'
#app.config['MYSQL_USER'] = 'sebastianDuran'
#app.config['MYSQL_PASSWORD'] = 'proyecto'
#app.config['MYSQL_DB'] = 'sebastianDuran$default'

#app.config['MYSQL_HOST'] = 'iribarrenp.mysql.pythonanywhere-services.com'
#app.config['MYSQL_USER'] = 'iribarrenp'
#app.config['MYSQL_PASSWORD'] = 'nuevositio'
#app.config['MYSQL_DB'] = 'iribarrenp$proyectoGeografia'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'proyectoGeografia'


password = 'password'

mysql.init_app(app)



def extractallZip(directory, namefile):
    fantasy_zip = zipfile.ZipFile(directory + '/' + namefile)
    fantasy_zip.extractall(directory)
    fantasy_zip.close()
    os.remove(directory + '/' + namefile)

@app.route('/login')
def login():
    return render_template('Admin.html')

@app.route('/loading',methods = ['POST','GET'])
def loadingLogin():
     correct = False
     if request.method == 'POST':
        try:
            entry = request.form['password']
        except:
            flash("Contraseña incorrecta")
            return redirect(url_for("login"))
        if entry == password:
            correct = True
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO ip (ipName) values(%s);', [request.remote_addr])
            mysql.connection.commit()
            cur.close()
            return render_template('option.html')
        flash("Contraseña incorrecta")
        return redirect(url_for("login"))
     else:
        if correct:
            return render_template('option.html')
        else:
            return redirect(url_for("login"))

def comprobation():
    cur = mysql.connection.cursor()
    cur.execute('select ipName from ip;')
    ips = cur.fetchall()
    cur.close()
    ips = (str(ips))
    return request.remote_addr in ips

##   i   n   d   e   x -----

@app.route('/')
def index():
    return render_template('index.html')

#####   A   U   T   O   R   ######

@app.route('/new/author',methods = ['POST','GET'])
def newAuthor():
    if comprobation():
        return render_template('new/author/newAuthor.html')
    return redirect(url_for("login"))



@app.route('/list/author', methods = ['POST','GET'])
def listAuthor():
    if comprobation():
        correct = True
        cur = mysql.connection.cursor()
        cur.execute('select * from author;')
        authors = cur.fetchall()
        return render_template('new/author/deleteEditAuthor.html', data = authors)
    return redirect(url_for("login"))



@app.route('/edit/author/<idAuthor>')
def editAuthor(idAuthor):
    if comprobation():
        cur = mysql.connection.cursor()
        cur.execute('select * from author where idAuthor = ' +idAuthor)
        author = cur.fetchall()
        return render_template('new/author/editAuthor.html', data = author)
    return redirect(url_for("login"))


@app.route('/delete/author/<idAuthor>')
def deleteAuthor(idAuthor):
    if comprobation():
        cur = mysql.connection.cursor()
        cur.execute('delete from author where idAuthor = ' + idAuthor)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("listAuthor"))
    return redirect(url_for("login"))



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

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO author (names,lastnames, gradeAcademy, descripttion,contact)'
                       +' VALUES(%s,%s,%s,%s,%s)',(names, lastname, gradeAcademy,descripttion,contact))
        mysql.connection.commit()

        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO author (names,lastnames, gradeAcademy, descripttion,contact)'
                        +' VALUES(%s,%s,%s,%s,%s)',(names, lastname, gradeAcademy,descripttion,contact))
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
                    + ' LEFT JOIN author  ON ' + types + '.idAuthor = author.idAuthor ORDER BY dateTime' + types + '_update DESC; ')
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
    cur.execute('SELECT * FROM '+ types +' WHERE id'+ types.capitalize() +'=' + idType + ';')
    data = cur.fetchall()
    cur.execute('SELECT id'+ types +' FROM '+ types)
    otherData = cur.fetchall()
    if data:
        i = 0
        while str(otherData[i][0]) != idType and i<len(otherData):
            i += 1
        other = []
        if i == 0 :
            other.append(" ")
        else:
            other.append(otherData[i-1])
        try:
            other.append(otherData[i+1])
        except:
            other.append(" ")
        return render_template('news/oneNews.html', date = data, type = types, id = idType, otherData=other)

    else:
        return "<h2>NOT FOUND</h2>"


@app.route('/new/<nameType>')
def newRegisterType(nameType):
    if comprobation():
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
    return redirect(url_for("login"))

@app.route('/new/add_<types>', methods = ['POST'])
def addRegisterType(types):
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        if request.form['article']:
            article = request.form['article']
        else:
            article = None
        idAutor = request.form.get('autor')
        try:
            idCategory = request.form.get('category')
        except:
            print("no categoria")

        if request.form['Imagen-url']:
            imagen = request.form['Imagen-url']
        else:
            imagen = None

        try:
            cur = mysql.connection.cursor()
            if types == "blog":
                cur.execute('INSERT INTO '+ types +' VALUES(NULL,%s,%s,%s,NOW(),NOW(),%s,%s,%s)',(title, subtitle,article,imagen, idAutor,idCategory))
            else:
                cur.execute('INSERT INTO '+ types +' VALUES(NULL,%s,%s,%s,NOW(),NOW(),%s,%s)',(title, subtitle,article,imagen, idAutor))
        except:
            return"no insertado "

        # Subir archivos
        if request.files['files']:
            # Cambiar esto::
            cur.execute('SELECT * FROM '+ types + ' WHERE title'+ types +' = %s AND  subtitle'
                        + types +' = %s' ,(title, subtitle))
            data = cur.fetchall()
            #print(data[0][0])
            cur.close()

            directory = os.path.join('./proyecto-Geograf-a/static/uploaders/' + types, str(data[0][0]))
            #directory = './static/uploaders/' + types+'/' + str(data[0][0])

            try:
                os.makedirs(directory)
            except:
                return "no se pudo crear archivo" + directory

            app.config['UPLOAD_FOLDER'] = "./proyecto-Geograf-a/static/uploaders/" + types +'/'+ str(data[0][0])
            f = request.files['files']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            directory = "./proyecto-Geograf-a/static/uploaders/" + types +'/'+ str(data[0][0])
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
    if comprobation():
        try:
            cur = mysql.connection.cursor()
            cur.execute('select * from '+ nameTypes)
            data = cur.fetchall()
        except:
            return '<h2> NOT FOUND 404 : name type not found  <h2>'
        return render_template('deleteEdit.html', nameType = nameTypes, data=data)
    return redirect(url_for("login"))

@app.route('/delete/<nameType>/<id>')
def delete(nameType,id):
    if comprobation():
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
    return redirect(url_for("login"))

@app.route('/edit/<nameType>/<id>')
def edit(nameType,id):
    if comprobation():
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
    return redirect(url_for("login"))

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
        try:
            if types != "mapas":
                cur.execute('update '+ types + ' set title'+ types +' = %s,subtitle'+ types + ' = %s,article'
                            + types +' = %s, idAuthor = %s , dateTime'+ types +'_update = NOW(), imagen'+ types +' = %s'
                            ,(title, subtitle,article, idAutor,imagen))
            elif types == "blog":
                cur.execute('update blog set titleblog = %s,subtitleblog = %s,articleblog = %s, idAuthor = %s , dateTimeblog_update = NOW(), imagenblog = %s, idFilecategory = %s'
                            ,(title, subtitle,article, idAutor,imagen,idCategory))
            else:
                cur.execute('update mapas set titlemapas = %s , subtitlemapas = %s, filemapas = %s'
                        + ', idAuthor = %s , dateTimemapas_update = NOW(),idFilecategory = %s, imagenmapas = %s'
                        ,(title, subtitle, article,idAutor,idCategory,imagen))
        except:
            return "no se ha podido actualizar." + types

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
                os.makedirs(directory)
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
@app.route('/search',methods = ['POST','GET'])
def search():
    if request.method == 'POST':
        searchWords = request.form['search']
        search = searchWords.split()
        cur = mysql.connection.cursor()
        types =["noticias","blog","mapas","proyectos","monitoreos"]
        listFile = []
        for k in types:
            cur.execute("select * from " + k + " LEFT JOIN author ON " + k + ".idAuthor = author.idAuthor;")
            listType = cur.fetchall()
            listType = list(listType)
            for i in listType:
                exist = True
                j = 0
                while j < len(search) and exist:
                    if not search[j] in (i[1] + " " + i[2] + " " + i[3]):
                        exist = False
                    j += 1
                if exist :
                    f = []
                    for p in i:
                        f.append(p)
                    f.append(k)
                    listFile.append(f)
    return render_template("search.html", manyNews = listFile , type = (),  category=())



if __name__=='__main__':
    app.run(port = 2000, debug=True)