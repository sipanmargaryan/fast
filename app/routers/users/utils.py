import json

import numpy as np
import requests
from fastapi import HTTPException, status

from app import settings

URL = settings.HASURA_URL
AUTH = {'x-hasura-admin-secret': settings.HASURA_TOKEN}


class InterestVector:
    def __init__(self, categories_dict_path, post_coef=0.8, vote_coef=0.8, comment_coef=0.8):
        with open(categories_dict_path, "r") as read_content:
            self.categories_dict = json.load(read_content)

        self.post_coef = post_coef
        self.vote_coef = vote_coef
        self.comment_coef = comment_coef

        self.length_number = 220

    def __map_category(self, name: str, confidence: float):
        """Maps the nlp category into two-depth category.
        One depth-category translates to have the subcategories of this category,
        second depth-category remains as it is, and third-depth category maps to
        the parent subcategory.

        Args:
            name: Category name predicted
            confidence: The confidence associated with the category

        Returns:
            - indices: a numpy array of indices of mapped subcategories,
            - confidence: score for each subcategory in the list of indices,
        """
        splitted = name.split("/")[1:]
        if len(splitted) == 1:
            if type(self.categories_dict[splitted[0]]) == int:
                indices = np.array(self.categories_dict[splitted[0]])
            else:
                indices = np.array(list(self.categories_dict[splitted[0]].values()))
                confidence /= len(indices)
        else:
            try:
                cat, subcat = splitted[0], splitted[1]
                indices = np.array(self.categories_dict[cat][subcat])
            except IndexError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category.")

        return indices, confidence

    def __get_user_interest_vector(self, user_id: str):
        user_query = '''
        query InterestVector {{
          user_interested_vector(where: {{user_id: {{_eq: "{user_id}"}}}}) {{
            interested_vector
          }}
        }}
        '''.format(user_id=user_id)
        interest_vector = requests.post(URL, json={'query': user_query}, headers=AUTH).json()
        if interest_vector.get("errors"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found!")
        interest_vector = interest_vector['data']['user_interested_vector']
        return np.array(interest_vector[0]['interested_vector'])

    def __get_content_nlp_categories(self, content_id: str):
        content_query = '''query ContentNlp {{
          content(where: {{id: {{_eq: "{content_id}" }}}}) {{
            nlp_categories {{
                name
                confidence
            }}
          }}
        }}
        '''.format(content_id=content_id)
        content_nlp = requests.post(URL, json={'query': content_query}, headers=AUTH).json()
        if content_nlp.get("errors"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content not found!")
        content_nlp = content_nlp['data']['content']
        return content_nlp[0]['nlp_categories']

    def get_updated_vector(self, user_id: str, content_id: str, update_type: str):
        user_interest_vector = self.__get_user_interest_vector(user_id)
        nlp = self.__get_content_nlp_categories(content_id)

        if update_type == 'post':
            coefficient = self.post_coef
        elif update_type == 'vote':
            coefficient = self.vote_coef
        elif update_type == 'comment':
            coefficient = self.comment_coef

        if nlp:
            new_vector = np.zeros(self.length_number)
            for found in nlp:
                vector_index, conf = self.__map_category(found['name'], found['confidence'])
                new_vector[vector_index] = conf

            user_interest_vector = coefficient * user_interest_vector + (1 - coefficient) * new_vector

        return user_interest_vector.tolist()
    
    def create_vector(self, categories: list[str]) -> list[float]:
        """Get fisrt user interest vector based on marked interests of the user when registration."""
        user_interest_vector = np.zeros(self.length_number)
        for category in categories:
            vector_index, conf = self.__map_category(name=category, confidence=1.0)
            user_interest_vector[vector_index] = conf 
        return user_interest_vector.tolist()
