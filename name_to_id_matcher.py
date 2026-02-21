import pandas as pd
import difflib
from tqdm import tqdm
import json

DF = pd.read_csv("data/ratemyprof.csv")[["id", "firstName", "lastName"]]

DF["firstName"] = DF["firstName"].str.lower()
DF["lastName"] = DF["lastName"].str.lower()
DF["combined"] = DF["firstName"] + " " + DF["lastName"]


def match_name(first_name, last_name):
    first_name = first_name.lower()
    last_name = last_name.lower()

    exact = DF[(DF["firstName"] == first_name) & (DF["lastName"] == last_name)].reset_index(drop=True)

    if exact.shape[0] >= 1:
        return exact["id"].values.tolist()

    fuzzies = difflib.get_close_matches(f"{first_name} {last_name}", DF.combined.values, cutoff=0.85)
    matched_rows = DF[DF['combined'].isin(fuzzies)]

    return matched_rows["id"].values.tolist()


def main():
    df = pd.read_csv("data/course_evals.csv")[["first_name", "last_name"]].drop_duplicates().reset_index(drop=True)

    mapping = {}

    for first, last in tqdm(df.values):
        mapping[f"{first} {last}"] = match_name(first, last)

    with open("data/prof_mapping.json", "w") as f:
        json.dump(mapping, f)

if __name__ == "__main__":
    main()
