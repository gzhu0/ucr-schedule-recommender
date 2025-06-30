import re
from .coursenames import prereq_formats

'''
Parses prereqs into a list of course names converts name from long form to short form
eg. Computer Science -> CS
'''

def parse_prereqs(text: str)->list[str]:
    pattern = r"Course or Test:\s*(.+)"
    matches = re.findall(pattern, text)
    return [clean_prereqs(match.strip()) for match in matches]


def clean_prereqs(text:str)->str:
    pattern = r'([A-Za-z\s&]+?)\s(?=\d{3}[A-Z]?)'

    def replacer(match):
        subject = match.group(1).strip()
        mapped = prereq_formats.get(subject, subject)
        return mapped + ' '

    return re.sub(pattern, replacer, text)