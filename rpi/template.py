import tkinter as tk
import tkinter.messagebox

import requests
root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("Fingerprint Application")

def determine_grid_rows_amount(length):
    rows = int(length / 3)
    if length % 3 == 0:
        return rows
    return rows + 1

def confirm_user_choice(name):
    return tkinter.messagebox.askokcancel("Confirm your vote", "Are you sure you want to vote for candidate " + name)


server_response = None
try:
    server_response = requests.get("https://fingerprint-voter-server.onrender.com/candidate/all")
    if server_response.status_code == requests.codes.ok:
        candidates = server_response.json() or []
        container = tk.Frame(root, )
        rows_needed = determine_grid_rows_amount(len(candidates))
        print(rows_needed)
        container.rowconfigure(rows_needed)
        container.columnconfigure(3)
        container.pack()
        myscrollbar = tk.Scrollbar(container, orient="vertical", highlightbackground="black", highlightthickness=2 )
        myscrollbar.grid(column=3, row=0, sticky='NS')
        r = 0
        c = 0
        for candidate in candidates:
            if c > 2:
                r += 1
                c = 0

            print(f'[{r}][{c}]: Result {candidate["id"]}: {candidate["name"]}')
            frame = tk.Frame(container, borderwidth=1, background='white', highlightbackground="black", highlightthickness=2)
            candidate_name = tk.Label(frame, text=candidate["name"], font="helvetica 20 bold", background='white').pack(pady=25, padx=25)
            vote_btn = tk.Button(frame, text="Vote", font="helvetica 14", command= lambda : confirm_user_choice(candidate["name"])).pack(pady=25)
            frame.grid(row=r, column=c, columnspan=1, padx=150, pady=80)
            c += 1


    else:
        server_error = server_response.json()["error"]
        if server_error != "":
            print("An error occured: ", server_error)
except Exception as error:
    print("An error occured: ", error)
root.mainloop()


