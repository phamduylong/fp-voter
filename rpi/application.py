import tkinter as tk
import requests
import alert
import sensor_functions

def attempt_login():
    credentials = {"username": username.get(), "password": password.get()}
    server_response = None
    try:
        server_response = requests.post("http://localhost:8080/login", data=credentials)
        if server_response.status_code == requests.codes.ok:
            alert.show_alert(alert.Alert_Type.SUCCESS, "Logged in successfully", 2.5, result_string, result_message)
        else:
            server_error = server_response.json()["error"]
            if server_error != "":
                print("An error occured: ", server_error)
                alert.show_alert(alert.Alert_Type.ERROR, server_error, 2.5, result_string, result_message)
    except Exception as error:
        print("An error occured: ", error)
        alert.show_alert(alert.Alert_Type.ERROR, error, 5, result_string, result_message)
        
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

result_string = tk.StringVar()
result_message = tk.Label(root, textvariable=result_string, wraplength=400, justify="center", font="helvetica 14")

#enroll_btn = tk.Button(root, text="Enroll fingerprint", height=1, width=8, command=enroll_finger)

username_label.pack(pady=10)
username.pack(pady=5)
password_label.pack(pady=10)
password.pack(pady=5)
submit_credentials_btn.pack(pady=30)
#enroll_btn.pack(pady=30)

root.mainloop()