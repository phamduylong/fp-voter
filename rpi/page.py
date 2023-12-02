import tkinter as tk 
import requests
import sensor_functions as finger
import alert
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

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i


# Retrieve the stored JWT token
def get_jwt_token():
    return kr.get_password("fp-voter", "jwt_token")
    

class MainView(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.p0 = GreetingPage(self)
		self.p1 = LoginPage(self)
		self.p2 = RegisterPage(self)
		self.p3 = VotePage(self)
		self.location = 0
	
		buttonframe = tk.Frame(self)
		container = tk.Frame(self)
		buttonframe.pack(side="top", fill="x", expand=False)
		container.pack(side="top", fill="both", expand=True)

		b1 = tk.Button(buttonframe, text="Login", command=self.show_login_page)
		b2 = tk.Button(buttonframe, text="Register", command=self.show_register_page)

		b1.pack(side="left")
		b2.pack(side="left")

		self.p0.pack(fill="both", expand=True)
		self.p1.pack(fill="both", expand=True)
		self.p2.pack(fill="both", expand=True)

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
        
	def update_location(self, location):
		self.location = location
        
	def clear_input_fields(self, username_input, password_input):
		username_input.delete(0, tk.END)
		password_input.delete(0, tk.END)

	def schedule_label_clear(self, label_widget, delay):
		self.after(delay, lambda: label_widget.pack_forget())
        
        
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()
        self.pack(fill="both", expand=True)  # Make sure the page is packed to be visible


class RegisterPage(Page):
	def __init__(self, main_view, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.main_view = main_view  # Store a reference to the MainView instance
		self.label = tk.Label(self, text="Register page", font="helvetica 20 bold", bg="#fff")
		self.label.pack(side="top", fill="both", expand=True)

		self.username_label = tk.Label(self, bg="#fff", text="Username")
		self.username_input = tk.Entry(self, width=20, bg="#fff", bd=1, relief="solid")
		self.password_label = tk.Label(self, bg="#fff", text="Password")
		self.password_input = tk.Entry(self, show="*", width=20, bg="#fff", bd=1, relief="solid")
		
		self.result_string = tk.StringVar(value="")
		self.result_message = tk.Label(self, textvariable=self.result_string, wraplength=500, justify="center", bg="#fff", font="helvetica 14")
		
		self.register_user_btn = tk.Button(self, text="Register", height=1, width=8, command=lambda: attempt_register(self, self.username_input.get(), self.password_input.get(), self.fingerprintId))
		
		self.enrollment_result_string = tk.StringVar(value="")
		self.enrollment_result_message = tk.Label(self, textvariable=self.enrollment_result_string, wraplength=500, justify="center", bg="#fff", font="helvetica 14")

		self.fingerprint_enrollment_btn = tk.Button(self, text="Fingerprint Enrollment", height=1, width=16, command=lambda: enroll_fingerprint(self))
		
		self.register_success_label = tk.Label(self, text="Registered successfully!", font="helvetica 15", bg="#fff", foreground="green")

		self.first_img_instruction_label = tk.Label(self, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
		self.second_img_instruction_label = tk.Label(self, text="Place the same finger again...", font="helvetica 15", bg="#fff")
		self.img_error_label = tk.Label(self, text="Error while capturing finger image", font="helvetica 15", bg="#fff", foreground="red")
		self.storage_error_label = tk.Label(self, text="Error while storing the fingerprint", font="helvetica 15", bg="#fff", foreground="red")
		self.enrollment_success_label = tk.Label(self, text="Enrolled successfully!", font="helvetica 15", bg="#fff", foreground="green")

		self.username_label.pack(pady=10)
		self.username_input.pack(pady=5)
		self.password_label.pack(pady=10)
		self.password_input.pack(pady=5)
		self.fingerprint_enrollment_btn.pack(pady=10)
		self.register_user_btn.pack(pady=10)
		
		def attempt_register(self, username, password, fingerprintId):
			payload = {"username": username, "password": password, "fingerprintId": fingerprintId, "sensorId": 1}
			server_response = None
			try:
				server_response = requests.post("http://fingerprint-voter-server.onrender.com/register", data=payload)
				if server_response.status_code == requests.codes.ok:
					self.register_success_label.pack(pady=10)
					
					self.main_view.schedule_label_clear(self.register_success_label, 3000)		# Hide the label after 3 seconds
					
					self.main_view.clear_input_fields(self.username_input, self.password_input)	# Clear username & password input fields
				else:
					server_error = server_response.json()["error"]
					if server_error != "":
						print("An error occured: ", server_error)
						self.register_error_label = tk.Label(self, text=str(server_error), font="helvetica 15", bg="#fff", foreground="red")
						self.register_error_label.pack(pady=10)
						
						self.main_view.schedule_label_clear(self.register_error_label, 5000)
						
						finger.clear_location(fingerprintId)
			except Exception as error:
				print("An error occured: ", error)
				self.exception_label = tk.Label(self, text=str(error), font="helvetica 15", bg="#fff", foreground="red")
				self.exception_label.pack(pady=10)
				
				self.main_view.schedule_label_clear(self.exception_label, 5000)
				
				finger.clear_location(fingerprintId)
		
		def get_empty_location(self):
			min_location = 1
			max_location = 127
			locations = finger.read_templates()
			
			locations_set = set(locations)
			
			# Find the value not in the locations set and return the first value found
			for value in range(min_location, max_location + 1):
				if value not in locations_set:
					return value

			return None

		def enroll_fingerprint(self):
			# Get an empty location on the sensor's flash
			empty_location = get_empty_location(self)
			
			# Prompt the user to capture the finger image for the first time
			self.first_img_instruction_label.pack(pady=10)

			self.update_idletasks()
			
			# Capture finger image for the first time
			if finger.capture_img(1):
				# If successful, prompt the user to capture the finger image for the second time
				self.second_img_instruction_label.pack(pady=10)
			else:
				# If an error occured, hide the instruction labels and display error message
				self.first_img_instruction_label.pack_forget()
				self.second_img_instruction_label.pack_forget()
				
				# Display error message
				self.img_error_label.pack(pady=10)
				
				self.main_view.schedule_label_clear(self.img_error_label, 5000)
				return
				
			self.update_idletasks()
			
			# Capture finger image for the second time
			if finger.capture_img(2):
				# If successful, store the image in an empty location on the flash
				if finger.store_finger(empty_location):
					# Hide the instruction labels
					self.first_img_instruction_label.pack_forget()
					self.second_img_instruction_label.pack_forget()
					
					# Display the success message
					self.enrollment_success_label.pack(pady=10)
					
					self.main_view.schedule_label_clear(self.enrollment_success_label, 3000)
					
					self.fingerprintId = empty_location	# Set the fingerprintId after successful enrollment
				else:
					self.first_img_instruction_label.pack_forget()
					self.second_img_instruction_label.pack_forget()
					
					# Display error message
					self.storage_error_label.pack(pady=10)
					
					self.main_view.schedule_label_clear(self.storage_error_label, 5000)
			else:
				self.first_img_instruction_label.pack_forget()
				self.second_img_instruction_label.pack_forget()
				
				# Display error message
				self.img_error_label.pack(pady=10)
				
				self.main_view.schedule_label_clear(self.img_error_label, 5000)


    
        ###########login bypass
class VotePage(Page):
	def __init__(self, main_view, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.main_view = main_view
		
		# Create a frame
		self.fingerprint_auth_frame = tk.Frame(self, height=660, width=1320, bg="#fff", bd=2, relief="solid")
		self.fingerprint_auth_frame.pack_propagate(0)
		
		self.title_label = tk.Label(self.fingerprint_auth_frame, text="Fingerprint Authentication", font="helvetica 20 bold", bg="#fff")
		self.title_label.pack(pady=50)
		
		self.fingerprint_auth_result_string = tk.StringVar(value="")
		
		self.btn = tk.Button(self.fingerprint_auth_frame, text="Start Authentication", command=self.authenticate_fingerprint)
		self.btn.pack(pady=50)
		
		self.instruction_label = tk.Label(self.fingerprint_auth_frame, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")

		# Additional components for vote options
		self.vote_buttons_frame = tk.Frame(self)
		self.vote_buttons_frame.pack()

		# Vote option buttons
		self.vote_button_1 = tk.Button(self.vote_buttons_frame, text="Joe Biden", command=lambda: self.cast_vote(1))
		self.vote_button_2 = tk.Button(self.vote_buttons_frame, text="Kendrick Lamar", command=lambda: self.cast_vote(2))
		self.vote_button_3 = tk.Button(self.vote_buttons_frame, text="Beyoncé", command=lambda: self.cast_vote(3))
		
		self.fingerprint_auth_success_label = tk.Label(self.fingerprint_auth_frame, text="Authenticated successfully!", font="helvetica 15", bg="#fff", foreground="green")
		self.fingerprint_auth_failure_label = tk.Label(self.fingerprint_auth_frame, text="Fingerprint not found after 3 attempts. Please contact the election manager!", font="helvetica 20", bg="#fff", foreground="red")
        
		self.fingerprint_auth_frame.pack()
	def authenticate_fingerprint(self):
		self.instruction_label.pack(pady=10)

		# Get the location
		location = self.main_view.location
		
		self.update_idletasks()
		
		for attempt in range(1, 4):
			if finger.search_location(location):
				self.fingerprint_auth_success_label.pack(pady=10)	# Show success label
				self.main_view.schedule_label_clear(self.fingerprint_auth_success_label, 3000)	# Hide the label after 3 seconds

				self.fingerprint_auth_result = "success"
				break
			elif attempt < 3:               # Fingerprint not found, try again (max. 2 retries)
				self.fingerprint_auth_error_label = tk.Label(self.fingerprint_auth_frame, text=f"Finger not found! Place your finger again... (Attempt {attempt + 1})", font="helvetica 15", bg="#fff", foreground="red")
				self.fingerprint_auth_error_label.pack(pady=10)
				
				self.main_view.schedule_label_clear(self.fingerprint_auth_error_label, 5000)		# Hide the label after 5 seconds

				self.update_idletasks()
			else:
				self.fingerprint_auth_error_label.pack_forget()		# Hide all error messages 
				
				#self.fingerprint_auth_failure_label.pack(pady=10)	# Show failure label
				#self.main_view.schedule_label_clear(self.fingerprint_auth_failure_label, 5000)

				self.fingerprint_auth_result = "failure"
		if self.fingerprint_auth_result == "success":
			self.fingerprint_auth_result_string.set("Fingerprint Authentication Successful")
			self.show_vote_options()
		else:
			self.fingerprint_auth_result_string.set("Fingerprint Authentication Failed")
			self.user_not_found()
			#self.show_vote_options()

	def show_vote_options(self):
		# Clear existing components
		self.title_label.pack_forget()
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
		self.instruction_label.pack_forget()
		self.btn.pack_forget()

		self.vote_button_1.pack_forget()
		self.vote_button_2.pack_forget()
		self.vote_button_3.pack_forget()
        
		# Show failure
		self.fingerprint_auth_failure_label.pack(side="top", fill="both", expand=True)	# Show failure label
		#self.title_label.config(text="Error authenticating user!", font="helvetica 20 bold")
		#self.title_label.pack()

	def cast_vote(self, candidate):
		# TO-DO: logic for vote casting here
		self.fingerprint_auth_result_string.set(f"Vote for Candidate {candidate} cast successfully!")
		self.farewell_message()

	def farewell_message(self):
		# Clear existing components
		self.title_label.pack_forget()
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
		
		# Create a login frame
		login_frame = tk.Frame(self, height=660, width=1320, bg="#fff", bd=2, relief="solid")
		login_frame.pack_propagate(0)
		
		self.title_label = tk.Label(login_frame, text="Login", font="helvetica 20 bold", bg="#fff")
		self.title_label.pack(pady=50)
		
		self.username_label = tk.Label(login_frame, bg="#fff", text="Username")
		self.username_input = tk.Entry(login_frame, width=20, bg="#fff", bd=1, relief="solid")
		self.password_label = tk.Label(login_frame, bg="#fff", text="Password")
		self.password_input = tk.Entry(login_frame, show="*", width=20, bg="#fff", bd=1, relief="solid")
		
		self.submit_credentials_btn = tk.Button(login_frame, text="Submit", height=1, width=8, cursor="hand2", command=lambda: attempt_login(self, self.username_input.get(), self.password_input.get()))
		self.register_user_btn = tk.Button(login_frame, text="Don't have an account? Click here to register.", font="helvetica 12 underline", relief=tk.FLAT, cursor="hand2",  borderwidth=0, highlightthickness=0, bg="#fff", activebackground="#fff", command=lambda: self.main_view.show_register_page())
		
		self.result_string = tk.StringVar(value="")
		self.result_message = tk.Label(self, textvariable=self.result_string, wraplength=500, justify="center", bg="#fff", font="helvetica 14")
		
		self.login_success_label = tk.Label(login_frame, text="Logged in successfully!", font="helvetica 15", bg="#fff", foreground="green")

		self.username_label.pack(pady=10)
		self.username_input.pack(pady=5)
		self.password_label.pack(pady=10)
		self.password_input.pack(pady=5)
		self.submit_credentials_btn.pack(pady=30)
		self.register_user_btn.pack(pady=10)
		
		login_frame.pack()
		
		def attempt_login(self, username, password):
			###########login bypass
			#self.main_view.show_vote_page()

			credentials = {"username": username, "password": password}
			server_response = None
			try:
				server_response = requests.post("https://fingerprint-voter-server.onrender.com/login", data=credentials)
				if server_response.status_code == requests.codes.ok:
					# Show success label
					self.login_success_label.pack(pady=10)
					
					self.main_view.schedule_label_clear(self.login_success_label, 3000)		# Hide the label after 3 seconds
					
					# Get the JWT token from the server
					jwt_token = server_response.json().get("token")

					# Store the JWT token
					kr.set_password("fp-voter", "jwt_token", jwt_token)
					
					# Get the fingerprint Id
					fingerprintId = server_response.json().get("fingerprintId")
					
					# Update the location
					self.main_view.update_location(fingerprintId)
					
					self.main_view.clear_input_fields(self.username_input, self.password_input)	# Clear username & password input fields
					
					self.main_view.show_vote_page()
				else:
					server_error = server_response.json()["error"]
					if server_error != "":
						print("An error occured: ", server_error)
						self.login_error_label = tk.Label(login_frame, text=str(server_error), font="helvetica 15", bg="#fff", foreground="red")
						self.login_error_label.pack(pady=10)
						
						self.main_view.schedule_label_clear(self.login_error_label, 5000)	# Hide the label after 5 seconds
			except Exception as error:
				print("An error occured: ", error)
				self.exception_label = tk.Label(login_frame, text=str(error), font="helvetica 15", bg="#fff", foreground="red")
				self.exception_label.pack(pady=10)
						
				self.main_view.schedule_label_clear(self.exception_label, 5000)
        
class GreetingPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Welcome to the fingerprint voter!\nNavigate to different pages with the buttons at the top of the page.")
        label.pack(side="top", fill="both", expand=True)
