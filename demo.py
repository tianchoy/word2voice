from openai import OpenAI, APIError, APITimeoutError
client = OpenAI()

try:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )
    print(completion['choices'][0]['message']['content'])
    result = completion['choices'][0]['message']['content']

except APITimeoutError as err:
    print(f"openAI API Timeout Error: {err}")
except APIError as err:
    print(f"openAI API Error: {err}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")