import math
import ast
import re
import random
import string

# Constant improvement.

def get_user_input() -> str:
    """
    Get user input from terminal.
    """
    print('Input: ')
    return input()

def get_next_operation(text: str) -> (list, str, str):
    """
    Find the next expression to evaluate. Returns two objects:
    - A list with two integers that indicate the position of the next expression.
    - A string with the expression.
    - A string that contains special mathematical functions.
    Example: 4 * 3 * (3 + 4 * (5 / 7)) -> 5 / 7
    """
    # Define regex to extract the innermost complete pair of parantheses. 
    # Use re.search method to obtain the first complete set of parantheses.
    # If at least one set of parantheses exist it returns a re.match object.
    # The match includes the paranthesis, i.e. '(5 / 7)'
    paranthesis_regex = r'\([^\(\)]+\)'
    result = re.search(paranthesis_regex, text)

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
        if text[result.start() - 3: result.start()] in func_set:
            indices = [result.start() - 3, result.end()]
            func = text[result.start() - 3: result.start()]


    
    return indices, string, func

def get_numbers_operators(text: str, variables_dict: list) -> (list, list, dict, int):
    """
    Returns a list with numbers and operators in order of their appearance in a given expression.
    """
    # Define regex to extract all numbers in a string, as well as placeholders for intermediate results.
    # These placeholders are of the form '_xx_', with x being a lowercase letter.
    # Use re.findall method to get a list of all numbers from the string.
    variables_regex =  r'(?<=[\+\-\*\/\^\,])\s*[\+\-]?\s*\d+\.?\d*|[A-Za-z_]+[A-Za-z0-9_]*|^\s*[\+\-]?\s*\d+\.?\d*|[A-Za-z_]+[A-Za-z0-9_]*'
    variables_list = re.findall(variables_regex, text)

    variables_index = len(variables_dict)
    variables_dict_var = variables_dict.keys() # returns DYNAMIC view object
    for idx, entry in enumerate(variables_list):
        if not entry in variables_dict_var:
            new_var = create_new_var(list(variables_dict_var))
            variables_dict[new_var] = float(entry.replace(' ',''))
            variables_list[idx] = new_var
    
    # Define regex to extract mathematical operators +, -, *, /, ^.
    operator_regex = r'(?<=[\d\)A-z])\s*[\+\-\/\*\^,]'
    operator_list = re.findall(operator_regex, text)

    # Strip all remaining whitespaces.
    operator_list = [operator.replace(' ','') for operator in operator_list]

    # Return both lists.
    return variables_list, operator_list, variables_dict, variables_index

def evaluate_expression(variables_list: list, operator_list: list, variables_dict: list, variables_index: int,func: str) -> dict:
    """
    Evaluate all operations based on the established order of operations.
    """
    
    if not operator_list:
        if func: 
            variables_dict[variables_list[variables_index]] = evaluate_func(func, variables_dict[variables_list[variables_index]])
        return variables_dict   
    
    mul_diff_exp_list = ['^', '*', '/']
    for operation in mul_diff_exp_list:
        while operation in operator_list:
            operator_index = operator_list.index(operation)
            a = variables_dict[variables_list[operator_index]]
            b = variables_dict.pop(variables_list.pop(operator_index + 1))
            variables_dict[variables_list[operator_index]] =  arithmetic_operations(a, b, operator_list.pop(operator_index))
    
    if ',' not in operator_list:
        while operator_list:
            a = variables_dict[variables_list[variables_index]]
            b = variables_dict.pop(variables_list.pop(variables_index + 1))
            variables_dict[variables_list[variables_index]] =  arithmetic_operations(a, b, operator_list.pop(0))
    
        if func:
            variables_dict[variables_list[variables_index]] = evaluate_func(func, variables_dict[variables_list[variables_index]])
    else:
        idx = 0
        while operator_list[idx] != ',':
            a = variables_dict[variables_list[variables_index]]
            b = variables_dict.pop(variables_list.pop(variables_index + 1))
            variables_dict[variables_list[variables_index]] =  arithmetic_operations(a, b, operator_list[idx])
            idx = idx + 1
        
        operator_list = operator_list[idx + 1:]
        while operator_list:
            a = variables_dict[variables_list[variables_index + 1]]
            b = variables_dict.pop(variables_list.pop(variables_index + 2))
            variables_dict[variables_list[variables_index + 1]] =  arithmetic_operations(a, b, operator_list.pop(0))

        variables_dict[variables_list[variables_index]] = evaluate_func(func, variables_dict[variables_list[variables_index]], variables_dict.pop(variables_list.pop(variables_index + 1)))




    
    return variables_dict

def arithmetic_operations(a: str, b:str, operand:str) -> (float):

    significant_digits = get_significant_digits(a, b, operand)
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


def get_significant_digits(a: float, b: float, operator: str) -> int:
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
    
    switcher = {
        'sin' : lambda a: math.sin(a[0]),
        'cos' : lambda a: math.cos(a[0]),
        'exp' : lambda a: math.exp(a[0]),
        'abs' : lambda a: abs(a[0]),
        'log' : lambda a: math.log(a[0], a[1])
    }
    

    return switcher.get(func)(args)

def create_new_var(key_list: list) -> str:
    if not key_list:
        key = ''.join(random.choices(string.ascii_letters, k=2))
    else:
        key = key_list[0] 
        while key in key_list:
            key = ''.join(random.choices(string.ascii_letters, k=2))
    return key

def main_c(*args):
    if not args:
        text = get_user_input()
    else:
        text = args[0]
    variables_dict = {}
    repeat = True
    while repeat:
        indices, string, func = get_next_operation(text)
        variables_list, operators, variables_dict, index = get_numbers_operators(string, variables_dict)
        variables_dict = evaluate_expression(variables_list, operators, variables_dict, index, func) 
        text = text.replace(text[indices[0] : indices[1]], list(variables_dict.keys())[-1])
        if indices[0] == 0:
            repeat = False

    if not args: 
        print(str(variables_dict[variables_list[index]]))    
    return (variables_dict[variables_list[index]])


