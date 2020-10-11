from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'el perro se llama manjar'
mysql = MySQL()
app.config['MYSQL_HOST'] = 'sebastianDuran.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'sebastianDuran'
app.config['MYSQL_PASSWORD'] = 'proyecto'
app.config['MYSQL_DB'] = 'sebastianDuran$default'
mysql.init_app(app)
cur = mysql.connect.cursor()

    #author
cur.execute('CREATE TABLE author (idAuthor INT  AUTO_INCREMENT , PRIMARY KEY (idAuthor), names VARCHAR(40) , lastnames VARCHAR(40), gradeAcademy VARCHAR(60), descripttion VARCHAR(200), contact VARCHAR (40)), photo BOOL DEFAULT 0;')

    #categories
cur.execute('CREATE TABLE category (idFilecategory INT  AUTO_INCREMENT , PRIMARY KEY (idFilecategory), nameCategory VARCHAR(25));')

    # noticias
cur.execute('CREATE TABLE noticias ( idnoticias INT  AUTO_INCREMENT , PRIMARY KEY (idnoticias), titlenoticias VARCHAR(180) , subtitlenoticias VARCHAR(200) , '
                       +'articlenoticias MEDIUMTEXT , dateTimenoticias DATETIME , dateTimenoticias_update DATETIME ,imagennoticias VARCHAR(180)  '
                        +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor)  , archiveTruenoticias BOOL DEFAULT 0 '
                      +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory)  );')

    # blog
cur.execute('CREATE TABLE blog ( idBlog INT  AUTO_INCREMENT , PRIMARY KEY (idBlog), titleBlog VARCHAR(180)  , subtitleBlog VARCHAR(200)  , '
                        +'articleBlog MEDIUMTEXT  , dateTimeBlog DATETIME, dateTimeBlog_update DATETIME,  imagenBlog VARCHAR(180)  '
                        +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTrueBlog BOOL DEFAULT 0'
                       +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')

    #proyectos
cur.execute('CREATE TABLE proyectos ( idproyectos INT  AUTO_INCREMENT , PRIMARY KEY (idproyectos), titleproyectos VARCHAR(180) , subtitleproyectos VARCHAR(200) , '
                        +'articleproyectos MEDIUMTEXT  , dateTimeproyectos DATETIME, dateTimeproyectos_update DATETIME,  imagenproyectos VARCHAR(180)  '
                       +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTrueproyectos BOOL DEFAULT 0'
                        +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')

    #mapass
cur.execute('CREATE TABLE mapas ( idmapas INT  AUTO_INCREMENT , PRIMARY KEY (idmapas), titlemapas VARCHAR(200) , subtitlemapas VARCHAR(200) , '
                         +'filemapas VARCHAR(200)  , dateTimemapas DATETIME, dateTimemapas_update DATETIME,  imagenmapas VARCHAR(200)  '
                        +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTruemapas BOOL DEFAULT 0'
                        +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')

    #monitoreos
cur.execute('CREATE TABLE monitoreos ( idmonitoreos INT  AUTO_INCREMENT , PRIMARY KEY (idmonitoreos), titlemonitoreos VARCHAR(180) , subtitlemonitoreos VARCHAR(200) , '
                         +'articlemonitoreos MEDIUMTEXT  , dateTimemonitoreos DATETIME, dateTimemonitoreos_update DATETIME,  imagenmonitoreos  VARCHAR(180)  '
                        +',idAuthor int, FOREIGN KEY (idAuthor) REFERENCES author(idAuthor) , archiveTruemonitoreos BOOL DEFAULT 0'
                        +',idFilecategory int, FOREIGN KEY (idFilecategory) REFERENCES category(idFilecategory));')




cur.close()
print("listo")
