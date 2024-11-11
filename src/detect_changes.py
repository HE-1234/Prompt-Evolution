import json
from openai import OpenAI
import csv
import pandas as pd

client = OpenAI(
    base_url="http://pyxis.ics.uci.edu:50000/v1",
    api_key="lm-studio"
)

def get_data():
    with open("./filtered_data/changes.json") as f:
        return json.load(f)


def call_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="TechxGenus/Meta-Llama-3-70B-Instruct-AWQ",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        top_p=1,
        max_tokens=5000)
    return response.choices[0].message.content


SYSTEM_PROMPT = """
You are an expert in text processing and analysis.
"""

USER_PROMPT = """
Given two arrays of strings, namely "old" and "new". The "new" array is a modified version of the "old" array. The modifications that can happen are:

1. A string is added to the "new" array
2. A string is removed from the "old" array
3. A string is changed from the "old" array to the "new" array. 

*TASK:*
1. Compare these two arrays of strings and return only the strings that are changed from the "old" array to the "new" array (modification #3).
2. Summarize the change 

*CONSIDERATIONS:*

1. Multiple modifications can happen at the same time
2. The order of the strings in the "old" and "new" array can be different.
3. Do not count whitespace ONLY changes as modification #3.
4. Changes are one-to-one which means that a modified string in the "new" array can be mapped to one and only one string in the "old" array.
5. The output format should be json in a markdown. If no such change are found return "[]". Do not output any text before or after the json markdown:

*OUTPUT_FORMAT:*

[
    {"old": "The old version of the string", "new": "The modified version of the old string", "summary": "summary of the change"},
    {"old": "The old version of the string", "new": "The modified version of the old string", "summary": "summary of the change"}
]

*INPUT:*
%DATA%

*OUTPUT:*
"""

GOOD_PROMPT = """
You are given two arrays of prompt strings, namely "old_prompts" and "new_prompts". The "new_prompts" can contain modified version of the prompts in the "old_prompts" as well as other prompts.


Your task is to compare the two arrays of prompts and check if there is a modified version of a prompt in "old_prompts" exists in "new_prompts", record it, and briefly summarize the change. Do not record whitespace-only changes.
Note that the modifications are one-to-one which means that a modified prompt in the "new_prompts" array can be mapped to ONE and ONLY ONE prompt in the "old_prompts".

Some of the changes can be:
* Reformatting the structure of the prompt
* Replacing or changing of the words
* Rephrasing the sentences
* Expanding the instructions
* Adding or Removing examples
...

The output format should be json in a markdown. If no such change are found return "[]".
DO NOT output any text or note before or after the json markdown even when the output is empty:

[
    {"old": "The old version of the prompt", "new": "The modified version of the old prompt", "summary": "summary of the change"},
    {"old": "The old version of the prompt", "new": "The modified version of the old prompt", "summary": "summary of the change"}
]

Here are some examples:

1)
old_prompts: ['Context:\nPhotosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy.\nstatement_1: Albert Einstein was a genius.\nAnswer:\n[\n     {{\n        \"statement_1\": \"Albert Einstein was a genius.\",\n        \"reason\": \"The context and statement are unrelated\"\n        \"verdict\": \"No\"\n    }}\n]\n\n\n\n']
new_prompts: ['Context:\nPhotosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy.\nstatement_1: Albert Einstein was a genius.\nAnswer:\n[\n     {{\n        \"statement_1\": \"Albert Einstein was a genius.\",\n        \"reason\": \"The context and statement are unrelated\"\n        \"verdict\": \"No\"\n    }}\n]\n\nContext:\nAlbert Einstein was a German-born theoretical physicist who is widely held to be one of the greatest and most influential scientists of all time.\nstatement_1: Nil\nAnswer:\n[\n     {{\n        \"statement_1\": \"Nil\",\n        \"reason\": \"The statement is invalid\",\n        \"verdict\": \"No\"\n    }}\n]\n\n\n\n']

Output:
```
[
    {
        "old": "{old_prompt}",
        "new": "{new_prompt}",
        "summary": " A new context about Albert Einstein was added along with a statement and answer section, introducing a 'Nil' statement with a verdict and reason."
    }
]
```

2)
old_prompts: ['You are a helpful assistant, you will use the provided context to answer user questions.\nRead the given context before answering questions and think step by step. If you can not answer a user question based on \nthe provided context, inform the user. Do not use any other information for answering user']
new_prompts: ['You are a helpful assistant, you will use the provided context to answer user questions.\nRead the given context before answering questions and think step by step. If you can not answer a user question based on \nthe provided context, inform the user. Do not use any other information for answering user. Provide a detailed answer to the question.']

Ouput:
```
[
    {
        "old": "{old_prompt}",
        "new": "{new_prompt}",
        "summary": "The prompt was modified by adding 'Provide a detailed answer to the question' to the instruction."
    }
]
```


*Input:*

old_prompts: %OLD%
new_prompts: %NEW%

Output:
"""


TEMP_PROMPT = """
You are given two arrays of prompt strings, namely "old_prompts" and "new_prompts". The "new_prompts" can contain modified version of the prompts in the "old_prompts" as well as other prompts.

Your task is to compare the two arrays of prompts and check if there is a modified version of a prompt in "old_prompts" exists in "new_prompts", record it, and briefly summarize the change. Do not record whitespace-only changes.
Note that the modifications are one-to-one which means that a modified prompt in the "new_prompts" array can be mapped to ONE and ONLY ONE prompt in the "old_prompts".

The output format should be json in a markdown. If no such change are found return "[]". Do not output any text before or after the json markdown:

[
    {"old": "The old version of the prompt", "new": "The modified version of the old prompt", "summary": "summary of the change"},
    {"old": "The old version of the prompt", "new": "The modified version of the old prompt", "summary": "summary of the change"}
]


*Input:*

old_prompts: ['\n    Your role is to create synthetic text based on de-identified text with placeholders instead of personally identifiable information.\n    Replace the placeholders (e.g. , , {DATE}, {ip_address}) with fake values.\n\n    Instructions:\n\n    Use completely random numbers, so every digit is drawn between 0 and 9.\n    Use realistic names that come from diverse genders, ethnicities and countries.\n    If there are no placeholders, return the text as is and provide an answer.\n    input: How do I change the limit on my credit card {credit_card_number}?\n    output: How do I change the limit on my credit card 2539 3519 2345 1555?\n    input: PLACEHOLDER\n    output:\n    ', '\n    Your role is to create synthetic text based on de-identified text with placeholders instead of personally identifiable information.\n    Replace the placeholders (e.g. , , {DATE}, {ip_address}) with fake values.\n\n    Instructions:\n\n    Use completely random numbers, so every digit is drawn between 0 and 9.\n    Use realistic names that come from diverse genders, ethnicities and countries.\n    If there are no placeholders, return the text as is and provide an answer.\n    input: How do I change the limit on my credit card {credit_card_number}?\n    output: How do I change the limit on my credit card 2539 3519 2345 1555?\n    input: PLACEHOLDER\n    output:\n    ']

new_prompts: ['\n    Your role is to create synthetic text based on de-identified text with placeholders instead of Personally Identifiable Information (PII).\n    Replace the placeholders (e.g. ,<PERSON>, {DATE}, {ip_address}) with fake values.\n\n    Instructions:\n\n    a. Use completely random numbers, so every digit is drawn between 0 and 9.\n    b. Use realistic names that come from diverse genders, ethnicities and countries.\n    c. If there are no placeholders, return the text as is and provide an answer.\n    d. Keep the formatting as close to the original as possible.\n    e. If PII exists in the input, replace it with fake values in the output.\n    \n    input: How do I change the limit on my credit card {credit_card_number}?\n    output: How do I change the limit on my credit card 2539 3519 2345 1555?\n    input: <PERSON> was the chief science officer at <ORGANIZATION>.\n    output: Katherine Buckjov was the chief science officer at NASA.\n    input: Cameroon lives in <LOCATION>.\n    output: Vladimir lives in Moscow.\n    input: PLACEHOLDER\n    output:\n    ', '\n    Your role is to create synthetic text based on de-identified text with placeholders instead of Personally Identifiable Information (PII).\n    Replace the placeholders (e.g. ,<PERSON>, {DATE}, {ip_address}) with fake values.\n\n    Instructions:\n\n    a. Use completely random numbers, so every digit is drawn between 0 and 9.\n    b. Use realistic names that come from diverse genders, ethnicities and countries.\n    c. If there are no placeholders, return the text as is and provide an answer.\n    d. Keep the formatting as close to the original as possible.\n    e. If PII exists in the input, replace it with fake values in the output.\n    \n    input: How do I change the limit on my credit card {credit_card_number}?\n    output: How do I change the limit on my credit card 2539 3519 2345 1555?\n    input: <PERSON> was the chief science officer at <ORGANIZATION>.\n    output: Katherine Buckjov was the chief science officer at NASA.\n    input: Cameroon lives in <LOCATION>.\n    output: Vladimir lives in Moscow.\n    input: PLACEHOLDER\n    output:\n    ', '\n    Your role is to create synthetic text based on de-identified text with placeholders instead of Personally Identifiable Information (PII).\n    Replace the placeholders (e.g. ,<PERSON>, {DATE}, {ip_address}) with fake values.\n\n    Instructions:\n\n    a. Use completely random numbers, so every digit is drawn between 0 and 9.\n    b. Use realistic names that come from diverse genders, ethnicities and countries.\n    c. If there are no placeholders, return the text as is and provide an answer.\n    d. Keep the formatting as close to the original as possible.\n    e. If PII exists in the input, replace it with fake values in the output.\n    \n    input: How do I change the limit on my credit card {credit_card_number}?\n    output: How do I change the limit on my credit card 2539 3519 2345 1555?\n    input: <PERSON> was the chief science officer at <ORGANIZATION>.\n    output: Katherine Buckjov was the chief science officer at NASA.\n    input: Cameroon lives in <LOCATION>.\n    output: Vladimir lives in Moscow.\n    input: PLACEHOLDER\n    output:\n    ']
"""

prompts = []

if __name__ == '__main__':

    csv_results = []
    """
    {project_file, commit, old, new}
    """

    changes_data = get_data()

    for key in changes_data:
        if len(changes_data[key]) > 0:
            


            changes = changes_data[key]
            for change in changes:
                if len(change['old']) > 0 and len(change['new']) > 0:
                    old_set = set(change['new'])
                    new_set = set(change['old'])

                    common_elements = old_set.intersection(new_set)

                    unique_old_set = old_set - common_elements
                    unique_new_set = new_set - common_elements

                    if len(unique_old_set) > 0 and len(unique_new_set) > 0:
                        final_prompt = GOOD_PROMPT.replace("%OLD%", str(list(unique_old_set))).replace('%NEW%', str(list(unique_new_set)))
                        csv_results.append({ "project_file": key, "commit": change['commit_id'], "old": unique_old_set, "new":  unique_new_set})
                        prompts.append(final_prompt)


print(len(prompts))

df = pd.DataFrame(csv_results)
print(df.head())
df.to_csv("hello.csv")

# print(csv_results)

# sample_prompt = prompts[270]
# print(sample_prompt)

# print(call_llm("You are a helpful assistant", "Who are you"))

# data = call_llm(SYSTEM_PROMPT, sample_prompt)
# print(data)

        
        