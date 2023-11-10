import tkinter as tk
import requests
import alert
import page as page
#import sensor_functions as finger

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i


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
        if get_num() > 1:
        #if finger.get_fingerprint():
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