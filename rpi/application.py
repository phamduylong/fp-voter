import tkinter as tk
import page as page


def exit_application():
    root.destroy()


root = tk.Tk()
main = page.MainView(root)
main.pack(side="top", fill="both", expand=True)
root.wm_geometry("400x400")
root.mainloop()