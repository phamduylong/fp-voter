import tkinter as tk
import requests
import alert
import sensor_functions as finger
import page as page
    
def attempt_login(username, password):
    credentials = {"username": username, "password": password}
    server_response = None
    try:
        server_response = requests.post("https://fingerprint-voter-server.onrender.com/login", data=credentials)
        if server_response.status_code == requests.codes.ok:
            alert.show_alert(alert.AlertType.SUCCESS, "Logged in successfully", 2.5, result_string, result_message)
            
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

main = page.MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("400x400")
root.mainloop()
