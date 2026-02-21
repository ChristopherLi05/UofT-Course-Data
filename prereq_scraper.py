import json
from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm


class Prereq:
    def __init__(self, parent=None):
        self.parent = parent
        self.prereqs = []
        self.prereq_type = None

    def new_group(self):
        self.prereqs.append(Prereq(self))
        return self.prereqs[-1]

    def dump(self):
        return {
            "prereq_type": self.prereq_type,
            "prereqs": [i if isinstance(i, str) else i.dump() for i in self.prereqs]
        }


def get_course_prereqs(course_code):
    a = requests.get(f"https://artsci.calendar.utoronto.ca/course/{course_code}")
    soup = BeautifulSoup(a.text, "html.parser")

    PREREQ_SELECTOR = "#block-w3css-subtheme-content > article > div > div.w3-row.field.field--name-field-prerequisite.field--type-text-long.field--label-inline.clearfix > div"

    selector = [i for i in soup.select(PREREQ_SELECTOR)]

    if not selector:
        print(f"No prereqs found for course: {course_code}")
        return Prereq().dump()

    print(course_code)

    tokens = [
        k
        for i in selector[0].children
        for j in [re.sub(r"\s", "", i.text)]
        for k in ([j] if j.isalnum() else list(j))
    ]

    root = ref = Prereq()
    for i in tokens:
        if i == "(":
            ref = ref.new_group()
        elif i == "/":
            if not ref.prereq_type:
                ref.prereq_type = "OR"
            elif ref.prereq_type != "OR":
                ref = ref.parent.new_group()
                ref.prereq_type = "OR"
        elif i == "," or i == ";":
            if not ref.prereq_type:
                ref.prereq_type = "AND"
            elif ref.prereq_type != "AND":
                ref = ref.parent.new_group()
                ref.prereq_type = "AND"
        elif i == ")":
            ref = ref.parent
        elif len(i) > 3 and i[:3].isupper():
            ref.prereqs.append(i)
        else:
            break

    return root.dump()


with open("data/courses.json") as f:
    courses = json.load(f)

course_prereqs = {}

for idx, c in enumerate(tqdm(courses), start=1):
    course_prereqs[c] = get_course_prereqs(c.lower())

    if idx % 200 == 0:
        with open("data/partial_prereq/course_prereqs_partial.json", "w") as f:
            json.dump(course_prereqs, f)

with open("data/course_prereqs.json", "w") as f:
    json.dump(course_prereqs, f)
