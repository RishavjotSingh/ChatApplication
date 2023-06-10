import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 8000

# Color scheme
PRIMARY_COLOR = "#1F1F1F"        # Dark gray
SECONDARY_COLOR = "#FFFFFF"      # White
ACCENT_COLOR = "#FF0000"         # Red
TEXT_COLOR = "#FFFFFF"           # White
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def display_message(sender, message):
    frame = tk.LabelFrame(messages_frame, text=sender, font=SMALL_FONT, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, padx=10, pady=5)
    frame.pack(fill=tk.X, padx=5, pady=5)
    label = tk.Label(frame, text=message, font=SMALL_FONT, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR)
    label.pack(anchor=tk.W)
    messages_frame.update_idletasks()  # Update the frame to reflect the changes

    # Adjust the canvas scroll region to include the new message
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Scroll to the bottom of the canvas
    canvas.yview_moveto(1.0)

def communicate_to_server():
    # as a client, choose new username
    username = username_input.get()

    if not username.strip().isspace():
        client_socket.sendall(username.encode())
    else:
        messagebox.showerror('Invalid username', 'Username cannot be blank')

    threading.Thread(target=receive_messages, args=()).start()

def connect_to_server():
    try:
        client_socket.connect((HOST, PORT))
        display_message("[SERVER]", "Connected to the server")
    except:
        messagebox.showerror('Unable to connect to the server', f'Something went wrong while connecting to the server {HOST} {PORT}')

    communicate_to_server()

    username_input.config(state=tk.DISABLED)
    join_button.config(state=tk.DISABLED)

def send_message():
    message = message_input.get()

    if not message.strip().isspace():
        client_socket.sendall(message.encode())
        message_input.delete(0, len(message))
    else:
        messagebox.showerror('Blank message', 'Blank message cannot be sent')

# Dimensions for the window
window_width = 600
window_height = 600

# Setting up the window
root = tk.Tk()
root.geometry(f"{window_width}x{window_height}")
root.title("Chat Application")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_region = tk.Frame(root, width=window_width, height=window_height/6, bg=PRIMARY_COLOR)
top_region.grid(row=0, column=0, sticky=tk.NSEW)

middle_region = tk.Frame(root, width=window_width, height=window_height*4/6, bg=PRIMARY_COLOR)
middle_region.grid(row=1, column=0, sticky=tk.NSEW)

bottom_region = tk.Frame(root, width=window_width, height=window_height/6, bg=PRIMARY_COLOR)
bottom_region.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_region, text="Enter username here:", font=FONT, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR)
username_label.pack(side=tk.LEFT, padx=10)

username_input = tk.Entry(top_region, width=(int)(window_width/30), font=FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR)
username_input.pack(side=tk.LEFT)

join_button = tk.Button(top_region, text="Join", font=BUTTON_FONT, bg=ACCENT_COLOR, fg=SECONDARY_COLOR, command=connect_to_server)
join_button.pack(side=tk.LEFT, padx=15)

message_input = tk.Entry(bottom_region, font=FONT, bg=SECONDARY_COLOR, fg=PRIMARY_COLOR, width=38)
message_input.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(bottom_region, text="Send", font=BUTTON_FONT, bg=ACCENT_COLOR, fg=SECONDARY_COLOR, command=send_message)
send_button.pack(side=tk.LEFT, padx=10)

canvas = tk.Canvas(middle_region, bg=PRIMARY_COLOR, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(middle_region, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

messages_frame = tk.Frame(canvas, bg=PRIMARY_COLOR)
messages_frame.pack(fill=tk.BOTH, padx=5, pady=5)

canvas.create_window((0, 0), window=messages_frame, anchor=tk.NW)

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", on_canvas_configure)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)

def receive_messages():
    while True:
        full_message = client_socket.recv(2048).decode('utf-8')
        if not full_message.strip().isspace():
            username = full_message.split("~")[0]
            message = full_message.split("~")[1]
            display_message(f"[{username}]", message)
        else:
            messagebox.showerror('Error', 'A blank message received from the server')

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
