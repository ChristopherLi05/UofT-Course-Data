import pandas as pd
import requests
from tqdm import tqdm

HEADERS = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}


def fetch_depts():
    query = """
        query TeacherSearchPaginationQuery(
          $count: Int!
          $cursor: String
          $query: TeacherSearchQuery!
        ) {
          search: newSearch {
            teachers(query: $query, first: $count, after: $cursor) {
              filters {
                field
                options {
                  value
                  id
                }
              }
            }
          }
        }
    """

    payload = {
        "operationName": "TeacherSearchPaginationQuery",
        "query": query,
        "variables": {
            "count": 1,
            "query": {
                "text": "",
                "schoolID": "U2Nob29sLTEyMTg0",
                "fallback": True,
            }
        }
    }

    data = requests.post("https://www.ratemyprofessors.com/graphql", json=payload, headers=HEADERS).json()
    departments = data["data"]["search"]["teachers"]["filters"][0]["options"]

    return departments


def _fetch_teachers(payload):
    data = requests.post("https://www.ratemyprofessors.com/graphql", json=payload, headers=HEADERS).json()
    teachers = data["data"]["search"]["teachers"]["edges"]

    last_cur = data["data"]["search"]["teachers"]["pageInfo"]["endCursor"]
    has_next = data["data"]["search"]["teachers"]["pageInfo"]["hasNextPage"]

    teachers = [
        [
            i["node"]["id"],
            i["node"]["legacyId"],
            i["node"]["firstName"],
            i["node"]["lastName"],
            i["node"]["avgRating"],
            i["node"]["numRatings"],
            i["node"]["wouldTakeAgainPercent"],
            i["node"]["avgDifficulty"],
            i["node"]["department"],
        ]
        for i in teachers
    ]

    return teachers, last_cur, has_next


def fetch_teachers_dept(dept):
    query = """
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

    all_teachers = []

    last_cur = None
    has_next = True

    while has_next:
        payload = {
            "operationName": "TeacherSearchPaginationQuery",
            "query": query,
            "variables": {
                "count": 100,
                "cursor": last_cur,
                "query": {
                    "text": "",
                    "schoolID": "U2Nob29sLTEyMTg0",
                    "fallback": True,
                    "departmentID": dept
                }
            }
        }

        teachers, last_cur, has_next = _fetch_teachers(payload)
        all_teachers += teachers

    return all_teachers


def fetch_teachers_school(school_id):
    query = """
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

    all_teachers = []

    last_cur = None
    has_next = True

    while has_next:
        payload = {
            "operationName": "TeacherSearchPaginationQuery",
            "query": query,
            "variables": {
                "count": 100,
                "cursor": last_cur,
                "query": {
                    "text": "",
                    "schoolID": school_id,
                    "fallback": True,
                }
            }
        }

        teachers, last_cur, has_next = _fetch_teachers(payload)
        all_teachers += teachers

    return all_teachers


def main():
    all_teachers = []

    school_ids = ["U2Nob29sLTE0ODQ=", "U2Nob29sLTEyMTg0"]

    # departments = fetch_depts()
    # for i in tqdm(departments):
    #     all_teachers += fetch_teachers_dept(i["id"])

    for i in tqdm(school_ids):
        all_teachers += fetch_teachers_school(i)

    df = pd.DataFrame(
        all_teachers,
        columns=[
            "id",
            "legacyId",
            "firstName",
            "lastName",
            "avgRating",
            "numRatings",
            "wouldTakeAgainPercent",
            "avgDifficulty",
            "department",
        ],
    )

    df = df.drop_duplicates().reset_index(drop=True)

    df.to_csv("data/ratemyprof.csv", index=False)


if __name__ == "__main__":
    main()
