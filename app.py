import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import random
import string

# Function to generate a random password
'''Total Combinations=(Number of possible characters) ^ (Password length)
For the ASCII character set: Total Combinations = 128^6 = 4,398,046,511,104 (4.3 trillion)

Slow Attack (100,000 passwords per second): Approximately 509 days
Moderate Attack (1,000,000 passwords per second): Approximately 51 days
Fast Attack (1,000,000,000 passwords per second): Approximately 1.2 hours
'''
def generate_password(length=30):
    # Define the set of characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate the password
    password = "".join(random.choice(characters) for _ in range(length))
    return password

# Function to handle the UI action of generating a password
def generate_password_ui():
    try:
        length = int(password_length_entry.get())
        # Validate password length
        if length < 6:
            messagebox.showerror("Error", "Password length must be at least 6")
            return
        if length > 20:
            messagebox.showerror("Error", "Password length must not exceed 20")
            return
        # Generate the password and display it in the password entry
        generated_password = generate_password(length)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generated_password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length")

# Function to encrypt the password
def encrypt_password():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Password is required")
        return
    # Encrypt the password and display it in the encrypted entry
    encrypted_password = cipher.encrypt(password.encode()).decode()
    encrypted_entry.delete(0, tk.END)
    encrypted_entry.insert(0, encrypted_password)

''' Slow Scenario (10 passwords per second): Approximately 13,944 years
Moderate Scenario (100 passwords per second): Approximately 1,394 years
Fast Scenario (1,000 passwords per second): Approximately 139 years
Adding Fernet encryption dramatically increases the time required to crack the password,
making it significantly more secure against brute-force attacks.'''
# Function to decrypt the password
def decrypt_password():
    encrypted_password = encrypted_entry.get()
    if not encrypted_password:
        messagebox.showerror("Error", "Encrypted password is required")
        return
    try:
        # Decrypt the password and display it in the decrypted entry
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        decrypted_entry.delete(0, tk.END)
        decrypted_entry.insert(0, decrypted_password)
    except Exception:
        messagebox.showerror("Error", "Invalid encrypted password")

# Generate a key and instantiate a Fernet instance for encryption/decryption
key = Fernet.generate_key()      #A unique encryption key is generated using Fernet.generate_key().
cipher = Fernet(key)            #This key is used to create a Fernet instance, cipher, which handles the encryption and decryption operations.

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Password Generator and Encryption/Decryption")
root.geometry("600x300")

# Use ttk for better styling
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#007BFF", foreground="#000000",
                font=("Helvetica", 10))
style.configure("TLabel", font=("Helvetica", 10))
style.configure("TEntry", font=("Helvetica", 10))

# Create a frame for padding and place it in the root window
frame = ttk.Frame(root, padding="20 20 20 20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Make the frame stretchable
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Label and entry for password length
ttk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky=tk.E, pady=5)
password_length_entry = ttk.Entry(frame)
password_length_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

# Button to generate the password
generate_button = ttk.Button(frame, text="Generate Password", command=generate_password_ui)
generate_button.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)

# Label and entry to display the generated password
ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.E, pady=5)
password_entry = ttk.Entry(frame)
password_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)

# Button to encrypt the password
encrypt_button = ttk.Button(frame, text="Encrypt", command=encrypt_password)
encrypt_button.grid(row=1, column=3, sticky=tk.W, pady=5, padx=5)

# Label and entry to display the encrypted password
ttk.Label(frame, text="Encrypted Password:").grid(row=2, column=0, sticky=tk.E, pady=5)
encrypted_entry = ttk.Entry(frame)
encrypted_entry.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5)

# Label and entry to display the decrypted password
ttk.Label(frame, text="Decrypted Password:").grid(row=3, column=0, sticky=tk.E, pady=5)
decrypted_entry = ttk.Entry(frame)
decrypted_entry.grid(row=3, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5)

# Button to decrypt the password
decrypt_button = ttk.Button(frame, text="Decrypt", command=decrypt_password)
decrypt_button.grid(row=4, column=1, columnspan=3, sticky=tk.W, pady=5, padx=5)

# Make the entries stretchable
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)

# Start the Tkinter event loop
root.mainloop()
