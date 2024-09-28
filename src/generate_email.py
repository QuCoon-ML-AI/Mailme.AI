import os
import json
from openai import OpenAI

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# style_dict = {
#     "formal": "",
#     "informal": "",
#     "friendly": "",
# }

def function_tool(system_prompt):
    generate_email_tool = [
        {
            'type': 'function',
            'function': {
                'name': 'extract_email_details',
                'description': 'Extract/Generate a subject/theme and body for an email from the provided text. Ignore all email addresses in the text.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'subject': {
                            'type': 'string',
                            'items': {
                                'type': 'string',
                            },
                            'description': 'The subject of the email extracted from the text. If multiple emails are found, do not personalise the email. And do not include any extra information. Only details from the text.  Do not leave any template to be filled. Generate a complete and thorough body of the email with the context you have."'
                        },
                        'body': {
                            'type': 'string',
                            'items': {
                                'type': 'string',
                            },
                            'description': 'A fully formatted body of the email with the appropriate greetings and closings.'
                        }
                    }
                },
                'required': ['subject', 'body']
            },
            'instruction': system_prompt
        }
    ]    

    return generate_email_tool

def system_prompt(style):
    return f"""
            You are a very experienced Personal Assistant with expertise in drafting out {style} emails to from conversations.
            Generate an appropriate subject line and body for the text of the conversation provided.  Do not leave any template to be filled.
            Generate a complete and thorough email with the context you have.
            """

def generate_email(style, prompt):
    system_prompt = system_prompt(style)
    generate_email_tool = function_tool(system_prompt)
    completion = client.chat.completions.create(
        temperature=0.5,
        model="gpt-4o",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}],
        tools=generate_email_tool,
        tool_choice='required',
    )

    response = completion.choices[0].message.tool_calls[0].function.arguments
    response = json.loads(response)
    return response

    