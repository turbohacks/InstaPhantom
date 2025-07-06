# InstaPhantom – Instagram Info Finder (Modern GUI White Theme)
# Requires: pip install instagrapi

from instagrapi import Client
from tkinter import *
from tkinter import messagebox, scrolledtext
import threading

client = Client()

# GUI Setup
root = Tk()
root.title("InstaPhantom")
root.geometry("760x650")
root.configure(bg="white")

# Header
header = Label(root, text="InstaPhantom", bg="white", fg="#e1306c", font=("Segoe UI Semibold", 22))
header.pack(pady=15)

# Username Section
frame_input = Frame(root, bg="white")
Label(frame_input, text="Instagram Username:", bg="white", fg="black", font=("Segoe UI", 12)).grid(row=0, column=0, sticky=W, padx=5, pady=5)
username_entry = Entry(frame_input, width=32, font=("Segoe UI", 12), bd=2, relief=GROOVE)
username_entry.grid(row=0, column=1, padx=10, pady=5)
frame_input.pack(pady=5)

# Login Section
frame_login = Frame(root, bg="white")
Label(frame_login, text="Your Instagram Login:", bg="white", fg="black", font=("Segoe UI", 12)).grid(row=0, column=0, sticky=W, padx=5, pady=5)
login_user = Entry(frame_login, width=32, font=("Segoe UI", 12), bd=2, relief=GROOVE)
login_user.grid(row=0, column=1, padx=10, pady=5)

login_pass = Entry(frame_login, width=32, font=("Segoe UI", 12), show="*", bd=2, relief=GROOVE)
login_pass.grid(row=1, column=1, padx=10, pady=5)
Label(frame_login, text="Password:", bg="white", fg="black", font=("Segoe UI", 12)).grid(row=1, column=0, sticky=W, padx=5, pady=5)
frame_login.pack(pady=5)

# Output Box
output_box = scrolledtext.ScrolledText(root, width=85, height=20, bg="#f7f7f7", fg="black", font=("Consolas", 10), bd=2, relief=SOLID)
output_box.pack(pady=15)

last_report = ""

def export_report():
    global last_report
    if not last_report.strip():
        messagebox.showwarning("Nothing to export", "Run a search first.")
        return
    filename = f"insta_{username_entry.get().strip()}_report.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(last_report)
    messagebox.showinfo("Exported", f"Saved as {filename}")

def get_info():
    global last_report
    username = username_entry.get().strip()
    login = login_user.get().strip()
    passwd = login_pass.get().strip()

    if not username or not login or not passwd:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    output_box.delete(1.0, END)
    output_box.insert(END, "[*] Logging in...\n")

    def run():
        global last_report
        try:
            client.login(login, passwd)
            output_box.insert(END, "[✓] Logged in successfully!\n")
        except Exception as e:
            output_box.insert(END, f"[X] Login failed: {e}\n")
            return

        try:
            user = client.user_info_by_username(username)
            result = (
                f"\n[✓] Profile Found: https://instagram.com/{username}\n"
                f"Full Name: {user.full_name}\n"
                f"Username: {user.username}\n"
                f"Bio: {user.biography}\n"
                f"Followers: {user.follower_count}\n"
                f"Following: {user.following_count}\n"
                f"Total Posts: {user.media_count}\n"
                f"Is Verified: {user.is_verified}\n"
                f"Is Private: {user.is_private}\n"
                f"Business Account: {user.is_business}\n"
                f"Profile Picture: {user.profile_pic_url}\n"
            )
            output_box.insert(END, result)
            last_report = result
        except Exception as e:
            output_box.insert(END, f"[X] Failed to fetch data: {e}\n")

    threading.Thread(target=run).start()

# Buttons
button_frame = Frame(root, bg="white")
Button(button_frame, text="Start Info Gathering", command=get_info, bg="#e1306c", fg="white", font=("Segoe UI", 11), width=20).grid(row=0, column=0, padx=10)
Button(button_frame, text="Export to .txt", command=export_report, bg="#555", fg="white", font=("Segoe UI", 11), width=20).grid(row=0, column=1, padx=10)
button_frame.pack(pady=5)

root.mainloop()
