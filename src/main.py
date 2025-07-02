from google import genai
from google.genai import types

from src.tools.tool_declerations import function_declarations
import src.tools.tools

client = genai.Client(api_key="AIzaSyCWETNe6zUn0lS8CQQw8vJjjXHhQ0qHQjc")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)

# Configure the client and tools
tools = types.Tool(function_declarations=[function_declarations][0])
config = types.GenerateContentConfig(tools=[tools])

# Declare contents
contents=types.Content(
        role = "user", parts = [types.Part(text="Add a lecture and lab crn from CS010A to the schedule")]
    )

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents,
    config=config,
)
tool_call = response.candidates[0].content.parts[0].function_call
print(tool_call)

if tool_call.name == "add_to_schedule":
    result = src.tools.tools.add_to_schedule(**tool_call.args)
    print(f"Function execution result: {result}")

print(src.tools.tools.schedule)

# Create a function response part
function_response_part = types.Part.from_function_response(
    name=tool_call.name,
    response={"result": result},
)

# Append function call and result of the function execution to contents
contents.append(response.candidates[0].content) # Append the content from the model's response.
contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response

final_response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=config,
    contents=contents,
)

print(final_response.text)