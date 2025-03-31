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
        
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
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
            
            self.label_file_sucessfully_loaded = ttk.Label(self.root, text="File sucessfully loaded", foreground="green", font=("Arial", 16))
            self.label_file_sucessfully_loaded.place(relx=0.39, rely=0.9)

            self.input_text_field.insert(tk.END, self.read_file())
        else:
            self.label_file_sucessfully_loaded = ttk.Label(self.root, text="Failed to load file", foreground="red", font=("Arial", 16))
            self.label_file_sucessfully_loaded.place(relx=0.39, rely=0.9)
            
        self.root.after(5000, self.label_file_sucessfully_loaded.destroy)
                    
    def read_file(self):
        if not self.file_path:
            return ''
        with open(self.file_path, 'r') as file:
            return file.read()

    def encrypt(self):
        text = self.input_text_field.get("1.0", "end-1c")
        
        if text:
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)
            
            encrypted_text = self.cipher.encrypt(text.encode())
            
            with open("key.txt", "wb") as key_file:
                key_file.write(self.key)
            
            self.output_text_field.delete(1.0, tk.END)
            self.output_text_field.insert(tk.END, encrypted_text.decode())

    def decrypt(self):
        text = self.input_text_field.get("1.0", "end-1c")
        
        user_key = self.key_field.get("1.0", "end-1c")
        str_key = self.key.decode('utf-8')

        if text:
            if str_key == user_key:
                try:
                    decrypted_text = self.cipher.decrypt(text.encode())
                    
                    self.output_text_field.delete(1.0, tk.END)
                    self.output_text_field.insert(tk.END, decrypted_text.decode())
                    self.message("Decryptation successful", "success")
                except Exception as e:
                    self.message("Incorrect key", "error")
            else:
                print("ключ разный")
                print(user_key)
                print(str_key)
                
        
if __name__ == "__main__":
    app = App()
    app.root.mainloop()
