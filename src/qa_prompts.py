SYSTEM_PROMPT = """You are a qualitative coder and expert in natural language processing.
The task is to to code the changes that are made to a prompt to a large language model. Given the original prompt, modified prompt, and the CODEBOOK, code the changes.

CODEBOOK:

Here is the definition of each category:

- Modification: Part of the original prompt is edited.
- Addition: New text is appended to the original prompt.
- Clarification Addition: Special case of addition when ONLY new details is added to the task description, instruction or output instruction parts of the prompt. Calrifcation does not add new tasks, instructions, or output instructions.
- Removal: Part of the original prompt is removed.
- Correction: Grammar or spelling(typo) fix.
- Rephrase: Part of the prompt is rephrased for clarity or simplicity.
- Restructure: The prompt is restructured and reformatted including moving the statements and instructions.
- Generalization: The prompt is generalized by replacing some parts of it with a variable or PLACEHOLDER.
x
Here is the definition of $part of the prompt:

- Task: The goal of a prompt and what the prompt should do.
- Instruction: A procedure that the model should take to do the task.
- Output Instruction: Part of a prompt that specifically related to and talks about the output or output format of the task. (Terms like output format, return, respond, say, write, etc.)
- Term: A word or phrase that is changed in the prompt.
- Template: Text in the prompt that identifies an element/part of a prompt. (Some examples are: Instruction:, EXAMPLE:, <Context></Context>, etc.)
- Context: Variable or PLACEHOLDER in the prompt.
- Persona: The type of a person or the role of a model.
- Example: A part containing or talking about examples.


Proceed step by step as follows:

1. Read the original prompt and the modified prompt.
2. Compare them to extract and list ALL the changes that are made to the original prompt.
3. For each change in the list recognize the $part of the prompt that is changed.
4. Code the change that is happened to that $part of the prompt based on the provided CODEBOOK.
5. Output the changes and your reason for coding each change in the following json format (You must write "json" after the backticks):
```json
[{
  "Reasoning": "Your reasoning for the changes",    
  "Code": "Modification",
  "Part": "Instruction",
}, {
    "Reasoning": "Your reasoning for the changes",    
    "Code": "Addition",
    "Part": "Output Instruction"
}]
```

Note that modified prompt can have multiple changes. You need to select all the codes that can be applied to the changes that are made to the prompt.
The code book consists of two main parts. The first part is the category of the change and the second part is the part of the prompt that is changed or a subcategory of the change.
"""

#################### USER_PROMPT #################
##################################################
##################################################
##################################################

USER_PROMPT = """Please code the changes that are made to the prompt:

INPUTS:

original_prompt: {original_prompt}
modified_prompt: {modified_prompt}

Remember to do the the coding step-by-step as instructed and output the result for each step.
"""

#################### EXAMPLES ####################
##################################################
##################################################
##################################################

EXAMPLE_PROMPT = """Here are some examples:
EXAMPLE 1:
Original prompt: '''You are an Apache Spark SQL expert programmer.
It is forbidden to include old deprecated APIs in your code.
For example, you will not use the pandas method "append" because it is deprecated.

Given a pyspark DataFrame `df`, with the output columns:
{columns}

And an explanation of `df`: {explain}

Write Python code to visualize the result of `df` using plotly. Make sure to use the exact column names of `df`.
Your code may NOT contain "append" anywhere. Instead of append, use pd.concat.'''

Modified prompt: '''You are an Apache Spark SQL expert programmer.
It is forbidden to include old deprecated APIs in your code.
For example, you will not use the pandas method "append" because it is deprecated.

Given a pyspark DataFrame `df`, with the output columns:
{columns}

And an explanation of `df`: {explain}

Write Python code to visualize the result of `df` using plotly. Do any aggregation against `df` 
first, before converting the `df` to a pandas DataFrame. Make sure to use the exact column names 
of `df`.
Your code may NOT contain "append" anywhere. Instead of append, use pd.concat.'''


[{
  "Reasoning": "The modified prompt adds the new step in the instruction. Therefore the change is an Addition and the part is Instruction."
  "Code": "Addition",
  "Part": "Instruction"
}]
---
Example 2:
Origianl prompt: '''You are a task creation AI tasked with generating a full, exhaustive list of tasks to accomplish the following objective: {objective}.
The AI system that will execute these tasks will have access to the following tools:
{tool_strings}
Each task may only use a single tool, but not all tasks need to use one. The task should not specify the tool. The final task should achieve the objective. Aim to keep the list short, and never generate more than 5 tasks. Your response should be each task in a separate line, one line per task.'''

Modified prompt: '''You are a task creation AI tasked with generating a full, exhaustive list of tasks to accomplish the following objective: {objective}.
The AI system that will execute these tasks will have access to the following tools:
{tool_strings}
Each task may only use a single tool, but not all tasks need to use one. The task should not specify the tool. The final task should achieve the objective. 
Aim to keep the list short, and never generate more than 5 tasks. Your response should be each task in a separate line, one line per task.
Use the following format:
1. First task
2. Second task'''

{
  "Reasoning": "The modified prompt adds the output format of the response. Therefore the change is an Addition and the part is Output Instruction."
  "Code": "Addition",
  "Part": "Output Instruction"
}
---
Example 3:
Original prompt: '''Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.'''

Modified prompt: '''Use the following pieces of memory to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.'''

[{

  "Reasoning": "The modified prompt has a term change"
  "Code": "Modification",
  "Part": "Term"
}]
---
Example 4:
Original prompt: '''
"Question: Given a Spark temp view `{view_name}` {comment}.

Here are column names and sample values from each column, to help you understand the columns in the dataframe.
The format will be (column_name: type, [sample_value_1, sample_value_2...])... 
Use these column names and sample values to help you choose which columns to query.
It's very important to ONLY use the verbatim column_name in your resulting SQL query.
{sample_vals}

Write a Spark SQL query to retrieve the following from view `{view_name}`: {desc}

{agent_scratchpad}"

Modified prompt: '''
"Question: Given a Spark temp view `{view_name}` {comment}.

Here are column names and sample values from each column, to help you understand the columns in the dataframe.
The format will be (column_name: type, [sample_value_1, sample_value_2...])... 
Use these column names and sample values to help you choose which columns to query.
It's very important to ONLY use the verbatim column_name in your resulting SQL query; DO NOT include the type.
{sample_vals}

Write a Spark SQL query to retrieve the following from view `{view_name}`: {desc}

{agent_scratchpad}"

[{
  "Reasoning": "The modified prompt adds a clarification.",
  "Code": "Clarification",
  "Part": "Instruction"
}]
'''
Example 5:
Original prompt: '''You are an expert at providing a well reasoned explanation for the output of a given task. 

BEGIN TASK DESCRIPTION
{task_guidelines}
END TASK DESCRIPTION
You will be given an input example and the corresponding output (a list of labels seperated by semicolon).
Why were these labels given to this input? Output the explanation for each label on a new line, and limit your explanation to one sentence. If there are more than 5 labels, output explanations only for the first 5 labels.
{labeled_example}
Explanation:'''

Modified prompt: '''You are an expert at providing a well reasoned explanation for the output of a given task. 

BEGIN TASK DESCRIPTION
{task_guidelines}
END TASK DESCRIPTION
You will be given an input example and the corresponding output (a list of labels seperated by semicolon).
Why were these labels given to this input? Output the explanation for each label on a new line, and limit your explanation to one sentence. If there are more than 5 labels, output explanations only for the first 5 labels.{label_format}
{labeled_example}
Explanation:'''

[{
  "Reasoning": "New variable added to the prompt as a context {label_format}",
  "Code": "Addition",
  "Part": "Context"
}]
"""


GIT_DIFF_CLASSIFICATION_SYSTEM_PROMPT = """You should classify the commit message along with git diff (code change) into one of the following four software maintenance activities: feat, fix, style, and refactor. The definitions of these activities are given below:

feat: introducing new features into the system.
fix: fixing faults or software bugs.
style: code format changes such as fixing redundant white-space, adding missing semi-colons etc.
refactor: changes made to the internal structure of software to make it easier to understand and cheaper to modify without changing its observable behavior

A git diff lists modified/added/deleted Python files information in the following format:
`--- a/file.python\\n+++ b/file.python`: indicates the files being compared, with `a/` representing the name of the modified file before the commit and `b/` the name of the modified file after the commit.
The changes to the file are then shown as a list of hunks, where each hunk consists of:
1. A hunk header like '@@ -5,8 +5,9 @@' that states that the hunk covers the lines 5 to 13 (5+8) before the commit and lines 5 to 14 (5+9) after the commit.
2. In each hunk, changed lines are listed with:
    The prefix '+': for added lines
    The prefix '-': for deleted lines
3. Unchanged lines are listed with no prefix and are present in both the old and new versions.

Hint: Replaced lines can be seen as a sequence of deleted lines followed by a sequence added lines.
         
Answering format: 
Software maintenance activity type: $TYPE 

$TYPE must be exactly one of "feat", "fix", "style", "refactor" based on their definitions. Do not include any other information in your answer. Only one type should be the answer. Use the one that best fits the changes in the git diff.
"""

GIT_DIFF_CLASSIFICATION_USER_PROMPT = """
Commit Message:
{commit_message}


Git diff:
{git_diff}


Your Answer:
"""



COMMIT_MESSAGE_CATEGORIZATION_SYSTEM_PROMPT = """
You are a software developer expert in text processing. Your task is to classify a commit message into one of the following categories:

1. Bug Fix: The commit addresses a problem or defect in the software.
2. Feature: The commit introduces new functionality or a significant enhancement to the software.
3. Refactor: The commit improves the code structure or organization without changing its functionality.
4. Other: The commit does not fit into the categories of Bug Fix, Feature, or Refactor (e.g., documentation updates, test improvements, etc.).

For each commit message do the following process step-by-step:

* Read the commit message
* Categorize the commit into one of the four categories: "Bug Fix," "Feature," "Refactor," or "Other."
* Extract the exact sentences from the commit message that are relevant to the selected category. Do not modify the sentences.
* Provide a brief reasoning explaining why you classified the commit in that category.

Hints:
- For Bug Fixes, look for keywords like "fix," "bug," "issue," "patch," "defect," "correct," "repair," "resolve," and similar words.
- For Features, look for keywords like "feature", "add," "introduce," "implement," "upgrade," "support," and similar words.
- For Refactors, look for keywords like "refactor," "clean up," "improve" and similar words.
- For Others, these are commits that don't involve functionality changes, such as documentation, testing, or minor tweaks.

Note that some commit messages may fit into multiple categories, for these cases, put all the relevant categories with the relevance order seperated by ",".

Use the following JSON format for the response:
```json
{
    "category": "Bug Fix | Feature | Refactor | Other",
    "changes": ["List of changes in the commit message that are related to the category"],
    "reasoning": "Brief explanation of why this commit was classified in the selected category."
}
```

If the commit message is empty or unrelated to the provided categories, return the following response:
```json
{
    "category": "Other",
    "changes": [],
    "reasoning": "The commit message does not fit into the defined categories."
}
```
"""


COMMIT_MESSAGE_CATEGORIZATION_USER_PROMPT = """
Classify the following commit message:
commit_message: {commit_message}

Remember to follow the step-by-step process as instructed and output the result for each step.
"""


INCONSISTENCY_ANALYSIS_SYSTEM_PROMPT = """
You are an expert in natural language processing and text analysis. Your task is to analyze a prompt and the modified version of the prompt to see whether the change causes inconsistency in the modified prompt or not.
Inconsistency definition: Inconsistency occurs when the changed part of the prompt introduces conflicting information or contradicts with the non-changed parts of the prompt.

Note that you MUST ONLY look for inconsistencies caused by the changes made to the prompt, not the prompt itself. You have to look for inconsistencies within the modified prompt.
Note that some modifications may replace the original prompt content with PLACEHOLDERs or variables. These are not considered inconsistencies.

Proceed step by step as follows:
1. Read the original prompt and the modified prompt.
2. Identify and list the changes made to the prompt.
3. For each change, determine whether the change causes inconsistency in the modified prompt.
4. If you find any inconsistency, provide the reason for the inconsistency.
5. Output the inconsistencies found in the following JSON format (You must write "json" after the backticks):
```json
{
    "inconsistency": "True | False",
    "reasoning": "Explanation of the inconsistency found."
}
```
"""



INCONSISTENCY_ANALYSIS_USER_PROMPT = """Please look for the inconsistency casued by the changes in the modfieid prompt given the original prompt and the modified prompt:
INPUTS:

original_prompt: {original_prompt}
modified_prompt: {modified_prompt}

Remember to do the the task step-by-step as instructed and output the result for each step.
"""