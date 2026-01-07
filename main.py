import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """ 

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, 
                               schema_get_file_content, 
                               schema_run_python_file, 
                               schema_write_file],
    )
    
    # Set up args
    parser =  argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args  = parser.parse_args()

    # Process user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt),
        )

    # Display resutls
    if response.usage_metadata == None:
        raise RuntimeError("No usage_metadata!!")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if len(response.function_calls) != 0:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    print(response.text)


if __name__ == "__main__":
    main()
