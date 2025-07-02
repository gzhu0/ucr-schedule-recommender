from collections import defaultdict
import json
from pathlib import Path

data_path = Path(__file__).resolve().parents[2] / "data" / "courses.json"
with open(data_path, 'r', encoding='utf-8') as f:
    course_list = json.load(f)

course_map = defaultdict(lambda: defaultdict(list))

for course in course_list:
    sc = course["subjectCourse"]
    stype = course["scheduletype"].lower()  # e.g. "lecture", "laboratory", "discussion"
    course_map[sc][stype].append(course)

regular_course_map = {sc: dict(types) for sc, types in course_map.items()}

# Write to JSON file
with open('data\\course_map.json', 'w', encoding='utf-8') as f:
    json.dump(regular_course_map, f, indent=2, ensure_ascii=False)