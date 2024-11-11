import json
from openai import OpenAI
import csv
import pandas as pd
import importlib
import qa_prompts
import re

INCONSISTENCY_ANALYSIS_SYSTEM_PROMPT = qa_prompts.INCONSISTENCY_ANALYSIS_SYSTEM_PROMPT
INCONSISTENCY_ANALYSIS_USER_PROMPT = qa_prompts.INCONSISTENCY_ANALYSIS_USER_PROMPT

client = OpenAI(
    base_url="http://pyxis.ics.uci.edu:50000/v1",
    api_key="lm-studio"
)

def call_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="TechxGenus/Meta-Llama-3-70B-Instruct-AWQ",
        # model="casperhansen/llama-3-8b-instruct-awq",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        top_p=1,
        # max_tokens=5000
        )
    return response.choices[0].message.content


def parse_output(output):
    code_string = ""
    for code in output:
        code_string += code['Part'] + ' ' + code['Code'] + '\n'
    return code_string

def extract_output(response):
    json_string = extract_json(response)
    if json_string:
        try:
            output = json.loads(json_string)
            return output
        except:
            return None
    else:
        return None

def extract_json(text):
    pattern = r'```json\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)  # re.DOTALL allows matching across multiple lines
    if match:
        return match.group(1)  # Group 1 is the text between the template
    else:
        return None  # Return None if no match is found


if __name__ == '__main__':
    df = pd.read_csv('full.csv')
    inconsistencies = []


    for index, row in df.iterrows():
        print(f"Processing row {index}")
        original_prompt = row['old']
        modified_prompt = row['new']
        system_prompt = INCONSISTENCY_ANALYSIS_SYSTEM_PROMPT
        user_prompt = INCONSISTENCY_ANALYSIS_USER_PROMPT

        try:
            result = call_llm(system_prompt, user_prompt.format(original_prompt=original_prompt, modified_prompt=modified_prompt))
            output = extract_output(result)
            print(output)
            if output['inconsistency'] == 'True':
                inconsistencies.append({
                    'project_file': row['project_file'],
                    'commit': row['commit'],
                    'commit_message': row['commit_message'],
                    'date': row['date'],
                    'old': row['old'],
                    'new': row['new'],
                    'similarity': row['similarity'],
                    'inconsistency_reason': output['reasoning']
                    })
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
    new_df = pd.DataFrame(inconsistencies)
    new_df.to_csv('inconsistencies.csv', index=False)