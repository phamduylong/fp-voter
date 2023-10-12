import tkinter as tk
import requests
import threading

def attempt_login():
    credentials = {"username": username.get(), "password": password.get()}
    server_response = requests.post("http://localhost:8080/login", data=credentials)
    if server_response.status_code == requests.codes.ok:
        result_string.set("Logged in successfully")
        result_message.config(fg="#0f0")
        result_message.pack(pady=30)
        t = threading.Timer(2.5, pop_result)
        t.start()
    else:
        server_error = server_response.json()["error"]
        if server_error != "":
            result_string.set(server_error)
            result_message.config(fg="#f00")
            result_message.pack(pady=30)
            t = threading.Timer(2.5, pop_result)
            t.start()

def pop_result():
    hide(result_message)
            
def hide(element):
    element.pack_forget()
        
def exit_application():
    root.destroy()

root = tk.Tk()
root.geometry("1600x900")
root.title("Fingerprint Application")

username_label = tk.Label(root, text="Username")
username = tk.Entry(root, width=20)
password_label = tk.Label(root, text="Password")
password = tk.Entry(root, show="*", width=20)
submit_credentials_btn = tk.Button(root, text="Submit", height=1, width=8, command=attempt_login)

result_string = StringVar()
result_message = tk.Label(root, textvariable=result_string)

username_label.pack(pady=10)
username.pack(pady=5)
password_label.pack(pady=10)
password.pack(pady=5)
submit_credentials_btn.pack(pady=30)

root.mainloop()