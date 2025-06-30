'''
Given a course request from Banner API, cleans the data to only contain the following attributes:

- courseReferenceNumber
- creditHours
- subject
- subjectCourse
- courseTitle
- meetingScheduleType
- scheduleTypeDescription (lecture, discussion, lab)
- seatsAvailable
- waitAvailable
- meetingsFaculty : beginTime
- meetingsFaculty : endTime
- meetingsFaculty : [Monday, Tuesday, Wed...] (True or False)
- faculty: displayName (if primaryInstructor : True)
'''

def get_dates(data):
    # Pass in meetingTime 
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    class_days = []
    for d in days:
        if data[d] == True:
            class_days.append(d)
    return class_days


def get_instructor(data):
    for d in data:
        if d["primaryIndicator"]:
            return d["displayName"]
        
def get_time_range(data):
    if len(data) > 0:
        mt = data[0]["meetingTime"]
        return mt.get("beginTime"), mt.get("endTime"), get_dates(data[0]["meetingTime"])
    return None, None, None

def clean_reqs(data):
    beginTime, endTime, dates = get_time_range(data["meetingsFaculty"])
    cleaned_data = {
        "crn" : int(data["courseReferenceNumber"]),
        "credits" : data["creditHours"],
        "subject" : data["subject"],
        "subjectCourse" : data["subjectCourse"],
        "title" : data["courseTitle"], 
        "scheduletype" : data["scheduleTypeDescription"],
        "seatsAvailable" : data["seatsAvailable"],
        "waitAvailable" : data["waitAvailable"],
        "beginTime" : beginTime,
        "endTime" : endTime,
        "dates" : dates, 
        "instructor" : get_instructor(data["faculty"]),
        "prereqs" : None
    }
    return cleaned_data


