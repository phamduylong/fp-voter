import tkinter as tk
import requests
import alert
import sensor_functions as finger
import keyring as kr

def attempt_login(username, password):
    credentials = {"username": username, "password": password}
    server_response = None
    try:
        server_response = requests.post("https://fingerprint-voter-server.onrender.com/login", data=credentials)
        if server_response.status_code == requests.codes.ok:
            alert.show_alert(alert.AlertType.SUCCESS, "Logged in successfully", 2.5, result_string, result_message)

            # Get the JWT token from the server
            jwt_token = server_response.json().get("token")
            
            # Store the JWT token
            kr.set_password("fp-voter", "jwt_token", jwt_token)
            
            fingerprint_authentication_page()
        else:
            server_error = server_response.json()["error"]
            if server_error != "":
                print("An error occured: ", server_error)
                alert.show_alert(alert.AlertType.ERROR, server_error, 2.5, result_string, result_message)
    except Exception as error:
        print("An error occured: ", error)
        alert.show_alert(alert.AlertType.ERROR, error, 5, result_string, result_message)
        
def attempt_register(username, password):
    credentials = {"username": username, "password": password}
    server_response = None
    try:
        server_response = requests.post("http://fingerprint-voter-server.onrender.com/register", data=credentials)
        if server_response.status_code == requests.codes.ok:
            alert.show_alert(alert.AlertType.SUCCESS, "Registered successfully", 2.5, result_string, result_message)
        else:
            server_error = server_response.json()["error"]
            if server_error != "":
                print("An error occured: ", server_error)
                alert.show_alert(alert.AlertType.ERROR, server_error, 2.5, result_string, result_message)
    except Exception as error:
        print("An error occured: ", error)
        alert.show_alert(alert.AlertType.ERROR, error, 5, result_string, result_message)

# Retrieve the stored JWT token
def get_jwt_token():
    return kr.get_password("fp-voter", "jwt_token")
    

# Display fingerprint authentication page
def fingerprint_authentication_page():
    fingerprint_window = tk.Toplevel(root)
    fingerprint_window.title("Fingerprint Authentication")
    
    # Set window to fullscreen 
    width = fingerprint_window.winfo_screenwidth()
    height = fingerprint_window.winfo_screenheight()
    fingerprint_window.geometry("%dx%d" % (width, height))
    
    authentication_card = tk.Frame(fingerprint_window, height=660, width=1320, bg="#fff", bd=2, relief="solid")
    authentication_card.pack_propagate(0)
    authentication_card.place(in_=fingerprint_window, anchor="c", relx=.5, rely=.5)
    
    title_label = tk.Label(authentication_card, text="Fingerprint Authentication", font="helvetica 20 bold", bg="#fff")
    title_label.pack(pady=50)
    
    fingerprint_auth_result_string = tk.StringVar(value="")
    fingerprint_auth_result_message = tk.Label(authentication_card, textvariable=fingerprint_auth_result_string, justify="center", bg="#fff", font="helvetica 15")
    
    instruction_label = tk.Label(authentication_card, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
    instruction_label.pack(pady=10)
    
    fingerprint_window.update_idletasks()   # Update the display

    for attempt in range(1, 4):   
        if finger.get_fingerprint():
            alert.show_alert(alert.AlertType.SUCCESS, "Authenticated successfully!", 2.5, fingerprint_auth_result_string, fingerprint_auth_result_message)
            break
        elif attempt < 3:               # Fingerprint not found, try again (max. 2 retries)
            alert.show_alert(alert.AlertType.ERROR, f"Finger not found! Place your finger again... (Attempt {attempt + 1})", 10, fingerprint_auth_result_string, fingerprint_auth_result_message)
            fingerprint_window.update_idletasks()
        else:
            alert.show_alert(alert.AlertType.ERROR, "Fingerprint not found after 3 attempts. Please contact the election manager!", 10, fingerprint_auth_result_string, fingerprint_auth_result_message)


def exit_application():
    root.destroy()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("Fingerprint Application")

login_card = tk.Frame(root, height=660, width=1320, bg="#fff", bd=2, relief="solid")
login_label = tk.Label(login_card, text="Login", bg="#fff", font="helvetica 20 bold")
username_label = tk.Label(login_card, bg="#fff", text="Username")
username_input = tk.Entry(login_card, width=20, bg="#fff", bd=1, relief="solid")
password_label = tk.Label(login_card, bg="#fff", text="Password")
password_input = tk.Entry(login_card, show="*", width=20, bg="#fff", bd=1, relief="solid")
submit_credentials_btn = tk.Button(login_card, text="Submit", height=1, width=8, command=lambda: attempt_login(username_input.get(), password_input.get()))
# TODO: Implement register functionality
register_label = tk.Label(login_card, text="Don't have an account? Click here to register.", bg="#fff", font="helvetica 12 underline")
result_string = tk.StringVar(value="")
result_message = tk.Label(login_card, textvariable=result_string, wraplength=500, justify="center", bg="#fff", font="helvetica 14")

login_label.pack(pady=50)
username_label.pack(pady=10)
username_input.pack(pady=5)
password_label.pack(pady=10)
password_input.pack(pady=5)
submit_credentials_btn.pack(pady=30)
register_label.pack(pady=10)
login_card.pack_propagate(0)
login_card.place(in_=root, anchor="c", relx=.5, rely=.5)
root.mainloop()
