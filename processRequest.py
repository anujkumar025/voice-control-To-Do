import functions
import re
from ast import literal_eval
import LLMModel
import inspect

FUNCTIONS = {
    'add_task': functions.add_task,
    'mark_task_done': functions.mark_task_done,
    'mark_task_undone': functions.mark_task_undone,
    'modify_task_description': functions.modify_task_description,
    'modify_time': functions.modify_time,
    'sort_tasks': functions.sort_tasks,
    'delete_task': functions.delete_task,
}

def execute_user_command(command: str):
    # Match function call pattern
    match = re.match(r"^(\w+)\((.*)\)$", command)
    if not match:
        raise ValueError("Invalid command format")
    
    func_name, args_str = match.groups()
    
    # Validate function exists
    if func_name not in FUNCTIONS:
        raise ValueError(f"Function '{func_name}' not found")
    
    func = FUNCTIONS[func_name]
    sig = inspect.signature(func)
    parameters = sig.parameters
    param_names = list(parameters.keys())
    
    pos_args = []
    kwargs = {}
    
    if args_str:
        # Split arguments while handling nested parentheses
        split_args = re.split(r",\s*(?![^()]*\))", args_str)
        for arg in split_args:
            arg = arg.strip()
            if not arg:
                continue
            if '=' in arg:
                # Handle keyword arguments
                key_part, value_part = arg.split('=', 1)
                key = key_part.strip()
                value = literal_eval(value_part.strip())
                kwargs[key] = value
            else:
                # Handle positional arguments
                pos_args.append(literal_eval(arg.strip()))
    
    # Map positional arguments to parameters
    for i, pos_value in enumerate(pos_args):
        if i >= len(param_names):
            raise ValueError(f"Too many positional arguments for {func_name}")
        param_name = param_names[i]
        if param_name in kwargs:
            raise ValueError(f"Parameter '{param_name}' provided both positionally and as keyword")
        kwargs[param_name] = pos_value
    
    # Validate required parameters
    for param_name in param_names:
        param = parameters[param_name]
        if param.default is param.empty and param_name not in kwargs:
            raise ValueError(f"Missing required argument '{param_name}'")
    
    return func(**kwargs)

def handle_get_structured_command(user_input):
    return LLMModel.get_structured_command(user_input)

# Example usage
def process_request(user_input):
    try:        
        function_calls = None
        count = 0
        print("Running DeepSeek")
        while function_calls == None:
            if count > 0:
                print("Some error occured, trying again!")
            function_calls = handle_get_structured_command(user_input)
            count += 1
        # print("Filtered commands:")
        # print(function_calls, "\n")
        
        # Split multiple commands by newline
        commands = [cmd.strip() for cmd in function_calls.split('\n') if cmd.strip()]
        
        for cmd in commands:
            execute_user_command(cmd)
            # print(f"Result of '{cmd}': {result}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
