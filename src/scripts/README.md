Usage of Scripts
(It's a little messy)

banner_pull: pulls course information from banner. creates courses.json and uses the following:
- clean_reqs: given a Banner API request, it extracts only relevant information
- get_prereqs: given a term and course CRN, returns a list of prereqs for the class
assign_keys: given courses.json, groups all courses with the same 