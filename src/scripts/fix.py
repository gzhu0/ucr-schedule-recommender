import requests as rq
from requests.cookies import RequestsCookieJar
import json
from .clean_reqs import clean_reqs
from .get_prereqs import fetch_prereq_info
from collections import defaultdict

'''
Fix to assign courseschedule to course_data
'''
# Get Java Token (J Session ID)
JSESSIONID = rq.get("https://registrationssb.ucr.edu").cookies["JSESSIONID"]

# Set Headers
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

# Post Request 
year = 2025
quarter = {'winter':10, 'spring':20, 'summer':30, 'fall':40}
term = year*100 + quarter['fall']
r = rq.request("POST", "https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/term/search?mode=search", data={"term": term})

# Store Cookies
jar = RequestsCookieJar()
jar.update(r.cookies)

# Get Total Number of Courses in the quarter
pageOffset = 0
pageMaxSize = 500

# Initial request to get totalCount of courses
url = f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?&txt_term={term}&pageOffset={pageOffset}&pageMaxSize={pageMaxSize}&sortColumn=subjectDescription&sortDirection=asc"
response = rq.request("GET", url, headers=headers, cookies=jar)
totalCount = response.json()["totalCount"]
print(totalCount) 


# Note: Totalcount is 10843 for Fall 2024

pageMaxSize = 500  # max request size
courses = []
pageOffset = 0


from pathlib import Path
data_path = Path(__file__).resolve().parents[2] / "data" / "course_data.json"
with open(data_path, 'r', encoding='utf-8') as f:
    course_list = json.load(f)

    
crn_map = dict()

while True:
    print(pageOffset)
    url = f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?&txt_term={term}&startDatepicker=&endDatepicker=&pageOffset={pageOffset}&pageMaxSize={pageMaxSize}&sortColumn=subjectDescription&sortDirection=asc"

    response = rq.request("GET", url, headers=headers, cookies=jar)
    response.raise_for_status()
    new_courses = response.json()["data"]

    if not new_courses:
        print("No more courses available.")
        break

    for course in new_courses:
        crn = int(course["courseReferenceNumber"])
        subjectCourse = course['subjectCourse']
        #There won't be crn dupes present
        crn_map[crn] = subjectCourse

    if len(new_courses) < pageMaxSize:
        print("Fetched all available data.")
        break
    
    pageOffset += pageMaxSize #getting next 500 sections
    
    if len(courses) >= totalCount:
        break

unfound = 0
for course in course_list:
    if int(course["crn"]) in crn_map:
        course['subjectCourse'] = crn_map[int(course["crn"])]
    else: unfound += 1
print(f"{unfound} crns not found")

file_path = "data/courses_update.json"
with open(file_path, "w") as json_file:
    json.dump(course_list, json_file, indent=4)


