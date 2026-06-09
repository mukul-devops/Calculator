import customtkinter as ctk
import math

# ---------------- APP ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Calculator")
app.geometry("500x750")
app.minsize(400, 650)

# ---------------- GRID ----------------

for i in range(8):
    app.grid_rowconfigure(i, weight=1)

for j in range(4):
    app.grid_columnconfigure(j, weight=1)

# ---------------- ENTRY ----------------

entry = ctk.CTkEntry(
    app,
    font=("Arial", 32),
    justify="right",
    height=70
)
entry.grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=15,
    pady=15
)

entry.focus_set()   # IMPORTANT: auto keyboard focus

# ---------------- HISTORY ----------------

history = ctk.CTkTextbox(
    app,
    font=("Arial", 14),
    height=150
)
history.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=15,
    pady=10
)

# ---------------- FUNCTIONS ----------------

def add_history(text):
    history.insert("end", text + "\n")
    history.see("end")

def click(value):
    entry.insert("end", value)

def clear():
    entry.delete(0, "end")

def backspace():
    current = entry.get()
    entry.delete(0, "end")
    entry.insert(0, current[:-1])

def calculate():
    try:
        expression = entry.get()

        # Convert ^ to Python power
        expression = expression.replace("^", "**")

        result = eval(expression)

        add_history(f"{entry.get()} = {result}")

        entry.delete(0, "end")
        entry.insert(0, result)

    except:
        entry.delete(0, "end")
        entry.insert(0, "Error")

def square_root():
    try:
        value = float(entry.get())
        result = math.sqrt(value)

        add_history(f"sqrt({value}) = {result}")

        entry.delete(0, "end")
        entry.insert(0, result)

    except:
        entry.delete(0, "end")
        entry.insert(0, "Error")

# ---------------- BUTTON CREATION ----------------

def make_button(text, row, col, command):
    btn = ctk.CTkButton(
        app,
        text=text,
        command=command,
        font=("Arial", 20),
        corner_radius=15,
        height=70
    )
    btn.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=8,
        pady=8
    )

# ---------------- BUTTONS ----------------

buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('%', 5, 2), ('+', 5, 3),
]

for (text, row, col) in buttons:
    make_button(text, row, col, lambda t=text: click(t))

# ---------------- SPECIAL BUTTONS ----------------

make_button("Clear", 6, 0, clear)
make_button("⌫", 6, 1, backspace)
make_button("√", 6, 2, square_root)
make_button("=", 6, 3, calculate)

make_button("^", 7, 0, lambda: click("^"))

# ---------------- KEYBOARD SUPPORT (FIXED) ----------------

def keyboard(event):

    key = event.char
    allowed = "1234567890+-*/.%^"

    # normal keys
    if key in allowed:
        return  # IMPORTANT: prevents double typing

    # Enter key
    if event.keysym == "Return":
        calculate()
        return "break"

    # Backspace
    if event.keysym == "BackSpace":
        backspace()
        return "break"

# Bind only to entry (IMPORTANT FIX)
entry.bind("<KeyPress>", keyboard)

# ---------------- RUN ----------------

app.mainloop()
