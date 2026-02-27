#-------------***importing libraries***----------------------
import tkinter as tk
from tkinter import ttk, messagebox

# ----------***Users***------------------------------------
USERS = {
    "teacher": {"password": "teacher123", "role": "teacher"},
    "parent": {"password": "parent123", "role": "parent"}
}
#----------***Sample student data just for the UI***-------------------------
students = [
    {"id": "S001", "name": "Alice Johnson", "module": "Mathematics", "average": 75},
    {"id": "S002", "name": "Bob Smith", "module": "Science", "average": 62},
    {"id": "S003", "name": "Charlie Brown", "module": "English", "average": 48},
]
#--------------------***Main Window (Dashboard) UI***-------------------------
def build_main_window(role):
    root = tk.Tk()
    root.title("Academic Performance DSS")
    root.geometry("1200x600")
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

 #--------------***Teacher-only Buttons (UI only)***----------------------
    if role == "teacher":
        tk.Button(btn_frame, text="Import CSV", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sort Table", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Module Distribution", width=18).pack(side=tk.LEFT, padx=5)

    tk.Button(btn_frame, text="Search Student", width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="At Risk Status", width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Predicted Grade", width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Export Report", width=18).pack(side=tk.LEFT, padx=5)
   
    tk.Button(btn_frame, text="Close", width=15,command=root.destroy).pack(side=tk.LEFT, padx=5)

    #--------------------***Student Data Table***----------------------
    table_frame = tk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    columns = ("Student ID", "Name", "Module", "Average")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=250, anchor="center")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for s in students:
        tree.insert("", "end", values=(
            s["id"], s["name"], s["module"], s["average"]
        ))

    root.mainloop()

#--------------------***Login Functionality***----------------------
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USERS and USERS[username]["password"] == password:
        role = USERS[username]["role"]
        messagebox.showinfo("Login Successful", f"Welcome! Role: {role}")
        login_window.destroy()
        build_main_window(role)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def reset_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    username_entry.focus()

#--------------------***Login Window UI***----------------------
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x280")

tk.Label(login_window, text="Username").pack(pady=5)
username_entry = tk.Entry(login_window, width=25)
username_entry.pack()

tk.Label(login_window, text="Password").pack(pady=5)
password_entry = tk.Entry(login_window, show="*", width=25)
password_entry.pack()

tk.Button(login_window, text="Login", width=20,command=login).pack(pady=8)
tk.Button(login_window, text="Reset", width=20,command=reset_fields).pack(pady=5)
login_window.mainloop()