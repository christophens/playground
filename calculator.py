import math
import ast
import re
import random
import string

# Revert to original.

def get_user_input() -> (str, str):
    """
    Get user input from terminal.
    """
    print('Input: ')
    user_input = input()

    a = user_input.find('=')
    var = None
    if a != -1:
        var = user_input[0:a]
        var = var.replace(' ','')
        text = user_input[a + 1:]

    else:
        text = user_input
    return var, text



def get_next_operation(text: str) -> (list, str, str):
    """
    Find the next expression to evaluate. 
    Input:
    
    
    Return objects:
    - A list with two integers that indicate the position of the next expression within the innput string.
    - A string with the expression.
    - A string that contains a mathematical function keyword such as sin, cos, ...
    Example: 4 * 3 * (3 + 4 * (5 / 7)) -> 5 / 7
    """
    # Define regex to extract the innermost complete pair of parantheses. 
    # Use re.search method to obtain the first complete set of parantheses.
    # If at least one set of parantheses exist it returns a re.match object.
    # The match includes the paranthesis, i.e. '(5 / 7)'
    paranthesis_regex = r'\([^\(\)]+\)'
    result = re.search(paranthesis_regex, text)

    # Define a set of accepted function keywords that preceed the parantheses.
    # Set the default return value that contains the function keyword to None
    func_set = {'sin', 'cos', 'exp', 'abs', 'log'}
    func = None
    # If no parantheses are found, return the entire string and set the list with the position of the
    # extracted string to [0, length of the the string - 1]. 
    if result == None:
        string = text
        indices = [0, len(text) - 1]
    # If a match object is found, slice and return the resulting string without the parantheses.      
    else:
        indices = [result.start(), result.end()]
        string = result.group(0)[1:-1]
        # If a valid function keyword preceeds the parantheses, change the position of the extracted string to
        # include the function keyword and return the keyword.
        if text[result.start() - 3: result.start()] in func_set:
            indices = [result.start() - 3, result.end()]
            func = text[result.start() - 3: result.start()]


    
    return indices, string, func

def get_numbers_operators(text: str, var_dict: dict, svar_dict:dict) -> (list, list, dict):
    """
    Returns a list with variables and operators in order of their appearance in a given expression.
    A dict maps values to each variable.

    Input:
    - text: string with an operation to evaluate. Must not contain parantheses. \n \
    Example: '5 - ans * az'
    - var_dict: Dict that keeps intermediate results. \n \
    Example: {'az': -4.36}
    - svar_dict: Dict that keeps stored variables from previous evaluations. \n \
    Example: {'ans': 3.0}
    
    Output objects:
    - var_list: list with variables in the order of their apperance. \n \
    Example: 5 - ans * az returns ['fT', 'ans, 'az'] \n

    - var_operators: list with arithmetic operators in order of their appearance. \n \
    Example: 5 - ans * az returns ['-', '*'] \n

    - var_dict: Dictionary that maps float values to all elements in var_list. \n \
    Example: 5 - ans * az returns {'ft': 5.0, 'ans': 3.0, 'az': -4.36}
    """


    # Define regex to extract all numbers in a string, as well as placeholders for intermediate results.
    # These placeholders start with a character, followed by a sequence of characters and numbers.
    # Use re.findall method to get a list of all numbers from the string.
    variables_regex =  r"((?<=[\+\-\*\/\^\,])|^)\s*[\+\-]?\s*(\d+\.?\d*(e-?\d+)?|[A-Za-z]+[A-Za-z0-9]*)"
    var_list = re.findall(variables_regex, text)
    var_list = [i[1] for i in var_list]

    # Create dynamic view objects of the keys in var_dict and svar_dict.
    var_dict_keys = var_dict.keys() # returns DYNAMIC view object
    svar_dict_keys = svar_dict.keys()

    # Loop over var_list to assign variables to numbers and to copy saved variables from svar_dict to var_dict.
    for idx, entry in enumerate(var_list):
        # Do nothing if an entry in var_list is already stored as a variable in var_dict
        if not entry in var_dict_keys:
            # Check if entry is contained in svar_dict
            if not entry in svar_dict_keys:
                # Create a new variable that is different from all existing variable names
                new_var = create_new_var(list(var_dict_keys) + list(svar_dict_keys))

                # Add the new variable to var_dict, the variable name is the key, the value is a float of the number
                var_dict[new_var] = float(entry)
                # Change number to variable in var_list
                var_list[idx] = new_var
            # Copy from svar_dict to var_dict
            else:
                var_dict[entry] = svar_dict[entry]

    
    operator_string = re.sub(variables_regex, '', text)
    operator_list = [i for i in operator_string if i !=' ']

    # Return both lists and the dictionairy.
    return var_list, operator_list, var_dict

def evaluate_expression(var_list: list, operator_list: list, var_dict: list,func: str) -> dict:
    """
    Evaluate all operations based on the established order of operations.
    """
    # If no operator is supplied, return var_dict without after evaluation of function keywords.
    if not operator_list:
        if func: 
            var_dict[var_list[0]] = evaluate_func(func, var_dict[var_list[0]])
        return var_dict   
    
    mul_diff_exp_list = ['^', '*', '/']
    for operation in mul_diff_exp_list:
        while operation in operator_list:
            operator_index = operator_list.index(operation)
            a = var_dict[var_list[operator_index]]
            b = var_dict.pop(var_list.pop(operator_index + 1))
            var_dict[var_list[operator_index]] =  arithmetic_operations(a, b, operator_list.pop(operator_index))
    
    if ',' not in operator_list:
        while operator_list:
            a = var_dict[var_list[0]]
            b = var_dict.pop(var_list.pop(0 + 1))
            var_dict[var_list[0]] =  arithmetic_operations(a, b, operator_list.pop(0))
    
        if func:
            var_dict[var_list[0]] = evaluate_func(func, var_dict[var_list[0]])
    else:
        idx = 0
        while operator_list[idx] != ',':
            a = var_dict[var_list[0]]
            b = var_dict.pop(var_list.pop(1))
            var_dict[var_list[0]] =  arithmetic_operations(a, b, operator_list[idx])
            idx = idx + 1
        
        operator_list = operator_list[idx + 1:]
        while operator_list:
            a = var_dict[var_list[1]]
            b = var_dict.pop(var_list.pop(2))
            var_dict[var_list[1]] =  arithmetic_operations(a, b, operator_list.pop(0))

        var_dict[var_list[0]] = evaluate_func(func, var_dict[var_list[0]], var_dict.pop(var_list.pop(1)))

    
    return var_dict

def arithmetic_operations(a: float, b:float, operand:str) -> (float):
    """
    Evaluate arithmetic operations.
    """

    significant_digits = get_significant_decimals(a, b, operand)
    switcher = {
        '/' : lambda a, b : a / b,
        '*' : lambda a, b : a * b,
        '+' : lambda a, b : a + b,
        '-' : lambda a, b : a - b,
        '^' : lambda a, b : pow(a, b)
    }

    result = switcher.get(operand)(a, b)
    result = round(result, significant_digits)
    
    return result


def get_significant_decimals(a: float, b: float, operator: str) -> int:
    """
    Get the number of significant decimals
    """
    a = str(a)
    b = str(b)    
    decimal_regex = r'(?<=\.)[0]*[1-9]+'
    a_dec = re.search(decimal_regex, a)
    b_dec = re.search(decimal_regex, b)

    a_dec = a_dec.end()- a_dec.start() if a_dec else 0
    b_dec = b_dec.end()- b_dec.start() if b_dec else 0

    
    if operator in ['+', '-']:
        return max(a_dec, b_dec)
    elif operator == '*':
        return a_dec + b_dec
    else:
        return 20

def evaluate_func(func: str, *args: float) -> dict:
    """
    Evaluate mathematical functions.
    """
    switcher = {
        'sin' : lambda a: math.sin(a[0]),
        'cos' : lambda a: math.cos(a[0]),
        'exp' : lambda a: math.exp(a[0]),
        'abs' : lambda a: abs(a[0]),
        'log' : lambda a: math.log(a[0], a[1])
    }
    

    return switcher.get(func)(args)

def create_new_var(var_list: list) -> str:
    """
    Create new variable.
    """
    if not var_list:
        key = ''.join(random.choices(string.ascii_letters, k=2))
    else:
        key = var_list[0] 
        while key in var_list:
            key = ''.join(random.choices(string.ascii_letters, k=2))
    return key

def main_c(*args):
    svar_dict ={}
    if args:
        text = args[0]
    else:
        var, text = get_user_input()
        while text !='quit':
            var_dict = {}
            repeat = True
            while repeat:
                indices, string, func = get_next_operation(text)
                var_list, operators, var_dict = get_numbers_operators(string, var_dict, svar_dict)
                var_dict = evaluate_expression(var_list, operators, var_dict, func) 
                text = text.replace(text[indices[0] : indices[1]], list(var_dict.keys())[0])
                if indices[0] == 0:
                    repeat = False
            svar_dict['ans'] = var_dict[var_list[0]]
            print(str(var_dict[var_list[0]]) + '\n')
            if var:
                svar_dict[var] = var_dict[var_list[0]]
                var = None
            var, text = get_user_input()
            
    return (var_dict[var_list[0]])

main_c()


