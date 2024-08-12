import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Sample dataset of movies
data = {
    'title': ['Inception', 'Interstellar', 'The Dark Knight', 'Fight Club', 'Pulp Fiction',
              'Forrest Gump', 'The Matrix', 'The Shawshank Redemption', 'Gladiator', 'Titanic'],
    'genre': ['Action', 'Sci-Fi', 'Action', 'Drama', 'Crime',
              'Drama', 'Sci-Fi', 'Drama', 'Action', 'Romance'],
    'director': ['Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'David Fincher', 'Quentin Tarantino',
                 'Robert Zemeckis', 'The Wachowskis', 'Frank Darabont', 'Ridley Scott', 'James Cameron'],
    'actors': ['Leonardo DiCaprio, Joseph Gordon-Levitt', 'Matthew McConaughey, Anne Hathaway',
               'Christian Bale, Heath Ledger',
               'Brad Pitt, Edward Norton', 'John Travolta, Uma Thurman', 'Tom Hanks, Robin Wright',
               'Keanu Reeves, Laurence Fishburne',
               'Tim Robbins, Morgan Freeman', 'Russell Crowe, Joaquin Phoenix', 'Leonardo DiCaprio, Kate Winslet']
}

# Create DataFrame
df = pd.DataFrame(data)

# Combine genre, director, and actors into a single string
df['content'] = df['genre'] + ' ' + df['director'] + ' ' + df['actors']

# Compute TF-IDF matrix
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['content'])

# Compute cosine similarity matrixS
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


# Function to get movie recommendations
def recommend_movies(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = df.index[df['title'] == title].tolist()[0]

    # Get pairwise similarity scores for the movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 5 similar movies
    movie_indices = [i[0] for i in sim_scores[1:6]]

    # Return the top 5 most similar movies
    return df['title'].iloc[movie_indices]


# Example usage
if __name__ == "__main__":
    movie_title = 'Inception'
    print(f"Movies similar to '{movie_title}':")
    recommendations = recommend_movies(movie_title)
    for movie in recommendations:
        print(f"- {movie}")

