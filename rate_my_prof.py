import pandas as pd
import requests
import tqdm

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}

QUERY = """
query TeacherSearchPaginationQuery(
  $count: Int!
  $cursor: String
  $query: TeacherSearchQuery!
) {
  search: newSearch {
    teachers(query: $query, first: $count, after: $cursor) {
      edges {
        cursor
        node {
          id
          legacyId
          firstName
          lastName
          avgRating
          numRatings
          wouldTakeAgainPercent
          avgDifficulty
          department
          school { name id }
          isSaved
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      resultCount
    }
  }
}
"""


def fetch_api(cursor=None, count=5):
    payload = {
        "operationName": "TeacherSearchPaginationQuery",
        "query": QUERY,
        "variables": {
            "count": count,
            "cursor": cursor,
            "query": {
                "text": "",
                "schoolID": "U2Nob29sLTEyMTg0",
                "fallback": True
            }
        }
    }

    data = requests.post("https://www.ratemyprofessors.com/graphql", json=payload, headers=headers).json()
    teachers = data["data"]["search"]["teachers"]["edges"]

    return [[i["node"]["avgDifficulty"],
             i["node"]["avgRating"],
             i["node"]["department"],
             i["node"]["firstName"],
             i["node"]["lastName"],
             i["node"]["numRatings"],
             i["node"]["wouldTakeAgainPercent"]] for i in teachers], teachers[-1]["cursor"]


data = []
last_cursor = None

for i in range(13):
    r, last_cursor = fetch_api(last_cursor, 100)
    data += r

df = pd.DataFrame(data, columns=["avgDifficulty", "avgRating", "department", "firstName", "lastName", "numRatings",
                                 "wouldTakeAgainPercent"])

df.to_csv("data/ratemyprof.csv", index=False)
