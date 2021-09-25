import pymysql
import pymysql.cursors
import pymongo
import moviesAppMongo
from datetime import datetime, date


def connect():
    global conn
    conn = pymysql.connect(host='localhost', user='root', password='root', database='moviesDB', autocommit = True, cursorclass=pymysql.cursors.DictCursor)
    return conn

conn = connect()

def fullList ():

    query = """SELECT f.FilmName, a.actorName FROM film f 
               inner join filmcast fc on f.filmID = fc.CastFilmID
               INNER JOIN actor a on fc.CastActorID = a.ActorID;
                """

    conn = connect ()
    cursor = conn.cursor() 
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def get_actors (l1, l2):
    conn = connect()

    query = """SELECT f.FilmName, a.actorName FROM film f 
               inner join filmcast fc on f.filmID = fc.CastFilmID
               INNER JOIN actor a on fc.CastActorID = a.ActorID 
               order by f.filmName asc, a.actorName asc
               limit %s, %s;"""

    with conn:

        try:
            cursor = conn.cursor()

        except pymysql.err.Error as e:
            cursor = conn.cursor()

        cursor.execute(query, (l1,l2))
        results = cursor.fetchall()

        for r in results:
            print(r["FilmName"], "\t : \t", r["actorName"])
  

def get_birthmonth(g, y): 

    conn = connect()

    query = """SELECT ActorName, ActorGender, monthname(ActorDOB) AS "Birth Month"
               FROM actor WHERE ActorGender = %s AND year(ActorDOB) = %s; """
    
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, (g,y))
        results = cursor.fetchall()
        for r in results:
            print(r["ActorName"].ljust(20) + ":"+ r["ActorGender"].center(10) +":".center(5) + r["Birth Month"].ljust(5))

def get_bm_both_genders(y): 

    conn = connect()

    query = """SELECT ActorName, ActorGender, monthname(ActorDOB) AS "Birth Month"
               FROM actor WHERE year(ActorDOB) = %s; """
    
    with conn:
        cursor = conn.cursor()
        cursor.execute(query, (y))
        results = cursor.fetchall()
        for r in results:
            print(r["ActorName"].ljust(20) + ":"+ r["ActorGender"].center(10) +":".center(5) + r["Birth Month"].ljust(5))

firstTime = True
studioList = []  

def get_studios ():
    #Once this function has been ran once, firstTime is set to false
    #Any time this function is called thereafter it will skip to line 106 and just print the studioList
    global firstTime
    global studioList
    if firstTime == True:
        conn = connect()

        query = """ SELECT StudioID, StudioName
                    FROM studio
                    ORDER BY StudioID asc; """

        with conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            #print("first time")
            for r in results:
                print(str(r["StudioID"]).ljust(1 )+ ":".center(5) + r["StudioName"].ljust(5))
                studioList.append(r)
        firstTime = False
    
    else:
        for studio in studioList:
            print(str(studio["StudioID"]).ljust(1 )+ ":".center(5) + studio["StudioName"].ljust(5))

            

        
def add_country (cid, name):
    
    conn = connect ()

    sql = "INSERT INTO country VALUES (%s, %s); "
    
    with conn:
        cursor = conn.cursor ()
        cursor.execute(sql, (cid, name))


def get_subtitles (filmIds):

    conn = connect ()

    params = ",".join(['%s']* len(filmIds))

    query = "select filmName,  substring(filmSynopsis, 1, 30) as Description from film where filmID in (%s)" %params

    with conn:
        cursor = conn.cursor ()
        cursor.execute (query, filmIds)
        results = cursor.fetchall ()
        for r in results:
            print(str(r["filmName"]).ljust(1 )+ ":".center(5) + r["Description"].ljust(5))

def check_id (id):

    conn = connect ()

    query = "select filmID from film where filmID in (%s) "

    with conn:
        cursor = conn.cursor ()
        cursor.execute (query, id)
        result = cursor.fetchone ()

    return result
    

def movie_recommendations(age_yrs, genre):
    conn = connect ()
    if age_yrs <12:
        query = "select f.filmname, c.certificateID, c.certificate, g.genrename from film f inner join certificate c on f.filmCertificateID = c.CertificateID inner join genre g on g.genreID = f.filmGenreID where c.certificateID <3 and g.genreID = %s order by certificateID"
    elif age_yrs >= 12 and age_yrs <15:
        query = "select f.filmname, c.certificateID, c.certificate, g.genrename from film f inner join certificate c on f.filmCertificateID = c.CertificateID inner join genre g on g.genreID = f.filmGenreID  where c.certificateID <5 and g.genreID = %s order by certificateID"
    elif age_yrs >=15 and age_yrs <18:
        query = "select f.filmname, c.certificateID, c.certificate,g.genrename from film f inner join certificate c on f.filmCertificateID = c.CertificateID inner join genre g on g.genreID = f.filmGenreID where c.certificateID <6 and g.genreID = %s order by certificateID"
    else:
        query = "select f.filmname, c.certificateID, c.certificate, g.genrename from film f  inner join certificate c on f.filmCertificateID = c.CertificateID inner join genre g on g.genreID = f.filmGenreID where g.genreID = %s order by certificateID"

    with conn:
        cursor = conn.cursor ()
        cursor.execute (query, genre)
        results = cursor.fetchall ()
        for r in results:
            print(str(r["filmname"]).ljust(1 )+ ":".center(5) + r["certificate"].ljust(5)+ ":" +r["genrename"])

    return results



def get_oscar_winners (decade):
    
    conn = connect ()
    if decade == "1":
        yr1 = "1970"
        yr2 = "1979"
    elif decade == "2":
        yr1 = "1980"
        yr2 = "1989"
    elif decade == "3":
        yr1 = "1990"
        yr2 = "1999"
    elif decade == "4":
        yr1 = "2000"
        yr2 = "2009"
    elif decade == "5":
        yr1 = "2010"
        yr2 = "2019"
    
   

    query = "select filmName, year(filmReleaseDate), c.CountryName, d.directorName, s.StudioName, filmOscarWins from film f inner join country c on f.filmcountryid = c.countryid inner join director d on f.filmdirectorid = d.directorId inner join studio s on f.FilmStudioID = s.studioid where year(filmReleaseDate) between %s and %s and filmOscarWins >0;"

    with conn:
        cursor = conn.cursor ()
        cursor.execute (query, (yr1, yr2))
        results = cursor.fetchall ()
        for r in results:
            print(str(r["filmName"]).ljust(1 )+ " : ".center(5) + str(r["year(filmReleaseDate)"])+ " : " +r["CountryName"]+ " : " +r["directorName"] + " : " +r["StudioName"] + " : " +str(r["filmOscarWins"]) + "  Oscars")
    
        








        
     

