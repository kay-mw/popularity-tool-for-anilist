import requests
import pandas as pd

QUERY = '''
query ($page: Int, $name: String) {
  Page (page: $page) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    users (name: $name) {
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

variables = {
    "page": 1,
    "name": "keejan"
}

URL = 'https://graphql.anilist.co'

max_pages = 5

response = requests.post(URL, json={'query': QUERY, 'variables': variables}, timeout=30)
json_response = response.json()
print(json_response)

df = pd.json_normalize(json_response, record_path=['data', 'Page', 'users'])

print(df.to_string())
# print(json_response['data']['Page']['users'].keys())

# while variables['page'] <= max_pages:
#     response = requests.post(URL, json={'query': QUERY, 'variables': variables}, timeout=30)
#     json_response = response.json()
#
#     if not json_response['data']['Page']['pageInfo']['hasNextPage']:
#         break
#
#     page_df = pd.json_normalize(json_response, record_path=['data', 'Page', 'users'])
#     df = pd.concat([page_df, df], ignore_index=True)
#
#     variables['page'] += 1
#
# print(df.to_string())
# print(response.headers)