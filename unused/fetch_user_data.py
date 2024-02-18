import requests
import pandas as pd

QUERY = '''
query ($page: Int, $name: String, $mediaIds: Int) {
  Page (page: $page) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    users (name: $name, mediaIds: $mediaIds) {
      id
      name
      statistics {
        anime {
          scores {
            mediaIds
            score
          }
        }
      }
    }
  }
}
'''

username = "keejan"

variables = {
    "page": 1,
    "name": {username}
}

URL = 'https://graphql.anilist.co'

response = requests.post(URL, json={'query': QUERY, 'variables': variables}, timeout=30)
json_response = response.json()

print(response.headers)
print(response.status_code)
print(response.reason)

df = pd.json_normalize(json_response, record_path=['data', 'Page', 'users', 'statistics', 'anime', 'scores'])

df = df.explode('mediaIds')
df['mediaIds'] = df['mediaIds'].astype(int)

print(df.to_string())
