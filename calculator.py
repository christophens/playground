import math
import ast
import re
import random
import string

#improved version with better operation switching. Work in progress.

def get_user_input() -> str:
    print('Input: ')
    return input()

def get_innermost_parantheses(text: str) -> (tuple, str):
    # Define regex to extract all parts inside a paranthesis
    paranthesis_regex = r'\([^\(\)]+\)'
    result = re.search(paranthesis_regex, text)
    if result == None:
        indices = [0, 0]
        string = text        
    else:
        indices = [result.start(), result.end()]
        string = result.group(0)[1:-1]
    return indices, string

def get_operations(text: str) -> (list, list):
    # Define regex to extract all numbers in a string and extract these numbers
    number_regex =  r'(?<=[\+\-\*\/\(\^])\s*[\+\-]?\s*\d+\.?\d*|_[a-z]{2}_|^\s*[\+\-]?\s*\d+\.?\d*|^_[a-z]{2}'
    number_list = re.findall(number_regex, text)

    # Strip all remaining whitespaces
    number_list = [number.replace(' ','') for number in number_list]

    operator_regex = r'(?<=[\d\)])\s*[\+\-\/\*\^]'
    operator_list = re.findall(operator_regex, text)
    operator_list = [operator.replace(' ','') for operator in operator_list]

    return number_list, operator_list

def evaluate_expression(number_list: list, operator_list: list, intermediate_results: dict) -> dict:
    # Evaluate all operations based on the established order of operations
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
        '/' : a / b,
        '*' : a * b,
        '+' : a + b,
        '-' : a - b,
        '^' : pow(a, b)
    }
    new_key = create_new_key(intermediate_results)
    intermediate_results[new_key] = switcher.get(operand)
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
