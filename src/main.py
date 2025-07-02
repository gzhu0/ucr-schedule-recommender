from google import genai
from google.genai import types
from src.tools.tool_declerations import function_declarations
import src.tools.tools
import time

client = genai.Client(api_key="AIzaSyCWETNe6zUn0lS8CQQw8vJjjXHhQ0qHQjc")

tools = types.Tool(function_declarations=function_declarations)
config = types.GenerateContentConfig(tools=[tools])

# Initial user message
messages = [
    types.Content(
        role="model",
        parts=[
            types.Part(text='''
                You are an AI scheculing assistant at a university. Your goal is to construct a schedule based on the user's 
                courses and the major required courses. Courses have two attributes: 
                    - Course Keys, which denote a unique type of course
                    - Course Reference Numbers(CRNs) which denote a specific section of a course. CRNs can include different types
                    of sections, such as lectureres, labs, discussions, etc. 
                                
                This is the proccess for adding a specific course to a schedule:
                       1. Use tools to find all associated CRNs with a course
                       2. Use tools to find information on all the CRNs
                       3. Add CRNs to the schedule. For each course, you should add one of each type of 
                       section and ensure that there are no time conflicts. 
''')
        ]
    ),
    types.Content(role="user", parts=[types.Part(text="Add CS010A to my schedule")])
]

while True:
    time.sleep(3)
    # Send current conversation to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config,
    )

    reply = response.candidates[0].content
    part = reply.parts[0]

    if hasattr(part, "function_call") and part.function_call:
        # Tool call made
        tool_call = part.function_call
        tool_name = tool_call.name
        tool_args = tool_call.args

        # Dynamically run tool function
        result = getattr(src.tools.tools, tool_name)(**tool_args)

        # Wrap if not already a dict
        safe_result = result if isinstance(result, dict) else {"result": result}

        # Generate function response part
        function_response_part = types.Part.from_function_response(
            name=tool_name,
            response=safe_result
        )

        # Ensure result is a dictionary (required by Gemini)
        if not isinstance(result, dict):
            result = {"result": result}

        # Use in Part.from_function_response
        function_response_part = types.Part.from_function_response(
            name=tool_name,
            response=result
        )

        print(f"📦 Tool `{tool_name}` result:\n{result}")

        # Append both tool call and function result
        messages.append(reply)
        messages.append(
            types.Content(
                role="function",
                parts=[types.Part.from_function_response(name=tool_name, response=result)]
            )
        )
    else:
        print(src.tools.tools.schedule)
        # No tool call → final answer or question to user
        print(f"\n🤖 Gemini: {part.text}")

        # Get user feedback (you can replace input() with predefined strings in tests)
        user_input = input("\n🧑 You: ")

        # Add it to the message list
        messages.append(
            types.Content(role="user", parts=[types.Part(text=user_input)])
        )