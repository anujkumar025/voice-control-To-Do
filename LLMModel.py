from ollama import chat
from ollama import ChatResponse
import re

def extract_python_code(input_str: str) -> str:
    # Match code blocks with optional language specification
    # print(input_str)
    code_blocks = re.findall(r'```python\n(.*?)```', input_str, re.DOTALL)
    
    if not code_blocks:
        # Try matching any code block without language specifier
        code_blocks = re.findall(r'```\n(.*?)```', input_str, re.DOTALL)
    
    if code_blocks:
        # Get the last code block (assuming the desired code is last), strip whitespace
        return code_blocks[-1].strip()
    return ""

def get_structured_command(request: str) -> str:
    prompt = """You are an assistant that converts natural language task management requests into exact Python function calls using only the following functions:

    1. add_task(task: str, time_str: str (in format HH:MM:SS))
    - Appends a new task in the format: time, task, Not Done to tasks.txt and then calls sort_tasks().

    2. mark_task_done(index: int)
    - Marks the task at the given 1-based index as done by replacing "Not Done" with "Done" in tasks.txt.

    3. mark_task_undone(index: int)
    - Marks the task at the given 1-based index as not done by replacing "Done" with "Not Done" in tasks.txt.

    4. modify_time(index: int, new_t: str)
    - Changes the time of the task at the given index to the new time (HH:MM:SS) and then calls sort_tasks().

    5. modify_task_description(index: int, new_value: str)
    - Updates the description of the task at the given index, preserving its original time and status.

    6. delete_task(index: int)
    - Deletes the task at the given index from tasks.txt and then calls sort_tasks().

    When given a command, you must:
    - Analyze the current state of tasks.txt (provided below) to determine the appropriate task index if needed.
    - Only output the exact Python function call(s) needed to fulfill the command.
    - Do not include any commentary, explanation, or extra text.
    - Do not output calls to any functions that do not exist (for example, do NOT use get_task_index()).

    Output should be in the format:
    remember wrap function call in ```python, ``` just as shown below.
    for adding a task:
    ```python
    add_task(task="solve leetcode question", time_str="17:00:00")
    ```,
    for marking a task done:
    ```python
    mark_task_done(index=1)
    ```,
    for marking a task undone:
    ```python
    mark_task_undone(index=1)
    ```,
    for modifying a task description:
    ```python
    modify_task_description(index=1, new_value="New task")
    ```,
    for modify a time of a task:
    ```python
    modify_time(index=1, new_t="17:00:00")
    ```,
    for delete a task:
    ```python
    delete_task(index=1)
    ```"""
    tprompt = prompt
    tprompt = tprompt + "\nexample ended here now you will get real input\ncurrent state of tasks.txt is: \n"
    with open('tasks.txt', 'r') as file:
        for line in file:
            line = line.strip()
            tprompt = tprompt + line + "\n"

    tprompt = tprompt + "\nanalyze the command and use the appropriate task description: \n" + request
    # print(tprompt)

    response: ChatResponse = chat(model='deepseek-r1:7b', messages=[
        {
            'role': 'system',
            'content': tprompt
        }
    ])

    # print(response.message.content, "\n\n")
    print("Extracting python code")

    filtered_str = extract_python_code(response.message.content)

    return filtered_str
