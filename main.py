import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import SYSTEM_PROMPT, MAX_LOOPS
from call_function import available_functions, call_function


def main():

    # Set up LLM
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API KEY NOT FOUND!!!")
    client = genai.Client(api_key=api_key)
    system_prompt = SYSTEM_PROMPT

    
    
    # Set up args
    parser =  argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args  = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(MAX_LOOPS):

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

        if _ == (MAX_LOOPS - 1):
            print("Error: Ran out of loops!")
            exit(1)


if __name__ == "__main__":
    main()
