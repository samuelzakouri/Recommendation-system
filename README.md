# Recommendation system

I tried to build a recommendation system for movies based on content-based filtering using some NLP methods.

## Dataset Information

The initial Database was from IMDB with a lot of cleaning to do and then I have constructed my own Database from it.

## Content-based filtering

To customize the recommendations, we create a engine that calculates the similarity between movies based on certain metrics and suggests movies that are the most similar to a particular movie that a user liked. Since we will use film metadata (or content) to create this engine, this is also called content-based filtering.

We use the casting, the director, the overview, the genre and the production company of the movies to calculate the similarity between them.
To do that, we use the Cosine similarity which the formula is given by :
```math
cos (x,y) =\frac {x.y^T}{\lVert{x}\\rVert.\lVert{y}\rVert}
```

## Application 

1. Run `generate_similarity.py`: It calculates the similarity matrix and save it in a file.

2. Run `recommendation_system.py`: 
 - Load the similarity file
 - Ask you which movie did you watch ? 
 - Return the ten most similar movies 
 - Create a `.txt` with the list of recommended movies for you
 
## Requirements

* `Numpy`
* `Pandas`
* `Scikit-learn`

or 

```bash
pip install -r requirements.txt
```

