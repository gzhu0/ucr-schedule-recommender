import json
from pathlib import Path

'''
Tools involving data pulling
'''

data_path = Path(__file__).resolve().parents[2] / "data" / "course_map.json"
with open(data_path, 'r', encoding='utf-8') as f:
    courses = json.load(f)

data_path = Path(__file__).resolve().parents[2] / "data" / "crn_map.json"
with open(data_path, 'r', encoding='utf-8') as f:
    crns = json.load(f)

data_path = Path(__file__).resolve().parents[2] / "data" / "courses_taken.json"
with open(data_path, 'r', encoding='utf-8') as f:
    courses_taken = json.load(f)

data_path = Path(__file__).resolve().parents[2] / "data" / "major_reqs.json"
with open(data_path, 'r', encoding='utf-8') as f:
    major_reqs = json.load(f)

# Data Retrieval

def get_course_crns(courseName:str):
    '''
    Returns a list of crns associated with that course
    '''
    return {"crns": courses[courseName]}

def get_crn_info(crn:str):
    '''
    Returns course data associated with a crn
    '''
    return crns[crn]

def get_all_crn_info(courseName: str):
    """
    Returns a list of detailed course info dictionaries for each CRN under the given course.
    """
    crn_list = get_course_crns(courseName)["crns"]
    return {
        "infos": [get_crn_info(str(crn)) for crn in crn_list]
    }

def get_dates(crn:str):
    return crns[crn]["section_data"]['dates']

def get_times(crn:str):
    return crns[crn]["section_data"]['beginTime'], crns[crn]["section_data"]['endTime']

# Schedule (list of course names)
schedule = []

def read_schedule():
    return schedule

def add_to_schedule(crn:str):
    for course in schedule:
        new_course_days = get_dates(crn)
        course_days = get_dates(course)
        if set(new_course_days).intersection(set(course_days)):
            #start time OR end time is within other course
            if (get_times(crn)[0] > get_times(course)[0] and get_times(crn)[0] < get_times(course)[1] or 
            get_times(crn)[1] > get_times(course)[0] and get_times(crn)[1] < get_times(course)[1] ):
                return {
                    "status": "error",
                    "reason": "time_conflict",
                    "conflicting_course": course,
                    "message": f"{crn} overlaps with {course}."
                }
    schedule.append(crn)
    return {
        "status": "success",
        "message": "Course added successfully.",
        "added_course": crn
    }



def remove_from_schedule(crn:str):
    schedule.pop(crn)


