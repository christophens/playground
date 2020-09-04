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
    func_set = {'sin', 'cos', 'exp'}
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

def get_operations(text: str) -> (list, list):
    """
    Returns a list with numbers and operators in order of their appearance in a given expression.
    """
    # Define regex to extract all numbers in a string, as well as placeholders for intermediate results.
    # These placeholders are of the form '_xx_', with x being a lowercase letter.
    # Use re.findall method to get a list of all numbers from the string.
    number_regex =  r'(?<=[\+\-\*\/\(\^])\s*[\+\-]?\s*\d+\.?\d*|_[a-z]{2}_|^\s*[\+\-]?\s*\d+\.?\d*|^_[a-z]{2}'
    number_list = re.findall(number_regex, text)

    # Strip all remaining whitespaces.
    number_list = [number.replace(' ','') for number in number_list]

    # Define regex to extract mathematical operators +, -, *, /, ^.
    operator_regex = r'(?<=[\d\)])\s*[\+\-\/\*\^]'
    operator_list = re.findall(operator_regex, text)

    # Strip all remaining whitespaces.
    operator_list = [operator.replace(' ','') for operator in operator_list]

    # Return both lists.
    return number_list, operator_list

def evaluate_expression(number_list: list, operator_list: list, intermediate_results: dict, func: str) -> dict:
    """
    Evaluate all operations based on the established order of operations.
    """
    
    if not operator_list:
        new_key = create_new_key(intermediate_results)
        intermediate_results[new_key] = float(number_list[0])       
    
    atomic_operations = ['^', '*', '/']
    for operation in atomic_operations:
        while operation in operator_list:
            operator_index = operator_list.index(operation)
            a = number_list[operator_index]
            b = number_list.pop(operator_index + 1)
            (number_list[operator_index], intermediate_results) =  evaluate_operations(a, b, operation, intermediate_results)
            operator_list.remove(operation)
    
    while operator_list:
        a = number_list[0]
        b = number_list.pop(1)
        (number_list[0], intermediate_results) =  evaluate_operations(a, b, operator_list.pop(0), intermediate_results)

    
    
    if func:
        intermediate_results = evaluate_func(intermediate_results, func)


    
    return intermediate_results

def evaluate_operations(a: str, b:str, operand:str, intermediate_results: dict) -> (str, dict):
    try:
        a = float(a)
    except ValueError:
        a = intermediate_results.pop(a)
    try:
        b = float(b)
    except ValueError:
        b = intermediate_results.pop(b)
    significant_digits = get_significant_digits(a, b, operand)
    switcher = {
        '/' : lambda a, b : a / b,
        '*' : lambda a, b : a * b,
        '+' : lambda a, b : a + b,
        '-' : lambda a, b : a - b,
        '^' : lambda a, b : pow(a, b)
    }

    new_key = create_new_key(intermediate_results)
    result = switcher.get(operand)(a, b)
    result = round(result, significant_digits)

    intermediate_results[new_key] = result
    
    return new_key, intermediate_results

def get_significant_digits(a: float, b: float, operator: str) -> int:
    a = str(a)
    b = str(b)    
    decimal_regex = r'(?<=.)[0]*[1-9]+'
    a_dec = re.search(decimal_regex, a)
    b_dec = re.search(decimal_regex, b)

    a_dec = a_dec.end()- a_dec.start() if a_dec else 0
    b_dec = b_dec.end()- b_dec.start() if b_dec else 0


    
    if operator in ['+', '-']:
        return max(a_dec, b_dec)
    elif operator == '*':
        return a_dec + b_dec
    elif operator == '/':
        return 


def evaluate_func(intermediate_results: dict, func: str) -> dict:
    
    switcher = {
        'sin' : lambda a: math.sin(a),
        'cos' : lambda a: math.cos(a),
        'exp' : lambda a: math.exp(a)
    }
    key = list(intermediate_results.keys())[0]
    intermediate_results[key] = switcher.get(func)(intermediate_results[key])

    return intermediate_results


def create_new_key(intermediate_results: dict) -> str:
    if not intermediate_results:
        key = ''.join(random.choices(string.ascii_lowercase, k=2))
        key = '_' + key + '_'
    else:
        key = list(intermediate_results.keys())
        key = key[0] 
        while key in intermediate_results:
            key = ''.join(random.choices(string.ascii_lowercase, k=2))
            key = '_' + key + '_'
    return key

def main_c(*args):
    if __name__ == '__main':
        text = get_user_input()
    else:
        text = args[0]
    intermediate_results = {}
    repeat = True
    while repeat:
        indices, string, func = get_next_operation(text)
        numbers, operators = get_operations(string)
        intermediate_results = evaluate_expression(numbers, operators, intermediate_results, func) 
        text = text.replace(text[indices[0] : indices[1]], list(intermediate_results.keys())[0])
        if indices[0] == 0:
            repeat = False
        
    return (list(intermediate_results.values())[0])
    print(str(list(intermediate_results.values())[0]))

