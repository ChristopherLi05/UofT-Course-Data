import os
import json

temp = set()

for i in range(2023, 2026):
    for j in [9, 5]:
        temp |= {i[:-5] for i in os.listdir(f"Enrollment-Data/{i}{j}") if
                 i.endswith(".json") and not i.lower().startswith("aa")}

temp |= {i[:-5] for i in os.listdir(f"Enrollment-Data/20229") if i.endswith(".json") and not i.lower().startswith("aa")}

# sg only
temp = [i[:-1] for i in temp if "H1" in i]

with open("data/courses.json", "w") as f:
    json.dump(temp, f)
