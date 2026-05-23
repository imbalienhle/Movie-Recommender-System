import streamlit as st
import pandas as pd
import requests
import pickle

#loads data
with open('movies_data.pki', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

#recommendation function
def get_recommendation(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11] # get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores] #Top10 similar movies
    return movies[['title', 'movie_id']].iloc[movie_indices]

def fetch_poster(movie_id):
    api_key = "1fa933dba3ef05048f9ff564d3411d07"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return None

#streamlit UI
st.title("Movie Recommender System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Search"):
    recommendations = get_recommendation(selected_movie)
    st.session_state.recommendations=recommendations

if "recommendations" in st.session_state:
    recommendations= st.session_state.recommendations

    st.write("Top 10 recommended movies:")

    for i in range(0, 10,5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j<len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    if poster_url:
                        st.image(poster_url, width=130)
                    else:
                        st.image("https://via.placeholder.com/130")
                    st.write(movie_title)



