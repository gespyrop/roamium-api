from abc import ABC, abstractmethod

from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial import distance
import pandas as pd
import json



class RecommendationService(ABC):
    '''Handles the place recommendation logic.'''

    @abstractmethod
    def recommend(self, places: list, user_features: dict) -> list:
        '''
        Recommends the most suitable places for a user 
        based on the provided criteria.
        '''
        pass


class CosineSimilarityRecommendationService(RecommendationService):
    '''
    Handles the place recommendation logic using weighted cosine similarity.
    '''
    
    def __init__(self, radius, weights):
        self.radius = radius
        self.weights = weights

    def __preprocess(self, df) -> pd.DataFrame:
        '''Handles place data preprocessing.'''

        # Map wheelchair values to numbers
        df['wheelchair'] = df['wheelchair'].map({'no': -1, 'limited': 1, 'yes': 2}).fillna(0)

        return df
    
    def __calculate_category_similarity(self, place_categories: pd.Series, user_categories: list) -> pd.Series:
        '''
        Calculates the category similarities for a given set of places.

        user_categories: A list containing the categories selected by the user.
        '''
        combined_categories = place_categories.apply(lambda row: ' '.join(row))

        # Calculate the place category feature vectors
        cv = CountVectorizer()
        count_array = cv.fit_transform(combined_categories).toarray()

        categories = cv.get_feature_names_out()
        place_feature_vectors = pd.DataFrame(count_array, columns=categories)

        # Calculate the user category feature vectors
        user_feature_vector = pd.DataFrame(columns=categories)
        user_feature_vector.loc[0] = [int(category in user_categories) for category in categories]

        # Return the cosine similarity between the user's category feature vector
        # and each of the place feature vectors.
        return place_feature_vectors.apply(lambda vector : 1 - distance.cosine(vector, user_feature_vector), axis=1)

    def recommend(self, places: list, user_features: dict) -> list:
        '''
        Recommends the most suitable places for a user 
        based on the provided criteria.
        '''
        df = self.__preprocess(pd.DataFrame(places))

        # Category Score
        df['category_similarity'] = self.__calculate_category_similarity(df['categories'], user_features.get('categories', []))

        wheelchair = user_features.get('wheelchair', 0)

        # Calculate the final feature vector
        features = df[['id', 'category_similarity', 'wheelchair', 'distance']].copy()

        max_distance = features['distance'].max() - 0.000001
        features['distance'] = 1 - (features['distance'] / max_distance)

        # Use the feature vector to calculate a score for each place
        df['score'] = features.apply(lambda vector: 1 - distance.cosine([1.0 , wheelchair, 1.0], [10*vector['category_similarity'], vector['wheelchair'], vector['distance']], self.weights), axis=1)

        # Sort places by score
        df.sort_values(by=['score'], ascending=[False], inplace=True)

        df['wheelchair'] = df['wheelchair'].map({-1: 'no', 0: None, 1: 'limited', 2: 'yes'})

        return json.loads(df.to_json(orient='records'))
