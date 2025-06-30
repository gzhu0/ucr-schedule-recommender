import requests as rq
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from ..util.parse_prereqs import parse_prereqs
import json

''' 
Testing API Requests
'''

# Testing course prereqs
term = 202440
crn = 30950

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

def fetch_prereq_info(term:int, crn:int) -> list[str]:
    url = f"https://registrationssb.ucr.edu/StudentRegistrationSsb/ssb/searchResults/getSectionPrerequisites?term={term}&courseReferenceNumber={crn}"
    response = rq.request("GET", url, headers=headers, cookies=jar)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.prettify()[:500]
    result = parse_prereqs(soup)
    return result

