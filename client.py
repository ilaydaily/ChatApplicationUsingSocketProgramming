import threading
import socket
import tkinter as tk
from tkinter import messagebox

import customtkinter

HOST = '10.33.14.21'
PORT = 1234

WHITE = "#FFFFFF"
MAIN_DARK = "#FF6F00"  # Turuncu
MAIN_MEDIUM = "#32CD32"  # Yeşil
MAIN_LIGHT = "#D4ADFC"
BUBBLE_COLOR = "#D4ADFC"  # Mor
BG_COLOR = "#2E2E2E"  # Temaya uygun koyu arka plan

FONT_MAIN = ("Poppins", 17)
FONT_SMALL = ("Poppins", 12)
FONT_BUTTON = ("Poppins", 14)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    if new_appearance_mode == "Dark":
        textbox.configure(bg="#2E2E2E")  # Koyu arka plan
    else:
        textbox.configure(bg=WHITE)  # Açık arka plan

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message, align="left"):
    textbox.configure(state=tk.NORMAL)
    textbox.insert(tk.END, '\n')  # Bir satır boşluk ekle
    if align == "right":
        bubble = tk.Label(textbox, text=message, bg=BUBBLE_COLOR, fg="black", padx=10, pady=5, wraplength=400, justify=tk.RIGHT)
        bubble.pack(anchor='e', padx=5, pady=2)
    else:
        bubble = tk.Label(textbox, text=message, bg=BUBBLE_COLOR, fg="black", padx=10, pady=5, wraplength=400, justify=tk.LEFT)
        bubble.pack(anchor='w', padx=5, pady=2)
    textbox.configure(state=tk.DISABLED)
    textbox.yview(tk.END)  # Otomatik olarak en sona kaydır

my_username = ""

def connect():
    global my_username
    try:
        client.connect((HOST, PORT))
        print("Connected to the server!")
        add_message("[SERVER] Connected to the server successfully!")
    except:
        messagebox.showerror("Can not connect to the server", f"Unable to connect to server {HOST}:{PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        my_username = username
        login_window.destroy()
        root.deiconify()
    else:
        messagebox.showerror("Error", "Please enter a username!")

    threading.Thread(target=listen_server, args=()).start()

def listen_server():
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split('!')[0]
            text = message.split('!')[1]
            if username != my_username:
                add_message(f"[{username}]: {text}")
        else:
            messagebox.showerror("Error", "Empty message!")

def send_message(event=None):
    message = entry.get()
    if message != "":
        client.sendall(message.encode())
        entry.delete(0, len(message))
        add_message(f"{message}", align="right")
    else:
        messagebox.showerror("Message can't be empty", "Write something into the chatbox to send it!")

def exit_socket():
    client.close()
    root.quit()

root = customtkinter.CTk()
root.title("Client")
root.geometry(f"{1100}x{580}")
root.withdraw()  # Ana pencereyi başlangıçta gizle

# configure grid layout (4x4)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

entry = customtkinter.CTkEntry(root, placeholder_text="Write message")
entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
entry.bind("<Return>", send_message)  # Bind the Enter key to send_message function

main_button_1 = customtkinter.CTkButton(master=root, command=send_message, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send")
main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

textbox = tk.Text(root, wrap='word', state=tk.DISABLED, bg=BG_COLOR, fg="white")
textbox.grid(row=0, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

# Create login window
login_window = customtkinter.CTkToplevel()
login_window.title("Login")
login_window.geometry("300x200")

login_label = customtkinter.CTkLabel(login_window, text="Enter Username", font=customtkinter.CTkFont(size=20, weight="bold"))
login_label.pack(pady=(20, 10))

username_textbox = customtkinter.CTkEntry(login_window, width=200)
username_textbox.pack(pady=(10, 10))

login_button = customtkinter.CTkButton(login_window, text="Enter Chat", command=connect)
login_button.pack(pady=(10, 10))

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(login_window, values=["Light", "Dark", "System"],
                                                          command=change_appearance_mode_event)
appearance_mode_optionemenu.pack(pady=(10, 10))

scaling_optionemenu = customtkinter.CTkOptionMenu(login_window, values=["80%", "90%", "100%", "110%", "120%"],
                                                  command=change_scaling_event)
scaling_optionemenu.pack(pady=(10, 20))

appearance_mode_optionemenu.set("Dark")
scaling_optionemenu.set("100%")

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
