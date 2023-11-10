import tkinter as tk 
#import sensor_functions as finger
import alert

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
        
class Page(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
	def show(self):
		self.lift()
            
class GreetingPage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		label = tk.Label(self, text="Welcome to the fingerprint voter!\nNavigate to different pages with the buttons at the top of the page.")
		label.pack(side="top", fill="both", expand=True)

class LoginPage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		title_label = tk.Label(self, text="Login to system", font="helvetica 20 bold", bg="#fff")
		title_label.pack(side="top", fill="both", expand=True)
        
		username_label = tk.Label(self, bg="#fff", text="Username")
		username_input = tk.Entry(self, width=20, bg="#fff", bd=1, relief="solid")
		password_label = tk.Label(self, bg="#fff", text="Password")
		password_input = tk.Entry(self, show="*", width=20, bg="#fff", bd=1, relief="solid")
		submit_credentials_btn = tk.Button(self, text="Submit", height=1, width=8, command=lambda: attempt_login(username_input.get(), password_input.get()))
		register_user_btn = tk.Button(self, text="Don't have an account? Click here to register.", bg="#fff", font="helvetica 12 underline", command=lambda: attempt_login(username_input.get(), password_input.get()))
		result_string = tk.StringVar(value="")
		result_message = tk.Label(self, textvariable=result_string, wraplength=500, justify="center", bg="#fff", font="helvetica 14")

		username_label.pack(pady=10)
		username_input.pack(pady=5)
		password_label.pack(pady=10)
		password_input.pack(pady=5)
		submit_credentials_btn.pack(pady=30)
		register_user_btn.pack(pady=10)

class RegisterPage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		label = tk.Label(self, text="Register page")
		label.pack(side="top", fill="both", expand=True)

class VotePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		title_label = tk.Label(self, text="Fingerprint Authentication", font="helvetica 20 bold", bg="#fff")
		title_label.pack(side="top", fill="both", expand=True)

		fingerprint_auth_result_string = tk.StringVar(value="")
		fingerprint_auth_result_message = tk.Label(self, textvariable=fingerprint_auth_result_string, justify="center", bg="#fff", font="helvetica 15")

		instruction_label = tk.Label(self, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
		instruction_label.pack(side="top", fill="both", expand=True)
		
		btn = tk.Button(self, text="Search", command=lambda: print('''finger.search_location(1)'''))
		btn.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		p0 = GreetingPage(self)
		p1 = LoginPage(self)
		p2 = RegisterPage(self)
		p3 = VotePage(self)

		buttonframe = tk.Frame(self)
		container = tk.Frame(self)
		buttonframe.pack(side="top", fill="x", expand=False)
		container.pack(side="top", fill="both", expand=True)

		p0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		b1 = tk.Button(buttonframe, text="Login", command=p1.show)
		b2 = tk.Button(buttonframe, text="Reqister", command=p2.show)
		b3 = tk.Button(buttonframe, text="Vote", command=p3.show)

		b1.pack(side="left")
		b2.pack(side="left")
		b3.pack(side="left")

		p0.show()
root = tk.Tk()
main = MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("400x400")
root.mainloop()
