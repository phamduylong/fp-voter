import tkinter as tk 
import sensor_functions as finger
import alert
class Page(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
	def show(self):
		self.lift()

class Page1(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		label = tk.Label(self, text="This is page 1")
		label.pack(side="top", fill="both", expand=True)

class Page2(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)

		title_label = tk.Label(self, text="Fingerprint Authentication", font="helvetica 20 bold", bg="#fff")
		title_label.pack(side="top", fill="both", expand=True)

		fingerprint_auth_result_string = tk.StringVar(value="")
		fingerprint_auth_result_message = tk.Label(self, textvariable=fingerprint_auth_result_string, justify="center", bg="#fff", font="helvetica 15")

		instruction_label = tk.Label(self, text="Place your finger on the scanner...", font="helvetica 15", bg="#fff")
		instruction_label.pack(side="top", fill="both", expand=True)
		
		btn = tk.Button(self, text="Search", command=lambda: finger.search_location(1))
		btn.pack(side="top", fill="both", expand=True)

class Page3(Page):
	def __init__(self, *args, **kwargs):
		Page.__init__(self, *args, **kwargs)
		label = tk.Label(self, text="This is page 3")
		label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		p1 = Page1(self)
		p2 = Page2(self)
		p3 = Page3(self)

		buttonframe = tk.Frame(self)
		container = tk.Frame(self)
		buttonframe.pack(side="top", fill="x", expand=False)
		container.pack(side="top", fill="both", expand=True)

		p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
		p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		b1 = tk.Button(buttonframe, text="Page 1", command=p1.show)
		b2 = tk.Button(buttonframe, text="Page 2", command=p2.show)
		b3 = tk.Button(buttonframe, text="Page 3", command=p3.show)

		b1.pack(side="left")
		b2.pack(side="left")
		b3.pack(side="left")

		p1.show()
root = tk.Tk()
main = MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("400x400")
root.mainloop()
