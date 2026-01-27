import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def request_artsci(page_num, page_size=100):
    data = requests.post("https://course-evals.utoronto.ca/BPI/fbview-WebService.asmx/getFbvGrid", json={
        "strUiCultureIn": "en",
        "datasourceId": "7160",
        "blockId": "2330",
        "subjectColId": "1",
        "subjectValue": "____[-1]____",
        "detailValue": "____[-1]____",
        "gridId": "fbvGrid",
        "pageActuelle": page_num,
        "strOrderBy": [
            "col_0",
            "asc"
        ],
        "strFilter": [
            "",
            "",
            "ddlFbvColumnSelectorLvl1",
            ""
        ],
        "sortCallbackFunc": "__getFbvGrid",
        "userid": "5cvfXC__2iiaFF-lP3upQ9R50q2cOcJ2bH2M",
        "pageSize": str(page_size)
    }).json()

    soup = BeautifulSoup(data["d"][0], 'html.parser')
    return [[j.text.strip() for j in i.children if j.text.strip()] for i in soup.select(".gData")]


data = []

for i in tqdm(range(444)):
    data += request_artsci(i + 1)

df = pd.DataFrame(data, columns=[
    "dept",
    "division",
    "course",
    "last_name",
    "first_name",
    "term",
    "year",
    "INS1",
    "INS2",
    "INS3",
    "INS4",
    "INS5",
    "INS6",
    "ARTSC1",
    "ARTSC2",
    "ARTSC3",
    "number_invited",
    "number_responses"
])

df["course_code"] = df["course"].str.extract(r'([A-Z]{3}\d{3}[HY]\d)')
df.to_csv("data/course_evals.csv", index=False)
