import sys
#print(sys.version)
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sqlalchemy import create_engine
import urllib.parse
from sqlalchemy import text

# Use a db created according to populateData.sql and schema.txt
# e.g. (obsolete credentials):
# 'db356_team04'
# 'riku.shoshin.uwaterloo.ca'
# 'dthero'
# 'dbubYnn3A%%eapZAmL%2'
DB_NAME = ''
DB_HOST = ''
DB_USER = ''
DB_PASSWORD = ''
DB_PORT = 3306

def connect_to_database():
    try:
        encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
        engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        print(f"Connected to database: {engine}")
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def fetch_data():
    engine = connect_to_database()
     
    if engine is not None:
        #print("engine succesfully obtained from database connection!")
        #query = text("SELECT * FROM Movies")
        query = text("SELECT * FROM MojoBudgetUpdate")
        
        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())
            
            print(f"DataFrame: {df}")
            return df
    else:
        print("returning None from fetch movies data")
        return None
    
def preprocess_and_combine_features(row):
    genre_1 = row['genre_1'] if not pd.isnull(row['genre_1']) else ''
    #mpaa_rating = row['mpaa_rating'] if not pd.isnull(row['mpaa_rating']) else ''
    mpaa = row['mpaa'] if not pd.isnull(row['mpaa']) else ''
    trivia = row['trivia'] if not pd.isnull(row['trivia']) else ''
    #synopsis = row['synopsis'] if not pd.isnull(row['synopsis']) else ''
    main_actor_1 = row['main_actor_1'] if not pd.isnull(row['main_actor_1']) else ''
    
    #combined = ' '.join(filter(None, [genres, mpaa_rating, tagline, synopsis])).strip()
    combined = ' '.join(filter(None, [genre_1, mpaa, trivia, main_actor_1])).strip()
    return combined

movies = fetch_data()
#if (movies.empty) or (movies is None):
if movies is None:
    raise ValueError("Movies DataFrame is empty.")

if movies is not None:
    movies.fillna('', inplace=True)

    movies['combined_features'] = [preprocess_and_combine_features(row) for index, row in movies.iterrows()]
    #print(movies['combined_features'].head())
    #print(movies['combined_features'].isnull().sum())
    vectorizer = CountVectorizer(stop_words=None, min_df = 1)
    feature_matrix = vectorizer.fit_transform(movies['combined_features'])
    #print("finished feature matrix...")
    cosine_sim = cosine_similarity(feature_matrix)
    #print("finished cosine, starting get rec...")

    def get_recommendations(title):
        indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
        idx = indices.get(title, None)
        if idx is None:
            return ["No movie found with that title."]
        
        sim_scores = [(i, score) for i, score in enumerate(cosine_sim[idx])]
        sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)[1:11]
        movie_indices = [i for i, _ in sim_scores]
        
        return movies['title'].iloc[movie_indices]

    if __name__ == '__main__':
        movie_title = input("Enter a movie title to find similar movies: ")
        recommendations = get_recommendations(movie_title)
        
        print("\nRecommendations based on '{}':".format(movie_title))
        for i, title in enumerate(recommendations, 1):
            print(f"{i}. {title}")
else:
    print("Data was not fetched properly")
