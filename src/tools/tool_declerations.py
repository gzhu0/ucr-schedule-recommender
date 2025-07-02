from google.genai import types

tool_declarations = [
    {
        "name": "get_course_crns",
        "description": "Retrieves a list of course CRNs of the given course. Returns a dictionary with key 'crns' mapping to the list.",
        "parameters": {
            "type": "object",
            "properties": {
                "courseName": {
                    "type": "string",
                    "description": "Course key or subjectCourse string, e.g., CS010A or MATH011"
                }
            },
            "required": ["courseName"]
        }
    },
    {
    "name": "get_all_crn_info",
    "description": "Returns a list of detailed information for all CRNs associated with the given course key.",
    "parameters": {
        "type": "object",
        "properties": {
            "courseName": {
                "type": "string",
                "description": "The course key or subjectCourse string, e.g., CS010A or MATH011"
            }
        },
        "required": ["courseName"]
    }
    },
    {
        "name": "get_crn_info",
        "description": "Retrieves course info with information such as date, prereqs, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "crn": {
                    "type": "string",
                    "description": "Unique course reference number to that section of the course"
                }
            },
            "required": ["crn"]
        }
    },
    {
        "name": "get_dates",
        "description": "Retrieves the days of the week that a course is on.",
        "parameters": {
            "type": "object",
            "properties": {
                "crn": {
                    "type": "string",
                    "description": "Unique course reference number to that section of the course"
                }
            },
            "required": ["crn"]
        }
    },
    {
        "name": "get_times",
        "description": "Retrieves the time of day a course is on.",
        "parameters": {
            "type": "object",
            "properties": {
                "crn": {
                    "type": "string",
                    "description": "Unique course reference number to that section of the course"
                }
            },
            "required": ["crn"]
        }
    },
    {
        "name": "read_schedule",
        "description": "Returns the current schedule where courses are denoted by course key.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "add_to_schedule",
        "description": "Adds a course to the schedule by course key. Returns whether the add is valid or invalid.",
        "parameters": {
            "type": "object",
            "properties": {
                "crn": {
                    "type": "string",
                    "description": "Course crn that includes information about the section of a course"
                }
            },
            "required": ["crn"]
        }
    },
    {
        "name": "remove_from_schedule",
        "description": "Removes a course from the schedule given its course key.",
        "parameters": {
            "type": "object",
            "properties": {
                "crn": {
                    "type": "string",
                    "description": "Course key or subjectCourse string, e.g., CS010A or MATH011"
                }
            },
            "required": ["crn"]
        }
    }
]

# Convert to FunctionDeclaration objects
function_declarations = []

for decl in tool_declarations:
    param_schema = decl.get("parameters", {})
    properties = {
        name: types.Schema(
            type=prop["type"],
            description=prop.get("description", "")
        )
        for name, prop in param_schema.get("properties", {}).items()
    }

    function_declarations.append(
        types.FunctionDeclaration(
            name=decl["name"],
            description=decl["description"],
            parameters=types.Schema(
                type=param_schema.get("type", "object"),
                properties=properties,
                required=param_schema.get("required", [])
            )
        )
    )

