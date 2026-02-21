import requests
from tqdm import tqdm
import pandas as pd

HEADERS = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}


def fetch_prof_ratings(prof_id):
    query = """query RatingsListQuery(
      $count: Int!
      $id: ID!
      $courseFilter: String
      $cursor: String
    ) {
      node(id: $id) {
        id
        
        ... on Teacher {
          id
          legacyId
          numRatings

          ratings(
            first: $count
            after: $cursor
            courseFilter: $courseFilter
          ) {
            edges {
              cursor
              node {    
                comment
                date
                class
                helpfulRating
                clarityRating
                difficultyRating
    
                attendanceMandatory
                wouldTakeAgain
                grade
                textbookUse
                isForOnlineClass
                isForCredit
    
                ratingTags
              }
            }
    
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }"""

    all_ratings = []

    last_cur = None
    has_next = True

    while has_next:
        payload = {
            "operationName": "RatingsListQuery",
            "query": query,
            "variables": {
                "count": 100,
                "cursor": last_cur,
                "courseFilter": None,
                "id": prof_id
            }
        }

        data = requests.post("https://www.ratemyprofessors.com/graphql", json=payload, headers=HEADERS).json()
        ratings = data["data"]["node"]["ratings"]["edges"]

        last_cur = data["data"]["node"]["ratings"]["pageInfo"]["endCursor"]
        has_next = data["data"]["node"]["ratings"]["pageInfo"]["hasNextPage"]

        all_ratings += [
            [
                prof_id,
                d["node"].get("comment"),
                d["node"].get("date"),
                d["node"].get("class"),
                d["node"].get("helpfulRating"),
                d["node"].get("clarityRating"),
                d["node"].get("difficultyRating"),
                d["node"].get("attendanceMandatory"),
                d["node"].get("wouldTakeAgain"),
                d["node"].get("grade"),
                d["node"].get("textbookUse"),
                d["node"].get("isForOnlineClass"),
                d["node"].get("isForCredit"),
                d["node"].get("ratingTags")
            ]
            for d in ratings
        ]

    return all_ratings


def main():
    prof_ids = pd.read_csv("data/ratemyprof.csv")["id"].values

    all_ratings = []

    for i in tqdm(prof_ids):
        all_ratings += fetch_prof_ratings(i)

    df = pd.DataFrame(all_ratings, columns=[
        "prof_id", "comment", "date", "class", "helpfulRating", "clarityRating", "difficultyRating",
        "attendanceMandatory", "wouldTakeAgain", "grade", "textbookUse", "isForOnlineClass",
        "isForCredit", "ratingTags"
    ])

    df.to_csv("data/ratings.csv", index=False)


if __name__ == "__main__":
    main()

fetch_prof_ratings("VGVhY2hlci04NjUyMjc=")
