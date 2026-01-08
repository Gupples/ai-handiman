import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def main():

    # Set up LLM
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API KEY NOT FOUND!!!")
    client = genai.Client(api_key=api_key)
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """ 

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, 
                               schema_get_file_content, 
                               schema_run_python_file, 
                               schema_write_file],
    )

    def call_function(function_call, verbose=False):
        if verbose:
            print (f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(f" - Calling function: {function_call.name}")
        function_map = {
            "get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "run_python_file": run_python_file,
            "write_file": write_file,
        }
        function_name = function_call.name or ""
        if function_name not in function_map:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator"
        function_result = function_map[function_name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    
    # Set up args
    parser =  argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args  = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):

        # Call the model and process user prompt
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt),
            )
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Display results
        if response.usage_metadata == None:
            raise RuntimeError("No usage_metadata!!")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if not response.function_calls:
            print(response.text)
            return
        else:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if len(function_call_result.parts) == 0:
                    raise Exception("Empty .parts list!")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Function response is None!")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Function_response.response is None!")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))

        if _ == 19:
            print("Error: Ran out of loops!")
            exit(1)


if __name__ == "__main__":
    main()
