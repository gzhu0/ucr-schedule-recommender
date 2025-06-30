import json
from ..scripts.clean_reqs import clean_reqs

with open("course_crns.json", "r") as file:
    data = json.load(file)  # Assuming it's a list of dicts

first_three = data[:100]
print(first_three)

for idx, val in enumerate(first_three):
    first_three[idx] = clean_reqs(val)

print(first_three)
    

