from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'el perro se llama manjar'
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'proyectoGeografia'

mysql.init_app(app)

@app.route('/', methods = ['POST','GET'])
def crearTablas():
    cur = mysql.connect.cursor()

    #author
    #cur.execute('CREATE TABLE author (idAuthor INT  AUTO_INCREMENT , PRIMARY KEY (idAuthor), names VARCHAR(40) , lastnames VARCHAR(40), gradeAcademy VARCHAR(60), descripttion VARCHAR(200), contact VARCHAR (40)), photo BOOL DEFAULT 0;')

    #categories
    #cur.execute('CREATE TABLE category (idFilecategory INT  AUTO_INCREMENT , PRIMARY KEY (idFilecategory), nameCategory VARCHAR(25));')

    # news
    #cur.execute('CREATE TABLE news ( idNews INT  AUTO_INCREMENT , PRIMARY KEY (idNews), titleNews VARCHAR(180) , subtitleNews VARCHAR(200) , '
    #                   +'articleNews MEDIUMTEXT , dateTimeNews DATETIME , dateTimeNews_update DATETIME ,imagenNews VARCHAR(180)  '
    #                    +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor)  , archiveTrueNews BOOL DEFAULT 0 '
    #                  +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory)  );')

    # blog
    #cur.execute('CREATE TABLE blog ( idBlog INT  AUTO_INCREMENT , PRIMARY KEY (idBlog), titleBlog VARCHAR(180)  , subtitleBlog VARCHAR(200)  , '
    #                    +'articleBlog MEDIUMTEXT  , dateTimeBlog DATETIME, dateTimeBlog_update DATETIME,  imagenBlog VARCHAR(180)  '
    #                    +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTrueBlog BOOL DEFAULT 0'
    #                   +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')

    #Project
    #cur.execute('CREATE TABLE projects ( idProject INT  AUTO_INCREMENT , PRIMARY KEY (idProject), titleProject VARCHAR(180) , subtitleProject VARCHAR(200) , '
    #                    +'articleProject MEDIUMTEXT  , dateTimeProject DATETIME, dateTimeProject_update DATETIME,  imagenProject VARCHAR(180)  '
    #                   +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTrueProject BOOL DEFAULT 0'
    #                    +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')

    #maps
    cur.execute('CREATE TABLE map ( idMap INT  AUTO_INCREMENT , PRIMARY KEY (idMap), titleMap VARCHAR(200) , subtitleMap VARCHAR(200) , '
                         +'fileMap VARCHAR(200)  , dateTimeMap DATETIME, dateTimeMap_update DATETIME,  imagenMap VARCHAR(200)  '
                        +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTrueMap BOOL DEFAULT 0'
                        +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')

    #monitoring
    #cur.execute('CREATE TABLE monitoring ( idMonitoring INT  AUTO_INCREMENT , PRIMARY KEY (idMonitoring), titleMonitoring VARCHAR(180) , subtitleMonitoring VARCHAR(200) , '
    #                     +'articleMonitoring MEDIUMTEXT  , dateTimeMonitoring DATETIME, dateTimeMonitoring_update DATETIME,  imagenMonitoring  VARCHAR(180)  '
    #                    +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTrueMonitoring BOOL DEFAULT 0'
    #                    +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')




    cur.close()
    return 'listo'


@app.route('/category', methods = ['POST','GET'])
def category():
    cur = mysql.connect.cursor()
    namesCategory = ['Arduino', 'Tutoriales', 'Raspberri Pi','Python','Qgis']
    for i in namesCategory:
        
        cur.execute('insert into category (nameCategory) VALUES(%s)',(i))
    mysql.connection.commit()
    cur.close()
    return 'listo categoria'

if __name__== '__main__':
    app.run(port = 2001, debug=True)