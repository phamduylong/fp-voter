import tkinter as tk 
import requests
import sensor_functions as finger
import alert
import keyring as kr
import subprocess
import tkinter.messagebox
import jwt

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
		self.p3.show_fingerprint_frame()
        
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
		
		# Create a register frame
		register_frame = tk.Frame(self, height=660, width=1320, bg="#fff", bd=2, relief="solid")
		register_frame.pack_propagate(0)
		
		self.label = tk.Label(register_frame, text="Register", font="helvetica 20 bold", bg="#fff")
		self.label.pack(pady=50)
		self.username_instruction_label = tk.Label(register_frame, bg="#fff", text="Username needs to be 6-20 characters long, no special characters.")
		self.password_instruction_label = tk.Label(register_frame, bg="#fff", text="Password needs to be at least 8 characters long, contain a capital letter, a number and a special character.")
		self.username_label = tk.Label(register_frame, bg="#fff", text="Username")
		self.username_input = tk.Entry(register_frame, width=20, bg="#fff", bd=1, relief="solid")
		self.password_label = tk.Label(register_frame, bg="#fff", text="Password")
		self.password_input = tk.Entry(register_frame, show="*", width=20, bg="#fff", bd=1, relief="solid")
		
		self.register_user_btn = tk.Button(register_frame, text="Register", height=1, width=8, command=lambda: attempt_register(self, self.username_input.get(), self.password_input.get(), self.fingerprintId))
		self.fingerprint_enrollment_btn = tk.Button(register_frame, text="Fingerprint Enrollment", height=1, width=16, command=lambda: enroll_fingerprint(self))
		
		self.register_success_label = tk.Label(register_frame, text="Registered successfully!", font="helvetica 15", bg="#fff", foreground="green")

		self.first_img_instruction_label = tk.Label(register_frame, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
		self.second_img_instruction_label = tk.Label(register_frame, text="Place the same finger again...", font="helvetica 15", bg="#fff")
		self.img_error_label = tk.Label(register_frame, text="Error while capturing finger image. Please contact the election manager.", font="helvetica 15", bg="#fff", foreground="red")
		self.storage_error_label = tk.Label(register_frame, text="Error while storing the fingerprint. Please contact the election manager.", font="helvetica 15", bg="#fff", foreground="red")
		self.enrollment_success_label = tk.Label(register_frame, text="Enrolled successfully!", font="helvetica 15", bg="#fff", foreground="green")
		
		self.username_instruction_label.pack(pady=5)
		self.password_instruction_label.pack(pady=5)
		self.username_label.pack(pady=10)
		self.username_input.pack(pady=5)
		self.password_label.pack(pady=10)
		self.password_input.pack(pady=5)
		self.fingerprint_enrollment_btn.pack(pady=30)
		self.register_user_btn.pack(pady=10)
		
		register_frame.pack()

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
						self.register_error_label = tk.Label(register_frame, text=str(server_error), font="helvetica 15", bg="#fff", foreground="red")
						self.register_error_label.pack(pady=10)
						
						self.main_view.schedule_label_clear(self.register_error_label, 5000)
						
						finger.clear_location(fingerprintId)
			except Exception as error:
				print("An error occured: ", error)
				self.exception_label = tk.Label(register_frame, text=str(error), font="helvetica 15", bg="#fff", foreground="red")
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


    
class VotePage(Page):
	def __init__(self, main_view, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.main_view = main_view
		
		# Create frames
		self.fingerprint_auth_frame = tk.Frame(self, height=660, width=1320, bg="#fff", bd=2, relief="solid")
		self.vote_options_container = tk.Frame(self)
		self.farewell_message_frame = tk.Frame(self, height=660, width=1320, bg="#fff", bd=2, relief="solid")
		
		self.fingerprint_auth_frame.pack_propagate(0)
		
		self.vote_cast_title_label = tk.Label(self, text="Cast your vote!", font="helvetica 20 bold")
		
		self.fingerprint_auth_result_string = tk.StringVar(value="")
		
		self.fingerprint_auth_success_label = tk.Label(self.fingerprint_auth_frame, text="Authenticated successfully!", font="helvetica 15", bg="#fff", foreground="green")
		self.fingerprint_auth_failure_label = tk.Label(self.fingerprint_auth_frame, text="Fingerprint not found after 3 attempts. Please contact the election manager!", font="helvetica 20", bg="#fff", foreground="red")


	def show_fingerprint_frame(self):
		# Clear existing components (if any)
		self.vote_options_container.pack_forget()
		self.farewell_message_frame.pack_forget()
		self.vote_cast_title_label.pack_forget()
		self.fingerprint_auth_failure_label.pack_forget()
		
		self.title_label = tk.Label(self.fingerprint_auth_frame, text="Fingerprint Authentication", font="helvetica 20 bold", bg="#fff")
		self.title_label.pack(pady=50)
		
		self.btn = tk.Button(self.fingerprint_auth_frame, text="Start Authentication", command=self.authenticate_fingerprint)
		self.btn.pack(pady=50)
		
		self.fingerprint_auth_frame.pack()


	def authenticate_fingerprint(self):
		self.instruction_label = tk.Label(self.fingerprint_auth_frame, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
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
				self.fingerprint_auth_error_label.pack(pady=20)
				
				self.main_view.schedule_label_clear(self.fingerprint_auth_error_label, 5000)		# Hide the label after 5 seconds

				self.update_idletasks()
			else:
				self.fingerprint_auth_error_label.pack_forget()		# Hide all error messages 
				self.fingerprint_auth_result = "failure"
				
		if self.fingerprint_auth_result == "success":
			self.fingerprint_auth_result_string.set("Fingerprint Authentication Successful")
			self.show_vote_options()
		else:
			self.fingerprint_auth_result_string.set("Fingerprint Authentication Failed")
			self.user_not_found()
			#self.show_vote_options()

	def show_vote_options(self):
		# Clear existing components (if any)
		self.title_label.pack_forget()
		self.btn.pack_forget()
		self.instruction_label.pack_forget()
		self.fingerprint_auth_failure_label.pack_forget()
		self.fingerprint_auth_frame.pack_forget()
		self.farewell_message_frame.pack_forget()
		
		#self.vote_cast_title_label = tk.Label(self, text="Cast your vote!", font="helvetica 20 bold")
		self.vote_cast_title_label.pack(pady=50)
		
		server_response = None
		try:
			server_response = requests.get("https://fingerprint-voter-server.onrender.com/candidate/all")
			if server_response.status_code == requests.codes.ok:
				candidates = server_response.json() or []
				
				#self.container = tk.Frame(self)
				rows_needed = self.determine_grid_rows_amount(len(candidates))
				print(rows_needed)
				
				self.vote_options_container.rowconfigure(rows_needed)
				self.vote_options_container.columnconfigure(3)
				self.vote_options_container.pack()
				
				myscrollbar = tk.Scrollbar(self.vote_options_container, orient="vertical", highlightbackground="black", highlightthickness=2)
				myscrollbar.grid(column=3, row=0, sticky='NS')
				
				r = 0
				c = 0
				for candidate in candidates:
					if c > 2:
						r += 1
						c = 0
						
					print(f'[{r}][{c}]: Result {candidate["id"]}: {candidate["name"]}')
					
					frame = tk.Frame(self.vote_options_container, borderwidth=1, background='white', highlightbackground="black", highlightthickness=2)
					candidate_name = tk.Label(frame, text=candidate["name"], font="helvetica 20 bold", background='white')
					candidate_name.pack(pady=25, padx=25)
					
					vote_btn = tk.Button(frame, text="Vote", font="helvetica 14", command= lambda candidate=candidate: self.handle_vote_confirmation(candidate))
					vote_btn.pack(pady=25)
					
					frame.grid(row=r, column=c, columnspan=1, padx=150, pady=80)
					c += 1
			else:
				server_error = server_response.json()["error"]
				if server_error != "":
					print("An error occured: ", server_error)
		except Exception as error:
			print("An error occured: ", error)
				
        
	def user_not_found(self):
		# Clear existing components
		self.title_label.pack_forget()
		self.instruction_label.pack_forget()
		self.btn.pack_forget()
        
		# Show failure
		self.fingerprint_auth_failure_label.pack(side="top", fill="both", expand=True)	# Show failure label

	def cast_vote(self, candidate):
		try:
			token = get_jwt_token()
	
			decoded_token = jwt.decode(token, options={"verify_signature": False}, algorithms=[])
			print(decoded_token)
			user_id = decoded_token.get("userId")
		except Exception as error:
			print("An error occured: ", error)
			
		if user_id:
			payload = {"userId": user_id, "candidateId": candidate["id"]}
			header = {'Authorization': f'Bearer {token}'}
			
			server_response = None
			try:
				server_response = requests.patch("https://fingerprint-voter-server.onrender.com/user/vote", data=payload, headers=header)
				if server_response.status_code == requests.codes.ok:
					self.farewell_message()
					
					self.logout_user(header)
					self.logout_label = tk.Label(self.farewell_message_frame, text="You have been logged out from the system.", font="helvetica 15", bg="#fff", foreground="green")
					self.logout_label.pack()
					self.logout_label.place(relx=0.5, rely=0.8, anchor="center")
					
					self.after(3000, lambda: self.main_view.show_login_page())
					
					self.vote_cast_title_label.pack_forget()
				else:
					server_error = server_response.json()["error"]
					if server_error != "":
						print("An error occured: ", server_error)
			except Exception as error:
				print("An error occured: ", error)

	def logout_user(self, header):
		server_response = None
		try:
			server_response = requests.post("https://fingerprint-voter-server.onrender.com/logout", headers=header)
			if server_response.status_code == requests.codes.ok:
				try:
					kr.delete_password("fp-voter", "jwt_token")
				except Exception as error:
					print("An error occured: ", server_error)
			else:
				server_error = server_response.json()["error"]
				if server_error != "":
					print("An error occured: ", server_error)
		except Exception as error:
			print("An error occured: ", error)

	def farewell_message(self):
		# Clear existing components
		self.vote_cast_title_label.pack_forget()
		self.instruction_label.pack_forget()
		self.vote_options_container.pack_forget()
		
		self.farewell_message_frame.pack_propagate(0)
		
		self.farewell_msg_label = tk.Label(self.farewell_message_frame, text="Thank you for voting!", font="helvetica 20 bold", bg="#fff")
		self.farewell_msg_label.pack(pady=50)
		self.farewell_msg_label.place(relx=0.5, rely=0.5, anchor="center")
		
		self.farewell_message_frame.pack()
	
	def determine_grid_rows_amount(self, length):
		rows = int(length / 3)
		if length % 3 == 0:
			return rows
		return rows + 1
	
	def handle_vote_confirmation(self, candidate):
		confirmation =  tkinter.messagebox.askokcancel("Confirm your vote", "Are you sure you want to vote for candidate " + candidate["name"] + "?")
		
		if confirmation:
			self.cast_vote(candidate)

class LoginPage(Page):
	def __init__(self, main_view, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		self.main_view = main_view  # Store a reference to the MainView instance
		
		# Create a login frame
		self.login_frame = tk.Frame(self, height=660, width=1320, bg="#fff", bd=2, relief="solid")
		self.login_frame.pack_propagate(0)
		
		self.title_label = tk.Label(self.login_frame, text="Login", font="helvetica 20 bold", bg="#fff")
		self.title_label.pack(pady=50)
		
		self.username_label = tk.Label(self.login_frame, bg="#fff", text="Username")
		self.username_input = tk.Entry(self.login_frame, width=20, bg="#fff", bd=1, relief="solid")
		self.password_label = tk.Label(self.login_frame, bg="#fff", text="Password")
		self.password_input = tk.Entry(self.login_frame, show="*", width=20, bg="#fff", bd=1, relief="solid")
		
		self.submit_credentials_btn = tk.Button(self.login_frame, text="Submit", height=1, width=8, cursor="hand2", command=lambda: self.attempt_login(self.username_input.get(), self.password_input.get()))
		self.register_user_btn = tk.Button(self.login_frame, text="Don't have an account? Click here to register.", font="helvetica 12 underline", relief=tk.FLAT, cursor="hand2",  borderwidth=0, highlightthickness=0, bg="#fff", activebackground="#fff", command=lambda: self.main_view.show_register_page())
		
		self.login_success_label = tk.Label(self.login_frame, text="Logged in successfully!", font="helvetica 15", bg="#fff", foreground="green")

		self.username_label.pack(pady=10)
		self.username_input.pack(pady=5)
		self.password_label.pack(pady=10)
		self.password_input.pack(pady=5)
		self.submit_credentials_btn.pack(pady=30)
		self.register_user_btn.pack(pady=10)
		
		self.login_frame.pack()
		
		
	def attempt_login(self, username, password):
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
				print("vote page shown")
			else:
				server_error = server_response.json()["error"]
				if server_error != "":
					print("An error occured: ", server_error)
					self.login_error_label = tk.Label(self.login_frame, text=str(server_error), font="helvetica 15", bg="#fff", foreground="red")
					self.login_error_label.pack(pady=10)
					
					self.main_view.schedule_label_clear(self.login_error_label, 5000)	# Hide the label after 5 seconds
		except Exception as error:
			print("An error occured: ", error)
			self.exception_label = tk.Label(self.login_frame, text=str(error), font="helvetica 15", bg="#fff", foreground="red")
			self.exception_label.pack(pady=10)
					
			self.main_view.schedule_label_clear(self.exception_label, 5000)
        
class GreetingPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Welcome to the fingerprint voter!\nNavigate to different pages with the buttons at the top of the page.")
        label.pack(side="top", fill="both", expand=True)
