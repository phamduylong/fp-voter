import tkinter as tk
import page as page
import requests
import alert
import sensor_functions as finger
import keyring as kr
import subprocess

def install_python_dbus():
    command = "sudo apt-get install python3-dbus"
    try:
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode == 0:
            print("python-dbus installed successfully")
    except subprocess.CalledProcessError as error:
        print(f"Installation failed with an error: {error}")
        alert.show_alert(alert.AlertType.ERROR, error, 5, result_string, result_message)
        
# Install python-dbus if not installed
try:
    import dbus
except ImportError:
    install_python_dbus()

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
main = page.MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("400x400")
root.mainloop()