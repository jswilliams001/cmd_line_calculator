import operator
import re

debug = False


def shunting_yard(infix_expression: str) -> tuple[list[str], str]:
    """
    This is pretty much by-the-book Dijkstra's Shunting Yard algorithm:
    https://www.cs.utexas.edu/~EWD/MCReps/MR35.PDF and https://math.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/

    :param infix_expression: String input of mathematical expression.
    :return: list of tokens in Postfix Notation AKA Reverse Polish Notation (RPN)
             and a sanitized string of the user's input expression.
    """
    return_val = [], ''
    operator_precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
    left_associative = {'+', '-', '*', '/', '%'}
    right_associative = {'^'}  # Here for reference; ^ having the highest precedence, will always be popped from the
                               # infix_expression and appended to the op_stack.

    # Initialize the stack for operators and the output queue
    op_stack = []
    post_fix_expression = []

    # Tokenize the expression
    # Assume that the user is sloppy with whitespace by ignoring whitespace and delimiting numbers with any non-number
    tokens = []  # expression.split()
    temp_token = []
    parenthesis_count = 0
    # match_string = '[-+*/^()0-9.\s]+'
    for char_ in infix_expression:
        if not bool(re.match(r'[-+*/%^()0-9.\s]+', char_)):  # r'...' raw string to supress escape sequence warning
            print(f"Invalid character: {char_}")
            return return_val
        if char_ in '()':
            parenthesis_count += 1
        if char_.isspace():
            continue
        if char_.isnumeric() or char_ == '.':
            temp_token.append(char_)
            if temp_token.count('.') > 1:
                print(f"Invalid use of '.' in token {''.join(temp_token)}")
                return return_val
        else:
            if temp_token:
                tokens.append(''.join(temp_token))
                temp_token = []
            tokens.append(char_)
    if temp_token:  # if last char_ was a number it still needs to be appended to tokens
        tokens.append(''.join(temp_token))
    if parenthesis_count % 2 != 0:
        print(f"Invalid use of parenthesis in input {' '.join(tokens)}")
        return return_val
    if debug:
        print(f"Tokenized String = {tokens}")

    # Find negatives. This could be combined above, but this is far more readable.
    previous_token = ''
    negative = False
    tokens_ = []
    for token in tokens:
        if negative:
            negative = False
            previous_token = token
            tokens_.append(f'-{token}')
            continue
        if token == '-' and (not previous_token or previous_token in '+-*/(^'):
            negative = True
            continue
        else:
            previous_token = token
            tokens_.append(token)
    if debug:
        print(f"Tokenized String with negatives = {tokens_}")
    # Clean up input string for output
    clean_user_input = ' '.join(tokens_).replace(' ^ ', '^')

    # Shunting Yard algorithm
    for token in tokens_:
        if token.replace(".", "").replace("-", "").isnumeric():  # If the token is a number, add it to the output queue
            post_fix_expression.append(token)
            if debug:
                print(f"Numeric token: {token}")
        elif token in operator_precedence:  # If the token is an operator
            # While there is an operator at the top of the op_stack with greater operator_precedence
            # Or the operator at the top of the op_stack has equal operator_precedence and is left associative
            # And the operator at the top of the op_stack is not a left parenthesis
            while (op_stack and op_stack[-1] in operator_precedence and
                   ((operator_precedence[op_stack[-1]] > operator_precedence[token]) or
                    (operator_precedence[op_stack[-1]] == operator_precedence[token] and token in left_associative)) and
                   (op_stack[-1] != '(')):
                post_fix_expression.append(op_stack.pop())  # Pop operators from the op_stack to the output queue
            op_stack.append(token)  # Push the current operator on the op_stack
        elif token == '(':  # If the token is a left parenthesis
            op_stack.append(token)
        elif token == ')':  # If the token is a right parenthesis
            # Pop operators from the op_stack to the output queue until we find a left parenthesis
            while op_stack and op_stack[-1] != '(':
                post_fix_expression.append(op_stack.pop())
            op_stack.pop()  # Pop the left parenthesis from the op_stack and discard it

    # Pop any remaining operators from the op_stack to the output queue
    while op_stack:
        post_fix_expression.append(op_stack.pop())
    if debug:
        print(f"RPN also known as {post_fix_expression=}")
    return post_fix_expression, clean_user_input


def calculate(rpn: list[str]) -> float:
    """
    Calculate the result of evaluating an arithmetic expression in Reverse Polish Notation (RPN).

    :param rpn: A list of strings representing the arithmetic expression in RPN format.
    :return: The result of evaluating the arithmetic expression.
    Note:
        - The arithmetic expression should only contain numbers and the following operators: +, -, *, /, %, ^.
        - The numbers and operators should be provided in the correct order for RPN evaluation.
        - The RPN expression should not contain any parentheses or other grouping symbols.
        - Division (/) is performed as true division, returning a float result.
        - The exponentiation (^) operator is not supported in all Python versions prior to Python 3.9.
    """
    eval_stack = []
    operator_ = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
        '%': operator.mod
    }

    for token in rpn:
        if debug:
            print(f"{token=}")
        if token.replace(".", "").replace("-", "").isnumeric():
            eval_stack.append(float(token))
            if debug:
                print(f"token is number: {eval_stack=}")
        else:
            if len(eval_stack) >= 2:
                op2 = float(eval_stack.pop())
                op1 = float(eval_stack.pop())
                eval_stack.append(operator_[token](op1, op2))
            else:
                print(f"Invalid expression - cannot tokenize")
                return ''
            if debug:
                print(f" {op1} {token} {op2} = {(eval_stack[-1:][0])}")
                print(f"eval: {eval_stack=}")
    if debug:
        print(f"Calculated result {eval_stack=}")
    if len(eval_stack) > 1:
        print(f"Invalid expression - mismatch between operands and operators")
        return ''
    else:
        return eval_stack[0]


def print_instructions():
    print("This is a simple command line calculator.")
    print("Enter any arithmetic expression and the calculator will compute and output the result.")
    print("""Supported operations are:
      addition (+)
      subtraction (-)
      multiplication (*)
      division (/)
      exponentiation (^)
      modulus (%)""")
    print("You can use parentheses to change the order of operations, similar to normal mathematical notation.")
    print("Decimal values are supported.")
    print("Example:  ( 14^2 * (3/2) - 101 )^-2")
    print()
    print("  q: exit the application")
    print("  h: print this help message")
    print()


if __name__ == "__main__":
    print("Enter expression followed by 'return' (q to quit, h for help): ")
    while True:
        user_input = input()
        if not user_input:
            print("Please enter a valid expression, q to quit, h for help:")
            continue
        if user_input == 'q':
            print("Goodbye.")
            break
        elif user_input == 'h':
            print_instructions()
            continue
        else:
            rpn, cleaned_input = shunting_yard(user_input)

            if rpn:
                x = calculate(rpn)
                if x and (x.is_integer() or x == 0):
                    print(f"{cleaned_input} = {x:g}")  # no trailing '.0'
                else:
                    print(f"{cleaned_input} = {x}")
            else:
                continue
