import os
import openai
from memory_manager import get_recent_snippets, add_snippet

openai.api_key = os.getenv('OPENAI_API_KEY')

def handle_task(instruction):
    recent_snippets = get_recent_snippets(2)
    context = '\n\n'.join(recent_snippets)

    messages = [
        {
            'role': 'system',
            'content': (
                'You are a senior software developer. Given a task and recent code context, '
                'produce code.'
            )
        },
        {'role': 'user', 'content': f"Recent code context:\n{context}\n\nTask: {instruction}"}
    ]

    response = openai.ChatCompletion.create(
        model='gpt-4-turbo',
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )

    generated_code = response.choices[0].message.content
    add_snippet(generated_code)

    return generated_code
