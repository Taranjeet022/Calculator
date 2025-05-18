from tkinter import *
from statistics import mean, median, mode, StatisticsError
import math

def buttonClick(number):
    global operator
    operator += str(number)
    input_value.set(operator)

def buttonClear():
    global operator
    operator = ""
    input_value.set("")

def buttonBackspace():
    global operator
    operator = operator[:-1]
    input_value.set(operator)

def buttonToggleSign():
    global operator
    try:
        if operator.startswith('-'):
            operator = operator[1:]
        else:
            operator = '-' + operator
        input_value.set(operator)
    except:
        input_value.set("Error")

def buttonEqual():
    global operator
    try:
        expression = operator.replace('^', '**')
        result = str(eval(expression))
        input_value.set(result)
        update_history(operator + " = " + result)
        operator = ""
    except:
        input_value.set("Error")
        operator = ""

def calculate_stat(stat_type):
    global operator
    try:
        numbers = list(map(float, operator.split(',')))
        if stat_type == 'mean':
            result = mean(numbers)
        elif stat_type == 'median':
            result = median(numbers)
        elif stat_type == 'mode':
            result = mode(numbers)
        input_value.set(str(result))
        update_history(f"{stat_type.title()}({numbers}) = {result}")
        operator = ""
    except ValueError:
        input_value.set("Error: Use commas")
    except StatisticsError:
        input_value.set("No unique mode")
        update_history(f"Mode({numbers}) = No unique mode")
    except:
        input_value.set("Error")

def calculate_sqrt():
    global operator
    try:
        result = math.sqrt(float(operator))
        input_value.set(str(result))
        update_history(f"√({operator}) = {result}")
        operator = ""
    except:
        input_value.set("Error")

def update_history(entry):
    history_list.insert(END, entry)

def clear_history():
    history_list.delete(0, END)

# GUI Setup
main = Tk()
main.title("CALCULATOR WITH STATS")
main.geometry("750x520")
main.config(bg="#e6f0f8") # Light background

operator = ""
input_value = StringVar()

# Create main frames
main_frame = Frame(main, bg="pink")
main_frame.pack(fill=BOTH, expand=True)

left_frame = Frame(main_frame, bg="pink")
left_frame.pack(side=LEFT, padx=10, pady=10)

right_frame = Frame(main_frame, bg="pink")
right_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)

# Display Entry
display_text = Entry(left_frame, font=("arial", 22), textvariable=input_value, bd=10, insertwidth=2,
                     bg="white", justify=RIGHT, relief=FLAT)
display_text.grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky="we")

# Buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3), ('Mean', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3), ('Median', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3), ('Mode', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('/', 4, 3), ('√', 4, 4),
    (',', 5, 0), ('C', 5, 1), ('←', 5, 2), ('^', 5, 3), ('+/-', 5, 4)
]

for (text, row, col) in buttons:
    if text == 'C':
        action = buttonClear
    elif text == '=':
        action = buttonEqual
    elif text == '←':
        action = buttonBackspace
    elif text == '+/-':
        action = buttonToggleSign
    elif text == '√':
        action = calculate_sqrt
    elif text == 'Mean':
        action = lambda: calculate_stat("mean")
    elif text == 'Median':
        action = lambda: calculate_stat("median")
    elif text == 'Mode':
        action = lambda: calculate_stat("mode")
    else:
        action = lambda x=text: buttonClick(x)

    Button(left_frame, text=text, padx=20, pady=15, bd=0, fg="white", bg="purple",
           font=("arial", 14, "bold"), command=action).grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

# Make buttons stretch
for i in range(5):
    left_frame.columnconfigure(i, weight=1)
for i in range(6):
    left_frame.rowconfigure(i, weight=1)

# History Section
Label(right_frame, text="History", font=("arial", 15,"bold"),fg="black", bg="white").pack(pady=(10, 5))

history_list = Listbox(right_frame, width=30, height=20, font=("arial", 12), bd=2, bg="white")
history_list.pack(padx=5, pady=5)

Button(right_frame, text="Clear History", font=("arial", 12, "bold"), fg="white", bg="purple", command=clear_history).pack(pady=10)

main.mainloop()
