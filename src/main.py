import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from cryptography.fernet import Fernet

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Cryptor Decryptor')
        self.root.resizable(False, False)
        self.root.geometry('900x450')
        
        self.file_path = None

        self.show_widgets()

    def show_widgets(self):
        input_label = ttk.Label(self.root, text="Input:")
        input_label.pack()

        self.input_text_field = tk.Text(self.root, width=30, height=7)
        self.input_text_field.pack()

        output_label = ttk.Label(self.root, text="Output:")
        output_label.place(relx=0.47, rely=0.41)

        self.output_text_field = tk.Text(self.root, width=30, height=7)
        self.output_text_field.place(relx=0.36, rely=0.45)
        
        self.key_field = tk.Text(self.root, width=15, height=0.5)
        self.key_field.place(relx=0.75, rely=0.37)
        
        self.decrypt_key_label = ttk.Label(self.root, text="Key for decrypt:")
        self.decrypt_key_label.place(relx=0.75, rely=0.32)
        
        self.decrypt_key_label = ttk.Label(self.root, text="Your generated key:")
        self.decrypt_key_label.place(relx=0.09, rely=0.32)

        self.generated_key_field = tk.Text(self.root, width=15, height=0.5)
        self.generated_key_field.place(relx=0.09, rely=0.37)

        open_file_button = ttk.Button(
            master=self.root,
            text='Open a File',
            command=self.open_file,
            width=25
        )
        
        start_crypt_button = ttk.Button(
            master=self.root,
            text='Crypt',
            command=self.encrypt,
            width=20
        )

        start_decrypt_button = ttk.Button(
            master=self.root,
            text='Decrypt',
            command=self.decrypt,
            width=20
        )
        
        start_crypt_button.place(relx=0.35, rely=0.32)
        start_decrypt_button.place(relx=0.50, rely=0.32)
        open_file_button.place(relx=0.01)
        
    def message(self, message_text, type):
        color = None
        
        if type == "error":
            color = "red"
        if type == "info":
            color = "gray"
        if type == "success":
            color = "green"
            
        msg = ttk.Label(self.root, text=message_text, foreground=color, font=("Arial", 16))
        msg.place(relx=0.39, rely=0.9)
        self.root.after(5000, msg.destroy)

    def open_file(self):
        self.file_path = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes = (
                ('Text files', '*.txt'),
                ('All files', '*.*')
            )
        )
        
        if self.file_path:
            self.input_text_field.delete(1.0, tk.END)
            self.message("File sucessfully loaded", "success")
            
            self.input_text_field.insert(tk.END, self.read_file())
        else:
            self.message("Failed to load file", "error")
            
    def read_file(self):
        if not self.file_path:
            return ''
        with open(self.file_path, 'r') as file:
            return file.read()

    def encrypt(self):
        input_text = self.input_text_field.get("1.0", "end-1c")
        
        if input_text:
            try:
                self.key = Fernet.generate_key()
                self.cipher_encrypt = Fernet(self.key)
                
                encrypted_text = self.cipher_encrypt.encrypt(input_text.encode())
                self.message("Encryption successfull", "success")
            except Exception:
                self.message("Encryption error", "error")
                
            self.generated_key_field.insert(tk.END, self.key)            
            
            self.output_text_field.delete(1.0, tk.END)
            self.output_text_field.insert(tk.END, encrypted_text.decode())
        else:
            self.message("Input field is empty", "error")

    def decrypt(self):
        input_text = self.input_text_field.get("1.0", "end-1c")
        user_key = self.key_field.get("1.0", "end-1c")
        
        cipher_decrypt = Fernet(user_key)

        if input_text:
            try:
                decrypted_text = cipher_decrypt.decrypt(input_text.encode())
                self.message("Decryption successful", "success")
            except Exception:
                self.message("Incorrect key", "error")
                
            self.output_text_field.delete(1.0, tk.END)
            self.output_text_field.insert(tk.END, decrypted_text.decode())
        else:
            self.message("Input field is empty", "error")
        
        
if __name__ == "__main__":
    app = App()
    app.root.mainloop()
