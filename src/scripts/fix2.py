from pathlib import Path
import json

data_path = Path(__file__).resolve().parents[2] / "data" / "course_data.json"
with open(data_path, 'r', encoding='utf-8') as f:
    courses = json.load(f)

for course in courses:
    for p in course['prereqs']:
        p = p.replace(" ", "")

file_path = "data/courses.json"
with open(file_path, "w") as json_file:
    json.dump(courses, json_file, indent=4)