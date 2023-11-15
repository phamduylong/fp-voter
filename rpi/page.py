import tkinter as tk 
import requests
import sensor_functions as finger
import alert

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i

def attempt_login(self, username, password):
    credentials = {"username": username, "password": password}
    server_response = None
    try:
        server_response = requests.post("https://fingerprint-voter-server.onrender.com/login", data=credentials)
        if server_response.status_code == requests.codes.ok:
            alert.show_alert(alert.AlertType.SUCCESS, "Logged in successfully", 2.5, self.result_string, self.result_message)
        else:
            server_error = server_response.json()["error"]
            if server_error != "":
                print("An error occured: ", server_error)
                alert.show_alert(alert.AlertType.ERROR, server_error, 2.5, self.result_string, self.result_message)
    except Exception as error:
        print("An error occured: ", error)
        alert.show_alert(alert.AlertType.ERROR, error, 5, self.result_string, self.result_message)
        
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


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.p0 = GreetingPage(self)
        self.p1 = LoginPage(self)
        self.p2 = RegisterPage(self)
        self.p3 = VotePage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        b1 = tk.Button(buttonframe, text="Login", command=self.show_login_page)
        b2 = tk.Button(buttonframe, text="Register", command=self.show_register_page)
        b3 = tk.Button(buttonframe, text="Vote", command=self.show_vote_page)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        self.p0.pack(fill="both", expand=True)
        self.p1.pack(fill="both", expand=True)
        self.p2.pack(fill="both", expand=True)
        self.p3.pack(fill="both", expand=True)

        self.show_greeting_page()

    def show_greeting_page(self):
        self.p0.pack(fill="both", expand=True)
        self.p1.pack_forget()
        self.p2.pack_forget()
        self.p3.pack_forget()

    def show_login_page(self):
        self.p0.pack_forget()
        self.p1.pack(fill="both", expand=True)
        self.p2.pack_forget()
        self.p3.pack_forget()

    def show_register_page(self):
        self.p0.pack_forget()
        self.p1.pack_forget()
        self.p2.pack(fill="both", expand=True)
        self.p3.pack_forget()

    def show_vote_page(self):
        self.p0.pack_forget()
        self.p1.pack_forget()
        self.p2.pack_forget()
        self.p3.pack(fill="both", expand=True)
        
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        self.pack(fill="both", expand=True)  # Make sure the page is packed to be visible


class RegisterPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Register page", font="helvetica 20 bold", bg="#fff")
        label.pack(side="top", fill="both", expand=True)

        username_label = tk.Label(self, bg="#fff", text="Username")
        username_input = tk.Entry(self, width=20, bg="#fff", bd=1, relief="solid")
        password_label = tk.Label(self, bg="#fff", text="Password")
        password_input = tk.Entry(self, show="*", width=20, bg="#fff", bd=1, relief="solid")
        register_user_btn = tk.Button(self, text="Register", height=1, width=8,
                                      command=lambda: attempt_register(username_input.get(), password_input.get()))

        username_label.pack(pady=10)
        username_input.pack(pady=5)
        password_label.pack(pady=10)
        password_input.pack(pady=5)
        register_user_btn.pack(pady=10)
        
class VotePage(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.title_label = tk.Label(self, text="Fingerprint Authentication", font="helvetica 20 bold", bg="#fff")
		self.title_label.pack(side="top", fill="both", expand=True)
		self.fingerprint_auth_result_string = tk.StringVar(value="")
		self.fingerprint_auth_result_message = tk.Label(self, textvariable=self.fingerprint_auth_result_string, justify="center", bg="#fff", font="helvetica 15")
		self.fingerprint_auth_result_message.pack(side="top", fill="both", expand=True)
		self.instruction_label = tk.Label(self, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
		self.instruction_label.pack(side="top", fill="both", expand=True)
		self.btn = tk.Button(self, text="Search", command=self.authenticate_fingerprint)
		self.btn.pack(side="top", fill="both", expand=True)

		# Additional components for vote options
		self.vote_buttons_frame = tk.Frame(self)
		self.vote_buttons_frame.pack(side="top", fill="both", expand=True)

		# Vote option buttons
		self.vote_button_1 = tk.Button(self.vote_buttons_frame, text="Joe Biden", command=lambda: self.cast_vote(1))
		self.vote_button_2 = tk.Button(self.vote_buttons_frame, text="Kendrick Lamar", command=lambda: self.cast_vote(2))
		self.vote_button_3 = tk.Button(self.vote_buttons_frame, text="Beyoncé", command=lambda: self.cast_vote(3))
        
	def authenticate_fingerprint(self):
		# Add your fingerprint authentication logic here
		location = 1
		#fingerprint_auth_result = finger.search_location(1)  # Replace this with your actual fingerprint authentication logic
		for attempt in range(1, 4):
			if finger.search_location(location):
				alert.show_alert(alert.AlertType.SUCCESS, "Authenticated successfully!", 2.5, self.fingerprint_auth_result_string, self.fingerprint_auth_result_message)
				self.fingerprint_auth_result = "success"
				break
			elif attempt < 3:               # Fingerprint not found, try again (max. 2 retries)
				alert.show_alert(alert.AlertType.ERROR, f"Finger not found! Place your finger again... (Attempt {attempt + 1})", 10, self.fingerprint_auth_result_string, self.fingerprint_auth_result_message)
			else:
				alert.show_alert(alert.AlertType.ERROR, "Fingerprint not found after 3 attempts. Please contact the election manager!", 10, self.fingerprint_auth_result_string, self.fingerprint_auth_result_message)
				self.fingerprint_auth_result = "failure"
				self.user_not_found()
		if self.fingerprint_auth_result == "success":
			self.fingerprint_auth_result_string.set("Fingerprint Authentication Successful")
			self.show_vote_options()
		else:
			self.fingerprint_auth_result_string.set("Fingerprint Authentication Failed")
			self.show_failure()

	def show_vote_options(self):
		# Clear existing components
		self.title_label.pack_forget()
		self.fingerprint_auth_result_message.pack_forget()
		self.instruction_label.pack_forget()
		self.btn.pack_forget()

		# Show vote options
		self.title_label.config(text="Cast your vote!", font="helvetica 20 bold")
		self.title_label.pack(side="top", fill="both", expand=True)

		self.vote_button_1.pack(side="top", fill="both", expand=True)
		self.vote_button_2.pack(side="top", fill="both", expand=True)
		self.vote_button_3.pack(side="top", fill="both", expand=True)
        
	def user_not_found(self):
		# Clear existing components
		self.title_label.pack_forget()
		self.fingerprint_auth_result_message.pack_forget()
		self.instruction_label.pack_forget()
		self.btn.pack_forget()

		self.vote_button_1.pack_forget()
		self.vote_button_2.pack_forget()
		self.vote_button_3.pack_forget()
        
		# Show failure
		self.title_label.config(text="Error authenticating user!", font="helvetica 20 bold")
		self.title_label.pack(side="top", fill="both", expand=True)

	def cast_vote(self, candidate):
		# TO-DO: logic for vote casting here
		self.fingerprint_auth_result_string.set(f"Vote for Candidate {candidate} cast successfully!")
		self.farewell_message()

	def farewell_message(self):
		# Clear existing components
		self.title_label.pack_forget()
		self.fingerprint_auth_result_message.pack_forget()
		self.instruction_label.pack_forget()
		self.vote_button_1.pack_forget()
		self.vote_button_2.pack_forget()
		self.vote_button_3.pack_forget()
		# Show farewell msg
		self.title_label.config(text="Thank you for voting!", font="helvetica 20 bold")
		self.title_label.pack(side="top", fill="both", expand=True)

        
class LoginPage(Page):
	def __init__(self, main_view, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.main_view = main_view  # Store a reference to the MainView instance
		self.title_label = tk.Label(self, text="Login to system", font="helvetica 20 bold", bg="#fff")
		self.title_label.pack(side="top", fill="both", expand=True)
		self.username_label = tk.Label(self, bg="#fff", text="Username")
		self.username_input = tk.Entry(self, width=20, bg="#fff", bd=1, relief="solid")
		self.password_label = tk.Label(self, bg="#fff", text="Password")
		self.password_input = tk.Entry(self, show="*", width=20, bg="#fff", bd=1, relief="solid")
		self.submit_credentials_btn = tk.Button(self, text="Submit", height=1, width=8, command=lambda: attempt_login(self, self.username_input.get(), self.password_input.get()))
		self.register_user_btn = tk.Button(self, text="Don't have an account? Click here to register.", bg="#fff", font="helvetica 12 underline", command=lambda: self.main_view.show_register_page())
		self.result_string = tk.StringVar(value="")
		self.result_message = tk.Label(self, textvariable=self.result_string, wraplength=500, justify="center", bg="#fff", font="helvetica 14")
		self.username_label.pack(pady=10)
		self.username_input.pack(pady=5)
		self.password_label.pack(pady=10)
		self.password_input.pack(pady=5)
		self.submit_credentials_btn.pack(pady=30)
		self.register_user_btn.pack(pady=10)
        
class GreetingPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Welcome to the fingerprint voter!\nNavigate to different pages with the buttons at the top of the page.")
        label.pack(side="top", fill="both", expand=True)
