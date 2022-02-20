from abc import ABC, abstractmethod


class RecommendationService(ABC):
    '''Handles the place recommendation logic.'''

    @abstractmethod
    def recommend(self, places: list) -> list:
        '''
        Recommends the most suitable places for a user 
        based on the provided criteria.
        '''
        pass


class CosineSimilarityRecommendationService(RecommendationService):
    '''
    Handles the place recommendation logic using weighted cosine similarity.
    '''

    def recommend(self, places: list) -> list:
        '''
        Recommends the most suitable places for a user 
        based on the provided criteria.
        '''
        # TODO Calculate weighted cosine similarity and sort places
        return places