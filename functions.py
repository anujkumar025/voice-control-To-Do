import datetime


def sort_tasks() -> None:
    tasks = []

    # Read all tasks from the file
    try:
        with open('tasks.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Split time and task
                    time_str, task_str = line.split(',', 1)
                    # Convert time string to time object
                    time_obj = datetime.datetime.strptime(time_str.strip(), "%H:%M:%S").time()
                    tasks.append((time_obj, task_str.strip()))
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return
    
    # Sort tasks by time in ascending order
    tasks.sort(key=lambda x: x[0])

    # Write the sorted tasks back to the file
    with open('tasks.txt', 'w') as file:
        for time_obj, task_str in tasks:
            time_str = time_obj.strftime("%H:%M:%S")
            file.write(f"{time_str}, {task_str}\n")

    # print("Tasks sorted successfully ✅")


def add_task(task: str, time_str: str) -> None:
    # Add the new task to the file
    reminding_time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    with open('tasks.txt', 'a') as file:
        file.write(f"{reminding_time.strftime('%H:%M:%S')}, {task}, Not Done\n")

    # Sort tasks after adding
    sort_tasks()

    print("Tasks added successfully ✅")


def mark_task_done(index: int) -> None:
    tasks = []

    # Read all tasks from the file
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return
    
    # Ensure the index is valid
    if index < 1 or index > len(tasks):
        print(f"Error: Invalid index {index}. Must be between 1 and {len(tasks)}.")
        return

    # Process the task: Remove "Not Done" and add "Done"
    task_line = tasks[index - 1].strip()
    if ", Done" in task_line:
        return
    task_line = task_line.replace(", Not Done", "").replace(" Not Done", "")  # Remove "Not Done"
    task_line += ", Done"  # Append "Done"

    tasks[index - 1] = task_line + "\n"

    # Write the updated tasks back to the file
    with open('tasks.txt', 'w') as file:
        file.writelines(tasks)

    print(f"Task {index} marked as Done ✅")


def mark_task_undone(index: int) -> None:
    tasks = []

    # Read all tasks from the file
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return
    
    # Ensure the index is valid
    if index < 1 or index > len(tasks):
        print(f"Error: Invalid index {index}. Must be between 1 and {len(tasks)}.")
        return

    # Process the task: Remove "Done" and add "Done"
    task_line = tasks[index - 1].strip()
    if ", Not Done" in task_line:
        return 
    task_line = task_line.replace(", Done", "").replace(", Done", "") # Remove "Done"
    task_line += ", Not Done"  # Append "Not Done"

    tasks[index - 1] = task_line + "\n"

    # Write the updated tasks back to the file
    with open('tasks.txt', 'w') as file:
        file.writelines(tasks)

    print(f"Task {index} marked as Done ✅")


def modify_time(index: int, new_t: str) -> None:
    tasks  = []
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return

    if index < 1 or index > len(tasks):
        print(f"Error: Invalid index {index}. Must be between 1 and {len(tasks)}.")
        return

    task_line = tasks[index - 1].strip()
    try:
        new_time = datetime.datetime.strptime(new_t, "%H:%M:%S").time()
        parts = task_line.split(',', 1)  # Split once to avoid breaking task description
        task_line = f"{new_time.strftime('%H:%M:%S')},{parts[1]}"
        tasks[index - 1] = task_line + "\n"

        with open('tasks.txt', 'w') as file:
            file.writelines(tasks)

        sort_tasks()
        print(f"Task {index} time changed successfully ✅")

    except ValueError:
        print("Error: Invalid time format. Use HH:MM:SS")
        return
    

def modify_task_description(index: int, new_value: str) -> None:
    tasks  = []
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return

    if index < 1 or index > len(tasks):
        print(f"Error: Invalid index {index}. Must be between 1 and {len(tasks)}.")
        return

    task_line = tasks[index - 1].strip()

    parts = task_line.split(',', 1)
    task_status = ", Done" if "Done" in task_line else ", Not Done"
    task_line = f"{parts[0]}, {new_value}{task_status}"
    tasks[index - 1] = task_line + "\n"

    with open('tasks.txt', 'w') as file:
        file.writelines(tasks)
    
    print(f"Task {index} description changed successfully ✅")


def delete_task(index: int) -> None:
    tasks = []

    # Read all tasks from the file
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
    except FileNotFoundError:
        print("Error: tasks.txt not found.")
        return
    
    # Ensure the index is valid
    if index < 1 or index > len(tasks):
        print(f"Error: Invalid index {index}. Must be between 1 and {len(tasks)}.")
        return

    # Remove the specified task
    deleted_task = tasks.pop(index - 1).strip()

    # Write the updated tasks back to the file
    with open('tasks.txt', 'w') as file:
        file.writelines(tasks)

    # Sort the tasks after deletion
    sort_tasks()

    print(f"Task {index} deleted successfully ✅")