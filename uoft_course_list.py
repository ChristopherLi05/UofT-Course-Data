import os
import json
import pandas as pd

temp = set()

for i in range(2023, 2026):
    for j in [9, 5]:
        temp |= {i[:-5] for i in os.listdir(f"Enrollment-Data/{i}{j}") if
                 i.endswith(".json") and not i.lower().startswith("aa")}

temp |= {i[:-5] for i in os.listdir(f"Enrollment-Data/20229") if i.endswith(".json") and not i.lower().startswith("aa")}

# sg only
temp = {i[:-1] for i in temp if "H1" in i}

# artsci only
df = pd.read_csv("data/course_evals.csv")
courses = set(df["course_code"].unique())

temp &= courses

with open("data/courses.json", "w") as f:
    json.dump(list(temp), f)
