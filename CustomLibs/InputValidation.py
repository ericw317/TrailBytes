import os

# input validation for an integer between two numbers
def int_between_numbers(prompt, lower_num, upper_num):
    while True:
        try:
            number = int(input(prompt))  # prompt the user

            # run input validation
            if lower_num <= number <= upper_num:
                return number  # return number once it passes input validation
            else:
                print(f"Error: Input must be an integer between {lower_num} and {upper_num}")
        except ValueError:
            print("Error: Input must be an integer.")

