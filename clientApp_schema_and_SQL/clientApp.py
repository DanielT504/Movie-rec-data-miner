from mysql import connector

#change
DB_NAME = ''
DB_HOST = ''
DB_USER = ''
DB_PASSWORD = ''
connection = None
starting_id = 0

criteria_dict = {
    'T': "SELECT title, runtime, release_date FROM Movies WHERE title = 'X';",
    'A': """
        SELECT DISTINCT m.title, m.runtime, m.release_date
        FROM Movies m
        JOIN Credits c ON m.metadata_id = c.id
        WHERE c.cast LIKE "%'name': 'X'%";
        """,
    'D': """
        SELECT DISTINCT m.title, m.runtime, m.release_date
        FROM Movies m
        JOIN Credits c ON m.metadata_id = c.id
        WHERE c.crew LIKE "%'job': 'Director', 'name': 'X'%";
        """,
    'G': 'SELECT title, runtime, release_date FROM Movies WHERE genres LIKE "%X%";', 
    'R': "SELECT m.title, m.runtime, m.release_date FROM Movies m JOIN Links l ON m.imdb_id = l.imdb_id JOIN Ratings r ON l.movie_id = r.movie_id WHERE r.rating = X;",
    'Y': "SELECT title, runtime, release_date FROM Movies WHERE release_date LIKE 'X%';",
    'K': "SELECT m.title, m.runtime, m.release_date FROM Movies m JOIN Keywords k ON m.metadata_id = k.metadata_id WHERE k.keyword_value LIKE '%X%';",
    'RT': "SELECT title, runtime, release_date FROM Movies WHERE runtime = X;",
}

def connect_to_database():
    global connection
    try:
        connection = connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port = 3306
        )
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            return
    except connector.Error as e:
        print("Error while connecting to MySQL", e)


def print_sql_table(data):
    headers = ("Title", "Runtime", "Release Date")
    max_lengths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]

    def print_separator():
        print("+".join("-" * (length + 2) for length in max_lengths))

    print_separator()
    header = "| {:<{}} ".format(headers[0], max_lengths[0])
    header += "| {:>{}} ".format(headers[1], max_lengths[1])
    header += "| {:<{}} |".format(headers[2], max_lengths[2])
    print(header)
    print_separator()

    for row in data:
        row_str = "|" + "|".join(" {:<{}} ".format(str(item), max_lengths[i]) for i, item in enumerate(row))
        row_str += "|"
        print(row_str)
        print_separator()

def query_data():
    global connection
    print("Select what criteria you would like to search for")
    print("Enter criteria followed by value, ex. T Avatar")
    print("Title(T), Actor/Actress(A), Director(D), Genre(G), Rating(R), Release Year(Y), Keywords(K), Runtime(RT), Exit(E): ")
    user_input = input("").strip()

    criteria = user_input.split(" ")[0].upper()

    if (not criteria or criteria.upper() == 'E'):
        return
    
    if (len(user_input.split(" ")) < 2):
        print("The criteria or value was missing from the input. Please ensure there is a space between the criteria and the value")
        query_data()

    query = criteria_dict[criteria].replace("X", user_input[len(criteria)+1:])
    cursor = connection.cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    if output:
        print_sql_table(output)
    else:
        print("No movies found matching the given criteria")

def modify_data():
    global connection, starting_userid
    print("Choose to add/edit a review(R), add a movie(M), or exit(E): ")
    user_input = input().strip()

    if user_input.upper() == 'R':
        print("Enter the movie title and your rating (0-5), ex. Avatar 4.5")
        print("If you've already reviewed this movie this will update it")
        rating_data = input().strip()
        rating = rating_data.split(" ")[-1]
        title = rating_data[:-len(rating)].strip()
        cursor = connection.cursor()
        cursor.execute(f"SELECT metadata_id, imdb_id FROM Movies WHERE title = '{title}';")
        metadata_id, imdb_id = cursor.fetchone()
        cursor.execute(f"SELECT movie_id FROM Links WHERE imdb_id = '{imdb_id}';")
        movie_id = cursor.fetchone()
        if movie_id:
            movie_id = movie_id[0]
        if metadata_id:
            query = """
            INSERT INTO Ratings (user_id, movie_id, rating)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE rating = VALUES(rating)
            """
            cursor.execute(query, (int(starting_id), int(movie_id), float(rating)))
            query = """
            INSERT INTO Links (movie_id, imdb_id, metadata_id)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY update movie_id = VALUES(movie_id)
            """
            cursor.execute(query, (int(movie_id), imdb_id, int(metadata_id)))
            print(f"Added review for {title}")
        else:
            print(f"'{title} not found'")
        connection.commit() 
        cursor.close()
    elif user_input.upper() == 'M':
        movie_data_list = []
        while True:
            print("Enter Movie title, overview, runtime(minutes), and release date(YYYY-MM-DD) in a comma seperated list")
            print("Ex. Avatar, blue people in the forest, 162, 2009-12-10")
            movie_data = input().strip()
            movie_data_list = movie_data.split(",")

            if len(movie_data_list) == 4:
                break
            else:
                print("Required data missing")
        
        title, overview, runtime, date = movie_data_list

        print("Additional data can be entered in a comma seperated list in the following order (N/A to ignore value | 'skip' to skip)")
        print("genres(wrapped in []), tagline, imdb_id")
        print("Ex. [Action | Adventure | Fantasy], Discover a new world, tt0114709")
        bonus_movie_data = input().strip()
        genres = ''
        tagline = ''
        imdb_id = ''
        if bonus_movie_data.lower() != 'skip':
            genres, tagline, imdb_id = bonus_movie_data.split(",")
        cursor = connection.cursor()
        query = """
        INSERT INTO Movies (imdb_id, title, release_date, genres, 
                        runtime, tagline, overview)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (imdb_id.strip(), title.strip(), date.strip(), genres.strip(),runtime, tagline.strip(), overview.strip()))
        print(f"{title} added!")
        connection.commit()
    elif user_input == 'E':
        return
    else: 
        print("Invalid option try 'R', 'M', or 'E'")
        modify_data()

def set_max_movie_id():
    global starting_id, connection
    if connection.is_connected():
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(metadata_id) FROM Movies;")        
        result = cursor.fetchone()
        if result and result[0] is not None:
            starting_id = result[0] + 1;
        else:
            print("No records in the table or no value in the 'movie_id' column.")

        cursor.close()

def main():
    global connection
    print("Project Client Application")

    connect_to_database()
    if connection:
        set_max_movie_id()
        
        while True:
            user_input = input("Enter a command ('query', 'modify', or 'exit'): ").strip().lower()
            if user_input == 'exit':
                break
            if user_input == 'query':
                query_data()
            elif user_input == 'modify':
                modify_data()
            else:
                print("Unknown command, try 'query' or 'modify'")

if __name__ == "__main__":
    main()
