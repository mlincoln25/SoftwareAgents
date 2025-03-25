import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from memory_manager import get_recent_snippets, add_snippet


def handle_task(instruction):
    recent_snippets = get_recent_snippets(2)
    context = '\n\n'.join(recent_snippets)

    messages = [
        {
            'role': 'system',
            'content': (
                'Write code as requested in the most reasonable language as requested by the user. You should only print out the final code and nothing else.'
                'Do not include any comments or apostrophes.'
            )
        },
        {'role': 'user', 'content': f"Recent code context:\n{context}\n\nTask: {instruction}"}
    ]

    response = client.chat.completions.create(model=os.getenv('MODEL_NAME'),
    messages=messages)

    generated_code = response.choices[0].message.content
    add_snippet(generated_code)

    return generated_code
