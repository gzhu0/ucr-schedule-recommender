import json

'''
Script to itereate through a json of course information to create a dictionary that maps
course names to its shorthand, eg. Computer Science : CS
'''

# course_crns.json is raw course data
with open('course_crns.json', 'r', encoding='utf-8') as f:
    course_list = json.load(f)


def extract_subject_map(course_list):
    subject_map = {}
    for course in course_list:
        desc = course.get("subjectDescription")
        code = course.get("subject")
        if desc and code:
            subject_map[desc] = code
    return subject_map

def save_subject_map(subject_map, filename='prereq_formats.py'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("prereq_formats = {\n")
        for k, v in sorted(subject_map.items()):
            f.write(f'    {json.dumps(k)}: {json.dumps(v)},\n')
        f.write("}\n")

subject_map = extract_subject_map(course_list)
save_subject_map(subject_map)
