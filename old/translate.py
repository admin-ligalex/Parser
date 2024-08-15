from openai import OpenAI

# Убедитесь, что у вас установлен правильный API-ключ
#OpenAI.api_key = "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"


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)