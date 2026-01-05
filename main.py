import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Hello from ai-handiman!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API KEY NOT FOUND!!!")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    if response.usage_metadata == None:
        raise RuntimeError("No usage_metadata!!")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
