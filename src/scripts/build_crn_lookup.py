import json
from pathlib import Path

data_path = Path(__file__).resolve().parents[2] / "data" / "course_map.json"
with open(data_path, 'r', encoding='utf-8') as f:
    courses = json.load(f)


def build_crn_lookup(course_data):
    crn_lookup = {}
    for course_code, section_types in course_data.items():
        for section_type, sections in section_types.items():
            for section in sections:
                crn = section["crn"]
                crn_lookup[crn] = {
                    "course_code": course_code,
                    "section_type": section_type,
                    "section_data": section
                }
    return crn_lookup

def extract_course_crns(course_data):
    course_crn_map = {}
    for course_key, section_types in course_data.items():
        crns = []
        for section_list in section_types.values():  # lecture, laboratory, etc.
            for section in section_list:
                crns.append(section["crn"])
        course_crn_map[course_key] = crns
    return course_crn_map

course_to_crn = extract_course_crns(courses)

file_path = "data/courses_map.json"
with open(file_path, "w") as json_file:
    json.dump(course_to_crn, json_file, indent=4)

# crn_lookup = build_crn_lookup(courses)

# file_path = "data/crn_map.json"
# with open(file_path, "w") as json_file:
#     json.dump(crn_lookup, json_file, indent=4)