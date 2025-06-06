from openai import AzureOpenAI
 
client = AzureOpenAI(
    azure_endpoint="https://everi-openai-poc.openai.azure.com/",
    api_key="737c3561b0bb4717bfc0d17e97ee6653",
    api_version="2024-08-01-preview"
)
 
sampling_params = {
    'max_tokens': 16384,
    "temperature": 0.2,
    "top_p": 0.9,
    "n": 1,
    "frequency_penalty": 0.7,
    "presence_penalty": 0.4,
}
 
# File contents
file1_name = "main.py"
file1_content = '''
# main.py
 
from utils import greet_user
 
name = input("Enter your name: ")
greet_user(name)
'''
 
file2_name = "utils.py"
file2_content = '''
# utils.py
 
def greet_user(name):
    print(f"Hello, {name}!")
'''
 
# Step 1: Initial prompt (pass only main.py)
task_instruction = """
You are a code analysis assistant.
 
Your task is to:
1. Detect if this file depends on any external or local modules.
2. Return a list of missing or unresolved imports or dependencies.
 
Just provide dependency analysis. Do not attempt to validate correctness yet.
"""
 
step1_response = client.chat.completions.create(
    model="gpt-4o-mini-code-review",
    messages=[
        {"role": "system", "content": task_instruction},
        {"role": "user", "content": f"Filename: {file1_name}\n\n{file1_content}"}
    ],
    **sampling_params
)
 
dependency_report = step1_response.choices[0].message.content
print("Step 1 - Dependency Report:\n", dependency_report)
 
# Step 2: Check if it mentions the dependency on "utils"
if "utils" in dependency_report:
    print("\nDependency on 'utils' found. Sending both files for full analysis...\n")
 
    full_analysis_instruction = """
You are a code analysis assistant.
 
Now that all dependent files are available, your task is to:
1. Check for any syntax or logic errors across all provided files.
2. Consider imported functions, modules, or classes across files.
3. Only report real errors, not false positives due to missing context.
 
Return a structured report of issues, if any.
"""
 
    all_files_message = f"Filename: {file1_name}\n{file1_content}\n\nFilename: {file2_name}\n{file2_content}"
 
    step2_response = client.chat.completions.create(
        model="gpt-4o-mini-code-review",
        messages=[
            {"role": "system", "content": full_analysis_instruction},
            {"role": "user", "content": all_files_message}
        ],
        **sampling_params
    )
 
    print("Step 2 - Full Analysis:\n", step2_response.choices[0].message.content)
else:
    print("\nNo dependencies detected. Proceed with file1 only.")
 
 
