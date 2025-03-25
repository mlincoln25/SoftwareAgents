import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def review_code(code):
    messages = [
        {
            'role': 'system',
            'content': (
                'You are a senior code reviewer. Examine the following code for correctness, '
                'efficiency, and best practices. Provide necessary improvements. Your response '
                'should contain only runnable code. Anything non-code should be in comments.'
            )
        },
        {'role': 'user', 'content': code}
    ]

    response = client.chat.completions.create(
        model=os.getenv('MODEL_NAME'),
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content
