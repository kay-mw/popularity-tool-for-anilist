import requests

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

username = "keejan"

variables = {
    "page": 1,
    "name": username
}

URL = 'https://graphql.anilist.co'

response = requests.post(URL, json={'query': QUERY, 'variables': variables}, timeout=10)
json_response = response.json()

print(json_response['data']['Page']['users'][0]['statistics']['anime']['scores'][0].keys())
