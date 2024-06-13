import requests
import pandas as pd
import pickle
import streamlit as st


def fetch_poster(movie_id):
    api_key = "6821bdfddbd814aaf0090a800aeff6fb"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except requests.RequestException as e:
        return f"Error fetching poster: {e}"


def recommend(movie, movies, similarity):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for index, _ in movies_list:
        movie_id = movies.iloc[index].movie_id
        recommended_movies.append(movies.iloc[index].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit interface
st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, movies, similarity)
    if names:
        cols = st.columns(len(names))
        for idx, col in enumerate(cols):
            with col:
                st.image(posters[idx], caption=names[idx])
    else:
        st.write("No recommendations found.")
