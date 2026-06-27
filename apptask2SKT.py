import streamlit as st
import pandas as pd
import requests 
import pickle

with open('movies.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)
    
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key= lambda x: x[1], reverse= True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

def fetch_poster(movie_title):
    api_key = "9cc85cc6"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=9cc85cc6"
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "True":
        return data["Poster"]
    else:
        return "http//via.placeholder.com/300x450?text =No+Poster"

st.title('Movie Recommendation System')

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write('Top 10 similar movies:')
    
    for i in range(0, 10, 5):
        cols= st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
               movie_title= recommendations.iloc[j]['title']
               poster_url = fetch_poster(movie_title)
               with col:
                   st.image(poster_url, width = 130)
                   st.write(movie_title)