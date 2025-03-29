import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from cryptor import Cryptor

class App:
    def __init__(self):
        self.cryptor = Cryptor()
        self.file_opener = FileOpener()
        self.root = tk.Tk()

        self.root.title('Cryptor Decryptor')
        self.root.resizable(False, False)
        self.root.geometry('900x450')

    def show_widgets(self):
        input_label = ttk.Label(self.root, text="Input:")
        input_label.pack()

        input_text_field = tk.Text(self.root, width=30, height=7)
        input_text_field.pack()

        output_label = ttk.Label(self.root, text="Output:")
        output_label.place(relx=0.47, rely=0.41)

        output_text_field = tk.Text(self.root, width=30, height=7)
        output_text_field.place(relx=0.36, rely=0.45)

        open_file_button = ttk.Button(
            master=self.root,
            text='Open a File',
            command=self.file_opener.open_file,
            width=25
        )
        
        start_crypt_button = ttk.Button(
            master=self.root,
            text='Start Crypt',
            command=self.cryptor.start_crypt,
            width=20
        )

        start_decrypt_button = ttk.Button(
            master=self.root,
            text='Start Decrypt',
            command=self.cryptor.start_decrypt,
            width=20
        )

        start_crypt_button.place(relx=0.35, rely=0.32)
        start_decrypt_button.place(relx=0.50, rely=0.32)

        open_file_button.place(relx=0.01)


class FileOpener:
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    def check_choosed_file(self):
        if (self.file_path):
            showinfo(title='Selected File', message=self.file_path)

    def open_file(self):
        self.file_path = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=self.filetypes)
        
        self.check_choosed_file()

    def get_file_path(self) -> str:
        return self.file_path


class FileReader():
    def __init__(self):
        file = FileOpener()
        self.file_path = file.get_file_path()

    
if __name__ == "__main__":
    app = App()
    app.show_widgets()
    app.root.mainloop()
