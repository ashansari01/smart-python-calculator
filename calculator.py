import tkinter as tk
import ast
import operator


# ==============================
# SAFE CALCULATION
# ==============================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}


def safe_calculate(expression):
    try:
        tree = ast.parse(expression, mode="eval")

        def calculate(node):

            if isinstance(node, ast.Expression):
                return calculate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError

            if isinstance(node, ast.BinOp):
                left = calculate(node.left)
                right = calculate(node.right)

                operation = operators.get(type(node.op))

                if operation is None:
                    raise ValueError

                if isinstance(node.op, (ast.Div, ast.Mod)) and right == 0:
                    raise ZeroDivisionError

                return operation(left, right)

            raise ValueError

        return calculate(tree)

    except ZeroDivisionError:
        return "Cannot divide by zero"

    except (ValueError, SyntaxError):
        return "Invalid expression"


# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title("Smart Calculator")

# Initial size
root.geometry("420x700")

# Minimum size
root.minsize(350, 600)

# IMPORTANT:
# Allow window resizing
root.resizable(True, True)

root.configure(bg="#1e1e1e")


# ==============================
# GRID CONFIGURATION
# ==============================

# Make the main window expandable
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)


# ==============================
# TITLE
# ==============================

title = tk.Label(
    root,
    text="SMART CALCULATOR",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.grid(
    row=0,
    column=0,
    pady=(15, 5)
)


# ==============================
# DISPLAY
# ==============================

display = tk.Entry(
    root,
    font=("Arial", 30),
    justify="right",
    bg="#2d2d2d",
    fg="white",
    insertbackground="white",
    bd=0
)

display.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=20,
    pady=15,
    ipady=15
)


# ==============================
# MAIN CONTENT FRAME
# ==============================

main_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

main_frame.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=15
)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)


# ==============================
# HISTORY
# ==============================

history_frame = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

history_frame.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=5
)

history_frame.grid_columnconfigure(0, weight=1)


history_title = tk.Label(
    history_frame,
    text="HISTORY",
    font=("Arial", 11, "bold"),
    bg="#1e1e1e",
    fg="#aaaaaa"
)

history_title.grid(
    row=0,
    column=0,
    pady=5
)


history_box = tk.Listbox(
    history_frame,
    height=8,
    font=("Arial", 11),
    bg="#2d2d2d",
    fg="white",
    bd=0,
    highlightthickness=0
)

history_box.grid(
    row=1,
    column=0,
    sticky="nsew"
)

history_frame.grid_rowconfigure(1, weight=1)


history = []


# ==============================
# CALCULATOR FRAME
# ==============================

calculator_frame = tk.Frame(
    main_frame,
    bg="#1e1e1e"
)

calculator_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=5
)


# Make calculator columns expandable
for column in range(4):
    calculator_frame.grid_columnconfigure(
        column,
        weight=1
    )


# Make calculator rows expandable
for row in range(5):
    calculator_frame.grid_rowconfigure(
        row,
        weight=1
    )


# ==============================
# FUNCTIONS
# ==============================

def button_click(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)


def backspace():

    current = display.get()

    display.delete(0, tk.END)

    display.insert(0, current[:-1])


def percentage():

    try:

        value = float(display.get())

        result = value / 100

        display.delete(0, tk.END)

        display.insert(0, result)

    except ValueError:

        display.delete(0, tk.END)

        display.insert(0, "Error")


def calculate():

    expression = display.get()

    if not expression:
        return

    result = safe_calculate(expression)

    display.delete(0, tk.END)

    display.insert(0, result)

    if isinstance(result, (int, float)):

        history.append(
            f"{expression} = {result}"
        )

        history_box.insert(
            tk.END,
            f"{expression} = {result}"
        )


def clear_history():

    history.clear()

    history_box.delete(
        0,
        tk.END
    )


# ==============================
# KEYBOARD SUPPORT
# ==============================

def keyboard_input(event):

    key = event.char

    if key in "0123456789+-*/%.":
        button_click(key)

    elif event.keysym == "Return":
        calculate()

    elif event.keysym == "BackSpace":
        backspace()

    elif event.keysym == "Escape":
        clear()


root.bind("<Key>", keyboard_input)


# ==============================
# BUTTON CREATOR
# ==============================

def create_button(
    text,
    row,
    column,
    bg="#333333",
    command=None
):

    button = tk.Button(
        calculator_frame,
        text=text,
        font=("Arial", 17, "bold"),
        bg=bg,
        fg="white",
        activebackground="#666666",
        activeforeground="white",
        bd=0,
        command=command
    )

    button.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=5,
        pady=5
    )


# ==============================
# BUTTONS
# ==============================

create_button(
    "AC", 0, 0,
    bg="#ff5959",
    command=clear
)

create_button(
    "⌫", 0, 1,
    bg="#555555",
    command=backspace
)

create_button(
    "%", 0, 2,
    bg="#ff9800",
    command=percentage
)

create_button(
    "/", 0, 3,
    bg="#ff9800",
    command=lambda: button_click("/")
)


create_button(
    "7", 1, 0,
    command=lambda: button_click("7")
)

create_button(
    "8", 1, 1,
    command=lambda: button_click("8")
)

create_button(
    "9", 1, 2,
    command=lambda: button_click("9")
)

create_button(
    "*", 1, 3,
    bg="#ff9800",
    command=lambda: button_click("*")
)


create_button(
    "4", 2, 0,
    command=lambda: button_click("4")
)

create_button(
    "5", 2, 1,
    command=lambda: button_click("5")
)

create_button(
    "6", 2, 2,
    command=lambda: button_click("6")
)

create_button(
    "-", 2, 3,
    bg="#ff9800",
    command=lambda: button_click("-")
)


create_button(
    "1", 3, 0,
    command=lambda: button_click("1")
)

create_button(
    "2", 3, 1,
    command=lambda: button_click("2")
)

create_button(
    "3", 3, 2,
    command=lambda: button_click("3")
)

create_button(
    "+", 3, 3,
    bg="#ff9800",
    command=lambda: button_click("+")
)


create_button(
    "0", 4, 0,
    command=lambda: button_click("0")
)

create_button(
    ".", 4, 1,
    command=lambda: button_click(".")
)

create_button(
    "=", 4, 2,
    bg="#4caf50",
    command=calculate
)

create_button(
    "C", 4, 3,
    bg="#555555",
    command=clear
)


# ==============================
# CLEAR HISTORY
# ==============================

tk.Button(
    root,
    text="CLEAR HISTORY",
    font=("Arial", 10, "bold"),
    bg="#555555",
    fg="white",
    activebackground="#777777",
    bd=0,
    command=clear_history
).grid(
    row=3,
    column=0,
    pady=10,
    ipadx=10,
    ipady=5
)


# ==============================
# START APP
# ==============================

root.mainloop()