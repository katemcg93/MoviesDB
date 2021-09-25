import pymysql
import moviesDB as mdb
from moviesDB import fullList
import sys
import pymongo
from pymongo.errors import DuplicateKeyError
import moviesAppMongo as mongo

#Need date time for one of the extra parts of the app
#Will ask for user's DOB, calculate age and feed back age-appropriate film recommendations
from datetime import datetime, date


def main ():
    def mainmenu ():
        print("Movies DB")
        print("-" * 9)

        print("Menu")
        print("="*4)

        print("1 - View Films")
        print("2 - View Actors by Year of Birth and Gender")
        print("3 - View Studios")
        print("4 - Add New Country")
        print("5 - View Movie with Subtitles")
        print("6 - Add new MovieScript")
        print("7 - Get Movie Recommendations")
        print("8 - View Oscar Winners by Decade")
        print("x - Exit application")

        choice = input("Choice: ")
        return choice

    choice = mainmenu()

    def viewfilms ():
        #This code is passing two arguments to the mdb view film function
        #l2 is limiting total results returned to 5
        #l1 is telling mySQL the position/row to start at in the film table
        #Every time the user presses enter, l1 is incremented by 5 to move through the table

        l1 = 0
        l2 = 5
        count = 0
        totalRows = fullList ()

        print("Films")
        print("-" * 5)
        mdb.get_actors(l1,l2)
            
        nextChoice = input("-- Quit <q> --")
        
        while nextChoice != "q":

            count = count + 5
            l1 = l1 +5
            l2 = 5

            mdb.get_actors(l1,l2)
        
            nextChoice = input("-- Quit <q> --")
            if nextChoice == "q":
                break

            #this code is to get Quit to keep showing up when the user reaches the end of the list
            #totalRows = function contained in the mdb file, will return count of rows in film table
            #Program keeps track of total rows returned in count variable
            #When value of count exceed the total rows of the films table, the below is shown to the user

            while count >= len(totalRows):
                nextChoice = input("-- Quit <q> --")
                if nextChoice == "q":
                   break
        
    def viewactors ():
        yr =input("Please enter a birth year: ")
        while True:
            try:
                y = int(yr)
            except ValueError as e:
                yr = input("Please enter a birth year :")
                
                #breaking out of while loop when user supplies a digit as input and converting to int for the SQL function
            if yr.isdigit ():
                y = int(yr)
                break
    
        g = input("Enter a Gender: ")

        while True: 
            #Checking if user has supplied a valid gender, until they do they will be asked to enter a value
            #converting the input to all lowercase and checking this to allow for users entering either upper or lower case

            lowerg = g.lower()
            if lowerg == "male" or lowerg == "female":
                mdb.get_birthmonth(g, y)
                break
            elif g.strip() == "":
                mdb.get_bm_both_genders(y)
                break               
            else:
                g = input("Enter a Gender")
    
    def view_studios ():
        mdb.get_studios ()
    
    def new_country ():
        countryid = input("ID: ")
        while True:
            try:
                cid = int(countryid)
            except ValueError as e:
                countryid = input ("ID:")
            if countryid.isdigit():
                cid = int(countryid)
                break

        name = input("Name: ")

        while name.strip () == "":
            name = input("Name: ")
        
        try:
            mdb.add_country(cid, name)
        except pymysql.err.IntegrityError as ie:
            print("ID or Country already exists")

    def view_subtitles ():
        while True:
                sub = input ("Enter subtitle language : ")

                #Using .strip function to allow for users clicking space bar and then pressing enter
                while sub.strip () == "":
                    sub = input("Enter subtitle language : ")
            
                else:
                    try:
                        print ("Movies with {} subtitles".format(sub.capitalize()))
                        print("-" * 9)
                        #Using capitalize function to handle users putting in incorrect case values
                        filmIds = mongo.get_film_ids(sub.capitalize())
                        mdb.get_subtitles(filmIds)
                        break

                    except pymysql.err.ProgrammingError as pe:
                        print("Invalid language selection {}".format(sub))

    def insert_script ():
        kwlist = []
        sblist = []

        fId = input("ID : ")

        while True:
            try:
                id = int(fId)
            except ValueError as e:
                fId = input("ID : ")
            if fId.isdigit():
                id = int(fId)
                break

        kw = input("Keyword < -1 to end >:")
        while kw != "-1":
            kwlist.append(kw)
            #print (kwlist)
            kw = input("Keyword < -1 to end >:")
        else:
            sb = input("Subtitle < -1 to end >:")
            while sb != "-1":
                sblist.append(sb)
                #print(sblist)
                sb = input("Subtitle < -1 to end >:")
            else:
                result = mdb.check_id(id)
                if result is None:
                    print("*** ERROR ***: Movie Script with ID : {} does not exist in moviesDB".format(str(id)))
                else:     
                    try:
                        mongo.insert_script(id,kwlist, sblist)

                    except DuplicateKeyError as dke:
                        print("*** Error ***: Movie Script with id : {} already exists".format(str(id)))

                    else:
                        print("New Script inserted")

    def movie_recs ():
        print("Please enter your date of birth (dd mm yyyy)")
        birth_date = datetime.strptime(input("--->"), "%d %m %Y")
        today = date.today()

        #Function to calculate user's DOB so the correct recommendations can be returned to them
        def calculate_age(birth_date):
            while True:
                    try:
                        #First part of code is subtracting current date from user's birthdate to get their age
                        # Second part is checking if current month is earlier than user's birth month, or if the months are equal but current date is before bday date
                        #If so, take a year off their age to get current age in years
                        y = today.year - birth_date.year
                        if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
                            y -= 1

                    except ValueError as e:
                        print("Invalid Date Format")
                        birth_date = datetime.strptime(input("Please Enter your date of birth (dd mm yyyy)"), "%d %m %Y")
                        y = today.year - birth_date.year

                    if str(y).isdigit():
                        break
            return y
        
        def choose_genre ():
            #Next part of code is asking user to choose a genre
            #Numbers here correspond to genre IDs on movie database
            #Can therefore feed the user input into the query to get age appropriate films of preferred genre
            print("Select one of the following genre options:")
            print("1: Action")
            print("2: Drama")
            print("3: Romantic")
            print("4: Comedy")
            print("5: Musical")
            print("6: Other")

            genre = input("--->")
            while int(genre) not in range(0,7):
                genre = input ("Please choose a valid option:")
            
            else:
                print("You have chosen {}".format(genre))
            
            return genre
       
        age_yrs = calculate_age(birth_date)
        genre = choose_genre()
        mdb.movie_recommendations(age_yrs, genre)


    def oscar_winners ():
        #This function asks users to choose a decade
        #Based on their option will feed back Oscar winners from that decade
        print("Choose a decade")
        print("1: 1970s")
        print("2: 1980s")
        print("3: 1990s")
        print("4: 2000s")
        print("5: 2010s")
        decade = input("--->")

        while int(decade) not in range(0,6):
            decade = input ("Please choose a valid option:")
            
        else:
            mdb.get_oscar_winners(decade)


        

        
    while choice != "x":
        if choice == "1":
            viewfilms()
            choice = mainmenu ()
        elif choice == "2":
            viewactors ()
            choice = mainmenu ()
        elif choice == "3":
            view_studios()
            choice = mainmenu ()
        elif choice == "4":
            new_country ()
            choice = mainmenu ()
        elif choice == "5":
            view_subtitles ()
            choice = mainmenu () 
        elif choice == "6":
            insert_script ()
            choice = mainmenu ()
        elif choice == "7":
            movie_recs()
            choice = mainmenu ()
        elif choice == "8":
            oscar_winners()
            choice = mainmenu()
        else:
            choice = mainmenu ()

    
    if choice == "x":
        sys.exit("Programme Terminated")
    

   


if __name__ == "__main__":
    main()