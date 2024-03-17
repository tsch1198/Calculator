
# Basic and Currancy Calculator - created by Tobias S. - 25.01.2024
# Last Update - 15.03.2024

import requests
import time

ERROR_COLOR = "\033[91;1m"
SUCCESS_COLOR = "\033[94m"
ANIMATION_COLOR = '\033[95m'
QUESTION_COLOR = "\033[93m"
RESET_COLOR = "\033[0m"

def exit_animation(type):
    print(f"{ANIMATION_COLOR}Exiting {type}{RESET_COLOR}", end="", flush=True)
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.3)

def boot_animation():
    print(f"{ANIMATION_COLOR}    ____       _____ _                 __     ______      __     ____  __          {RESET_COLOR}")
    print(f"{ANIMATION_COLOR}   / __ \\__  _/ ___/(_____ ___  ____  / ___  / ________ _/ _____/ __ \\/ __  _______{RESET_COLOR}")
    print(f"{ANIMATION_COLOR}  / /_/ / / / \\__ \\/ / __ `__ \\/ __ \\/ / _ \\/ /   / __ `/ / ___/ /_/ / / / / / ___/{RESET_COLOR}")
    print(f"{ANIMATION_COLOR} / ____/ /_/ ___/ / / / / / / / /_/ / /  __/ /___/ /_/ / / /__/ ____/ / /_/ (__  ) {RESET_COLOR}")
    print(f"{ANIMATION_COLOR}/_/    \\__, /____/_/_/ /_/ /_/ .___/_/\\___/\\____/\\__,_/_/\\___/_/   /_/\\__,_/____/  {RESET_COLOR}")
    print(f"{ANIMATION_COLOR}      /____/                /_/                                                    {RESET_COLOR}")

def number_input(prompt):
    #Checks if input is a Number
    while True:
        try:
            number = float(input(f"{QUESTION_COLOR}{prompt}{RESET_COLOR}"))
            return number
        except ValueError:
            print(f"{ERROR_COLOR}\nError: Please enter a valid number.{RESET_COLOR}")

def text_input(prompt, length):
    # Checks if input is the Proper length
    while True:
        text = input(f"{QUESTION_COLOR}{prompt}{RESET_COLOR}").upper()
        if len(text) != length:
            print(f"{ERROR_COLOR}\nError: Input must be exactly {length} characters long.{RESET_COLOR}")
        elif any(char.isdigit() for char in text):
            print(f"{ERROR_COLOR}\nError: Input cannot contain numbers.{RESET_COLOR}")
        else:
            return text

def get_operator():
    # Asks for Operator and checks if it is a valid one
    while True:
        operator = input(f"{QUESTION_COLOR}\nEnter your operator:  {RESET_COLOR}\n+ -> Plus \n- -> Minus \n* -> Multiply \n/ -> Divide \n \nc -> last Result \nh -> complete history \nq -> Quit \n")
        if operator.lower() in ['q', 'c', 'h', '+', '-', '*', '/']:
            return operator
        else:
            print(f"{ERROR_COLOR}\nError: Invalid operator.{RESET_COLOR}")

def round_result(result, precision):
    # Rounds the result to given Decimals
    try:
        if precision < 0:
            print(f"{ERROR_COLOR}\nError: Precision must be a non-negative integer.{RESET_COLOR}")
            return None
        rounded_result = round(result, precision)
        return rounded_result
    except Exception as e:
        print(f"{ERROR_COLOR}\nAn error occurred: {e}{RESET_COLOR}")

def main_calculator():
    # Does the main Calculation
    calc_main_result_array = []
    calc_main_history = []
    while True:

        operator = get_operator()
        
        # Check if user wants to quit
        if operator.lower() == 'q':
            exit_animation("Calculator")
            break

        # Check if user wants to see his last result
        elif operator.lower() == 'c':
            if not calc_main_history:
                print(f"{ERROR_COLOR}\nThere are no Results yet{RESET_COLOR}")
                continue
            print(f"{SUCCESS_COLOR}\nYour last Result = {calc_main_history[0]}{RESET_COLOR}")
            calc_main_history.clear()
            continue

        # Check if user wants to see the history    
        elif operator.lower() == 'h':
            if not calc_main_result_array:
                print(f"{ERROR_COLOR}\nHistory is empty{RESET_COLOR}")
                continue
            for index, item in enumerate(calc_main_result_array):
                print(f"{SUCCESS_COLOR}\n{index+1}. Entry {item}{RESET_COLOR}")
            continue

        # Get numbers from user
        num1 = number_input("Enter your first number: ")
        num2 = number_input("Enter your second number: ")

        # Perform calculation based on operator
        match operator:
            case "+":
                result = (num1 + num2)
            case "-":
                result = (num1 - num2)
            case "*":
                result = (num1 * num2)
            case "/":
                if num2 == 0:
                    print(f"{ERROR_COLOR}\nError: Division by zero!{RESET_COLOR}")
                    continue
                else:
                    result = (num1 / num2)
            case _:
                print(f"{ERROR_COLOR}\nError: Invalid Operator!{RESET_COLOR}")
                continue

        want_to_round = input(f"{QUESTION_COLOR}Do you want to round off your result? (y/n): {RESET_COLOR}")
        if want_to_round.lower() == "y":
            precision = number_input("How many digits after the decimal point do you want? ")
            rounded_result = round_result(result, int(precision))
            if rounded_result is None:
                continue
            else:
                result = rounded_result
        
        # Prints Result
        print(f"{SUCCESS_COLOR}\nResult: {result}{RESET_COLOR}")

        # Saves Result
        calc_normal_calc = f"{num1} {operator} {num2} = {result}"
        calc_main_result_array.append(result)
        calc_main_history.append(calc_normal_calc)

def currency_calculator():
    try:
        # Gets Imput from User
        base_currency = text_input("What's the base currency? (Short Term): ", 3)
        amount = number_input(f"How much {base_currency} do you want to exchange? ")
        wanted_currency = text_input("What's the wanted currency? (Short Term): ", 3)

        # Get the JSON object from the API
        api_link = f"https://v6.exchangerate-api.com/v6/<APITOKEN>/pair/{base_currency}/{wanted_currency}/{amount}"
        response = requests.get(api_link)
        data = response.json()

        # Collects HTTP errors
        response.raise_for_status()
        
        # Print only the conversion result
        if 'conversion_result' in data:
            conversion_result = round(data['conversion_result'], 2)
            print(f"{SUCCESS_COLOR}\n{amount}{base_currency} in {wanted_currency} = {conversion_result}{wanted_currency}{RESET_COLOR}")
        else:
            print(f"{ERROR_COLOR}\nError: Could not retrieve conversion result.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}\nAn unexpected error occurred: {e}{RESET_COLOR}")

def choose_calculator_type():
    # Main Calculator choosing
    while True:
        calc_type = input(f"{QUESTION_COLOR}\nWhich calculator do you want to use?{RESET_COLOR}\n1 -> Basic\n2 -> Currency\n3 -> Quit\n")
        if calc_type in ['1', '2', '3']:
            return int(calc_type)
        else:
            print(f"{ERROR_COLOR}\nError: Please enter 1, 2, or 3.{RESET_COLOR}")

def main():
    boot_animation()
    while True:
        calc_type = choose_calculator_type()
        if calc_type == 1:
            main_calculator()
        elif calc_type == 2:
            currency_calculator()
        elif calc_type == 3:
            exit_animation("Main Programm")
            break

main()
