import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import socks
import socket
import tkinter as tk
from tkinter import messagebox, font, filedialog, ttk
import threading
import time
import uuid
import random

IMAGE_PATH = None

def set_tor_proxy():
    try:
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
        socket.socket = socks.socksocket
        with socket.create_connection(("127.0.0.1", 9050), timeout=5):
            print("Tor is active and connected to port 9050.")
            return True
    except Exception as e:
        print(f"Tor connection error: {e}")
        return False


EMAIL_ADDRESS = "Roey1234r@gmail.com"
EMAIL_PASSWORD = "jyql zvhs uxnd rlqj"

stop_sending = False
email_count = 0

def select_image():
    global IMAGE_PATH
    IMAGE_PATH = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if IMAGE_PATH:
        lbl_image_status.config(text=f"Image Attached: {IMAGE_PATH.split('/')[-1]}")

def send_emails():
    global stop_sending, email_count, IMAGE_PATH
    to_email = entry_recipient.get()
    cc_email = entry_cc.get()
    bcc_email = entry_bcc.get()
    subject = entry_subject.get()
    body = text_body.get("1.0", tk.END)
    
    if not to_email or not subject or not body.strip():
        messagebox.showwarning("Error", "All fields must be filled.")
        return

    stop_sending = False
    email_count = 0
    progress_bar["value"] = 0
    progress_bar["maximum"] = 100

    use_tor = set_tor_proxy()
    if not use_tor:
        messagebox.showinfo("Notice", "Tor is not active. The email will be sent directly.")
        socks.set_default_proxy()

    def send_loop():
        global email_count
        while not stop_sending:
            try:
                msg = MIMEMultipart()
                unique_subject = f"{subject} - {random.randint(1000, 9999)}"
                msg["Subject"] = unique_subject
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = to_email
                msg["Cc"] = cc_email
                msg["Message-ID"] = f"<{uuid.uuid4()}@example.com>"
                
                msg.attach(MIMEText(body, "plain"))

                if IMAGE_PATH:
                    with open(IMAGE_PATH, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header('Content-Disposition', 'attachment', filename=IMAGE_PATH.split('/')[-1])
                        msg.attach(img)
                
                recipients = [to_email] + cc_email.split(",") + bcc_email.split(",")

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
                    email_count += 1
                    lbl_status.config(text=f"Emails Sent: {email_count}")
                    progress_bar["value"] = (email_count % 100)
                time.sleep(0.5)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {e}")
                break

    threading.Thread(target=send_loop).start()

def stop_sending_emails():
    global stop_sending
    stop_sending = True

# יצירת חלון ראשי בעיצוב שחור-אפור עם פינות מעוגלות ופונט מודרני
root = tk.Tk()
root.title("Dark Mode Email Sender")
root.geometry("700x850")
root.configure(bg="#1C1C1E")

# פונטים מודרניים בסגנון Apple
title_font = font.Font(family="Helvetica Neue", size=24, weight="bold")
label_font = font.Font(family="Helvetica Neue", size=12)
button_font = font.Font(family="Helvetica Neue", size=14, weight="bold")

# כותרת מעוצבת
lbl_title = tk.Label(root, text="Email Sender", bg="#1C1C1E", font=title_font, fg="#FFFFFF")
lbl_title.pack(pady=15)

# הגדרת מסגרות בצבעים כהים עם פינות מעוגלות והצללות עדינות
def create_frame(bg_color):
    frame = tk.Frame(root, bg=bg_color, padx=20, pady=15)
    frame.pack(pady=10, padx=15, fill="x", ipadx=10, ipady=5)
    frame.config(highlightbackground="#3A3A3C", highlightthickness=1, bd=1, relief="flat")
    return frame

recipient_frame = create_frame("#2C2C2E")
message_frame = create_frame("#3A3A3C")

def create_label_entry(parent, label_text, placeholder, bg_color):
    lbl = tk.Label(parent, text=label_text, bg=bg_color, fg="#FFFFFF", font=label_font)
    lbl.pack(anchor="w", padx=5)
    entry = tk.Entry(parent, font=label_font, bg="#48484A", fg="#FFFFFF", width=40, relief="flat", insertbackground="white")
    entry.insert(0, placeholder)
    entry.pack(fill="x", padx=5, pady=5)
    entry.config(highlightbackground="#3A3A3C", highlightthickness=1)
    return entry

entry_recipient = create_label_entry(recipient_frame, "To:", "Enter recipient email", "#2C2C2E")
entry_cc = create_label_entry(recipient_frame, "CC:", "Enter CC emails", "#2C2C2E")
entry_bcc = create_label_entry(recipient_frame, "BCC:", "Enter BCC emails", "#2C2C2E")

lbl_subject = tk.Label(message_frame, text="Subject:", bg="#3A3A3C", fg="#FFFFFF", font=label_font)
lbl_subject.pack(anchor="w", padx=5)
entry_subject = tk.Entry(message_frame, font=label_font, bg="#48484A", fg="#FFFFFF", relief="flat", width=40, insertbackground="white")
entry_subject.insert(0, "Enter subject")
entry_subject.pack(fill="x", padx=5, pady=5)
entry_subject.config(highlightbackground="#3A3A3C", highlightthickness=1)

lbl_body = tk.Label(message_frame, text="Message:", bg="#3A3A3C", fg="#FFFFFF", font=label_font)
lbl_body.pack(anchor="w", padx=5)
text_body = tk.Text(message_frame, wrap="word", font=label_font, height=8, bg="#48484A", fg="#FFFFFF", relief="flat", insertbackground="white")
text_body.insert("1.0", "Type your message here...")
text_body.pack(fill="x", padx=5, pady=5)
text_body.config(highlightbackground="#3A3A3C", highlightthickness=1)

attachment_frame = tk.Frame(root, bg="#1C1C1E")
attachment_frame.pack(pady=10)

lbl_image_status = tk.Label(attachment_frame, text="No Image Attached", bg="#1C1C1E", font=label_font, fg="#8E8E93")
lbl_image_status.pack(side="left", padx=10)

btn_image = tk.Button(attachment_frame, text="Attach Image", command=select_image, bg="#FF9500", fg="#FFFFFF", font=button_font, width=12, relief="flat")
btn_image.pack(side="right", padx=10)

lbl_status = tk.Label(root, text="Emails Sent: 0", bg="#1C1C1E", font=label_font, fg="#8E8E93")
lbl_status.pack(pady=15)

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", thickness=10, troughcolor="#3A3A3C", background="#32D74B")

progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=10)

button_frame = tk.Frame(root, bg="#1C1C1E")
button_frame.pack(pady=20)

btn_send = tk.Button(button_frame, text="Send Email", command=send_emails, bg="#007AFF", fg="#FFFFFF", font=button_font, width=15, relief="flat")
btn_send.grid(row=0, column=0, padx=20)

btn_stop = tk.Button(button_frame, text="Stop Sending", command=stop_sending_emails, bg="#FF3B30", fg="#FFFFFF", font=button_font, width=15, relief="flat")
btn_stop.grid(row=0, column=1, padx=20)

root.mainloop()
