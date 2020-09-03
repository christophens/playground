import math
import ast
import re
import random
import string

# Improving annotations.


def get_user_input() -> str:
    """
    Get user input from terminal.
    """
    print('Input: ')
    return input()

def get_innermost_parantheses(text: str) -> (list, str):
    """
    Find the next expression to evaluate. Returns two objects:
    - A list with two integers that indicate the position of the next expression.
    - A string with the expression.
    Example: 4 * 3 * (3 + 4 * (5 / 7)) -> 5 / 7
    """
    # Define regex to extract the innermost complete pair of parantheses. 
    # Use re.search method to obtain the first complete set of parantheses.
    # If at least one set of parantheses exist it returns a re.match object.
    # The match includes the paranthesis, i.e. '(5 / 7)
    paranthesis_regex = r'\([^\(\)]+\)'
    result = re.search(paranthesis_regex, text)

    # If no parantheses are found, return the entire string and set the list with the position of the 
    # index to [0, 0]. 
    if result == None:
        indices = [0, 0]
        string = text
    # If a match object is found, slice and return the resulting string without the parantheses.      
    else:
        indices = [result.start(), result.end()]
        string = result.group(0)[1:-1]
    return indices, string

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

def evaluate_expression(number_list: list, operator_list: list, intermediate_results: dict) -> dict:
    """
    Evaluate all operations based on the established order of operations.
    """
    # Define operations list
    operations_list = ['^', '*', '/', '+', '-']

    for operation in operations_list:
        while operation in operator_list:
            operator_index = operator_list.index(operation)
            a = number_list[operator_index]
            b = number_list.pop(operator_index + 1)
            (number_list[operator_index], intermediate_results) =  evaluate_operations(a, b, operation, intermediate_results)
            operator_list.remove(operation)
    
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
    
    switcher = {
        '/' : lambda a, b : a / b,
        '*' : lambda a, b : a * b,
        '+' : lambda a, b : a + b,
        '-' : lambda a, b : a - b,
        '^' : lambda a, b : pow(a, b)
    }

    new_key = create_new_key(intermediate_results)
    intermediate_results[new_key] = switcher.get(operand)(a, b)
    
    return new_key, intermediate_results

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

def main_c():
    text = get_user_input()
    repeat = True
    intermediate_results = {}
    while repeat:
        indices, string = get_innermost_parantheses(text)
        numbers, operators = get_operations(string)
        intermediate_results = evaluate_expression(numbers, operators, intermediate_results)
        if indices != [0, 0]:
            text = text.replace(text[indices[0] : indices[1]], list(intermediate_results.keys())[0])
        else:
            repeat = False
    
    print(str(list(intermediate_results.values())[0]))


main_c()
