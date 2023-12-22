To run data-mining application, first execute:

1. make install
2. make run

Once finished using data-mining application execute:

3. make clean


This movie recommender uses datamining to suggest movies to users based on the contents of a database populated by aggragating the dataset links below (the client application, SQl tables, and schema.txt were written with help from Hussain Kuvawala and Isaiah Richards).

The recommender establishes a connection to the database managed by connect_to_database(), which uses SQLAlchemy to interact with it. An SQL query then fetches data from the MojoBudgetUpdate, transforming the results into a pandas DataFrame to be processed.

To preprocess the data, our algorithm handles missing values and combines multiple text features from the dataset (genre_1, mpaa, main_actor_1, and trivia) into a single string. This creates a representation of each movie, making it easier to assess their similarities

The text data is then put into a numerical form to calculate similarity, using CountVectorizer() for feature extraction. The numerical form is a sparse matrix of token counts, which represents the frequency of words across all the movie descriptions. Using this matrix, the pairwise cosine_similarity() is computed for all movies in our dataset, to measure how similar the documents are (regardless of size).

Get_recommendations() takes a movie title as input, identifies its index, and finds the movies that are most similar based on these cosine similarities. They are sorted into descending order and the top ten are returned.



![image](https://github.com/DanielT504/Movie-rec-data-miner/assets/62156098/928e3710-29b9-4fd7-a2d8-e11190e17e18)



Dataset Links

- https://www.kaggle.com/igorkirko/wwwboxofficemojocom-movies-with-budget-listed
- https://www.kaggle.com/rounakbanik/the-movies-dataset
- https://www.kaggle.com/zeegerman/hollywood-stock-exchange-box-office-data
