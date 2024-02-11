"""Test API call to AniList"""

import requests
import pandas as pd
import json

QUERY = '''
query ($type: MediaType, $page: Int, $perPage: Int) {
  Page (page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media (type: $type) {
      characters {
        edges {
          role
          voiceActors {
            id
            name {
              first
              last
            }
          }
        }
      }
      id
      title {
        romaji
        english
        native
      }
    }
  }
}
'''

variables = {
    'type': 'ANIME',
    'page': 1,
    'perPage': 3
}

URL = 'https://graphql.anilist.co'

response = requests.post(URL, json={'query': QUERY, 'variables': variables}, timeout=10)
json_response = response.json()

# print(json_response['data']['Page']['media'].keys())

df = pd.json_normalize(json_response, record_path=['data','Page','media'])

print(df)

# df.to_csv('test.csv')
