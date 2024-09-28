import os
import json
from openai import OpenAI
from datetime import datetime

# Get Configuration Settings
from dotenv import load_dotenv
load_dotenv() 

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# style_dict = {
#     "formal": "",
#     "informal": "",
#     "friendly": "",
# }

def function_tool_email(system_prompt):
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

def function_tool_address(system_prompt):
    generate_address_tool = [
        {
            'type': 'function',
            'function': {
                'name': 'extract_address_details',
                'description': 'Extract/Generate address details from the provided text. Ignore any extra information not related to the address.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'address_line_1': {
                            'type': 'string',
                            'description': 'The primary address line containing the street name and house number or apartment number.'
                        },
                        'city': {
                            'type': 'string',
                            'description': 'The city associated with the address.'
                        },
                        'state': {
                            'type': 'string',
                            'description': 'The state or region associated with the address.'
                        },
                        'country': {
                            'type': 'string',
                            'description': 'The country associated with the address.'
                        }
                    }
                },
                'required': ['address_line_1', 'city', 'state']
            },
            'instruction': system_prompt
        }

    ]    

    return generate_address_tool

def system_prompt_email(style):
    return f"""
            You are a very experienced Personal Assistant with expertise in drafting out {style} emails to from conversations.
            Generate an appropriate subject line and body for the text of the conversation provided.  Do not leave any template to be filled.
            Generate a complete and thorough email with the context you have.
            """

def system_prompt_address():
    return f"""
            You are a very experienced Personal Assistant with expertise in extracting address details from any provided text. 
            Your task is to generate the following details from the text you are given: 
            - Address Line 1 (street name and house or apartment number)
            - City
            - State
            - Country (optional)
            
            Ensure that all required information is extracted thoroughly and accurately. Ignore any extra information not related to the address.
            """

def generate_email(style, prompt):
    system_prompt = system_prompt_email(style)
    generate_email_tool = function_tool_email(system_prompt)
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

def generate_address(prompt):
    system_prompt = system_prompt_address()
    generate_address_tool = function_tool_address(system_prompt)
    completion = client.chat.completions.create(
        temperature=0.5,
        model="gpt-4o",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}],
        tools=generate_address_tool,
        tool_choice='required',
    )

    response = completion.choices[0].message.tool_calls[0].function.arguments
    response = json.loads(response)
    current_date = datetime.now()
    response["time"] = current_date.strftime("%B %d, %Y.")
    return response 