import streamlit as st  
import pandas as pd  
import numpy as np

## cd "ali/Documents/Grad/DSC 680/Portfolio/Local Machine/Projects/Movie Recommender System"

st.title('Film Recommender')

movie_df = pd.read_csv("ratings.csv")
movie_titles_df = pd.read_csv("movies.csv")

movie_df = movie_df.merge(movie_titles_df, on='movieId', how='left')

avg_ratings = pd.DataFrame(movie_df.groupby('title')['rating'].mean())
avg_ratings.sort_values(by='rating', ascending=False)
avg_ratings['Total Ratings'] = pd.DataFrame(movie_df.groupby('title')['rating'].count())
avg_ratings.sort_values(by='rating', ascending=False)

movie100_df = avg_ratings.loc[avg_ratings['Total Ratings'] > 100]
movie_user = movie_df.pivot_table(index='userId',columns='title',values='rating')

def recommend(movie):
    movie_matches = [col for col in movie_df.title if
                    movie in col]
    try:
        match1 = movie_matches[0]
    except:
        print('No matches found for', movie)
        return()
        
    print('Finding recommendations for:', match1)
    
    corr = movie_user.corrwith(movie_user[match1])
    rec = pd.DataFrame(corr,columns=['Correlation'])
    rec.dropna(inplace=True)
    rec = rec.join(avg_ratings['Total Ratings'])
    rec_m = rec[rec['Total Ratings']>100].sort_values(
        'Correlation', ascending=False).reset_index()
    rec_m = rec_m.merge(movie_titles_df, on='title',
                       how='left')
    
    rec_m.drop(['Total Ratings', 'movieId'], axis=1, 
               inplace=True)
    rec_m = rec_m.rename(columns={'Correlation': 'match'})
    
    return rec_m.head(6)

###

movie = st.text_input('What is your favorite movie?', 'Shrek')

recs = recommend(movie)

recs.rename(columns = {'title':'Film', 'match':'Match', 'genres':'Genres'}, inplace=True)
recs['Match'] = recs['Match'].map('{:.1%}'.format)

selfm = recs['Match'] == '100.0%'
recs = recs[~selfm]

recs['Genres'] = recs['Genres'].str.split('|')

st.subheader('You should check out these titles:')

st.dataframe(data=recs, hide_index=True)