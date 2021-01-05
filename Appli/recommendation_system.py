import pandas as pd 
import pickle
import os 

#Define your own path
PATH = "/Users/samuel/Documents/Projets/Reco_movies/"
PATH_SIM = PATH + 'Similarity/'
PATH_MOVIES_RECO = "/Users/samuel/Desktop/"

formated_movie = None
movie = None
cosine_sim = None
recommended_movies = []
good_format_title = []

def recommend(title):
    """
    Function that returns the 10 most similar movies from the one the user liked

    Parameters
    ----------
    title : string
        Title of the film the user watched.

    Returns
    -------
    None.

    """
    
    idx = formated_movie[formated_movie == title].index[0]   # to get the index of the movie title matching the input movie
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)   # similarity scores in descending order
    top_10_indices = list(score_series.iloc[1:11].index)   # to get the indices of top 10 most similar movies
    
    for i in top_10_indices:   # to append the titles of top 10 similar movies to the recommended_movies list
        recommended_movies.append(movie[i])
    
    print('Recommended movies for you : \n')
    for i in top_10_indices:
        print(movie[i])
        
    good_format_title.append(movie[idx])
    


def main():
    
    with open(PATH_SIM + "similarity.pkl", "rb") as f:
        df_sim = pickle.load(f)
        
    global movie
    global cosine_sim
    global formated_movie

    movie = df_sim.ORIGINAL_TITLE
    formated_movie = df_sim.FORMATED_ORIGINAL_TITLE
    cosine_sim = df_sim.drop(['ORIGINAL_TITLE','FORMATED_ORIGINAL_TITLE'], axis=1).values
    
    while True:
        try:
            
            TITLE = input("Which movie did you watch ?\n\n").lower()
            print('')
        
            recommend(TITLE)
            
            with open(PATH_MOVIES_RECO + 'Recommended_for_me.txt', "w") as f:
                f.write(f'Movies to watch after {good_format_title[0]}:\n\n')
                for i in recommended_movies:
                    f.write(f"{i}\n")
                
            os.system("open " + PATH_MOVIES_RECO + 'Recommended_for_me.txt')
            #if you are in windows : os.system("start " + PATH_MOVIES_RECO + 'Recommended_for_me.txt') 
            
            break
        
        except IndexError:
        
            print('This movie is not in our base ! Try another one ')
            continue


if __name__ == '__main__':

    main()
    