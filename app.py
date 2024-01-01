import streamlit as st  
import numpy as np 
import pandas as pd
import requests as rq
import pickle 
df = pd.read_csv('popular_movies.csv')
def fetch_poster(movie_id):
    response = rq.get('https://api.themoviedb.org/3/movie/{}?api_key=122e3bb69d5482904eb5b0f00db44b77&language=en-US'.format(movie_id))
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
path=[]
names=[]
all_names=[]
for i in range(50):
    all_names.append(df.iloc[i]['title'])
st.set_page_config(page_title="Movie_recommender", page_icon="👑", layout="wide")

st.title('Movie Recommender System')  
st.subheader('Top 10 movies')  
def display_50():
    
    df = pd.read_csv('popular_movies.csv')
    for i in range(10):
        path.append(fetch_poster(df.iloc[i]['movieId']))
        names.append(df.iloc[i]['title'])
    return df
display_50()
k=0
for j in range(2):
    for i in st.columns(5,gap='medium'):
        with i:
            st.image(path[k])
            st.write(names[k])
        k+=1


simi=pickle.load(open('simi.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))

mv=pd.read_csv('movie_name_id.csv')
def search(name):
    rec=[]
    s=mv[mv['title']==name]
    return int(s['id'].values[0])

def recommend(movie):
    index=np.where(pt.index==movie)[0][0]
    s=sorted(list(enumerate(simi[index])),key=lambda x:x[1],reverse=True)[1:6]
    col=st.columns(5)
    for j,i in enumerate(s):
        with col[j]:
            st.write(pt.index[i[0]])
            st.image(fetch_poster(search(pt.index[i[0]])))
        #st.write(pt.index[i[0]])
        
n=st.selectbox('Select a movie',pt.index)       



if(st.button('Recommend')):
    recommend(n)