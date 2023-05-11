

def getFilms(conn, curs):

    mysql_query = """
            SELECT * FROM Film
                """
    curs.execute(mysql_query) #execution de la requete
    films = curs.fetchall() #renvoie des resulats

    resultat = {}

    resultat["data"] = []#creation de la clé et de la liste qui va contenur chaque film. Il faut creer cette liste, car il y a plusieurs films

    for film in films:
        dico = {} #dictionnaire
        dico["id"] = film[0]
        dico["title"] = film[1]

        resultat["data"].append(dico)

    return resultat



#print(getFilms(connection,cursor))


def get_fav_films(conn, curs, user):
    mysql_query = """
                  SELECT User.*, Film.*
                  FROM Film, Film_User_Aime_Jointure, User
                  WHERE Film.IdFilm = Film_User_Aime_Jointure.IdFilm 
                        AND Film_User_Aime_Jointure.IdUser = User.IdUser 
                        AND User.Name = %s
                  """

    curs.execute(mysql_query, (user,))  # exécution de la requête
    films = curs.fetchall()  # renvoie des résultats

    resultat = {}  # création de la dictionnaire

    resultat["data"] = []  # création du clé et de la liste qui va contenir chaque film
    # il faut créer cette liste, car il y a plusieurs films

    for film in films:
        dico = {}  # dictionnaire pour un film
        dico["film_infos"] = {}  # la valeur pour la clé film_infos sera une autre dictionnaire
        dico["film_infos"]["id"] = film[-2]  # 2ème avant la fin
        dico["film_infos"]["title"] = film[-1]  # dernier élément de la liste
        dico["user_infos"] = {}
        dico["user_infos"]["id"] = film[0]
        dico["user_infos"]["name"] = film[1]
        dico["user_infos"]["birthdate"] = film[2]
        dico["user_infos"]["address"] = film[3]
        dico["user_infos"]["phone_number"] = film[4]

        resultat["data"].append(dico)  # ajouter dans la liste

    return resultat


#print(get_fav_films(connection, cursor, "Bob"))


def get_user_info(conn, curs, user):
    mysql_query = """
                      SELECT *
                      FROM User
                      WHERE Name = %s
                      """

    mysql_query2= """SELECT * 
                        FROM User
                        """
    curs.execute(mysql_query, (user,))  # exécution de la requête
    user_data = curs.fetchall()  # renvoie des résultats


    resultat = {}  # création de la dictionnaire

    resultat["id"] = user_data[0][0] # le résultat est une ligne suelement, donc il faut prendre le tuple de la 0ème ligne
    resultat["name"] = user_data[0][1]
    resultat["birthdate"] = user_data[0][2]
    resultat["address"] = user_data[0][3]
    resultat["phone_number"] = user_data[0][4]

    return resultat

#print(get_user_info(connection, cursor, "Bob"))

