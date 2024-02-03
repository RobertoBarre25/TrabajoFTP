import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ftplib import FTP
import os

class FileTransferApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FTP File Transfer")

        self.ftp_host = 'RoberFtp.somee.com'
        self.ftp_user = 'RobertoB2'
        self.ftp_pass = 'Amoelfutbol25'

        self.bg_color = '#34495e'
        self.button_color = '#2ecc71'
        self.label_color = 'white'
        self.font_style = ('Helvetica', 12)

        self.master.configure(bg=self.bg_color)

        self.file_listbox = tk.Listbox(master, selectmode=tk.SINGLE, bg=self.bg_color, fg=self.label_color, font=self.font_style)
        self.file_listbox.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)
        self.file_list_label = tk.Label(master, text="Archivos en el servidor:", bg=self.bg_color, fg=self.label_color, font=self.font_style)
        self.file_list_label.pack(side=tk.RIGHT, padx=20, pady=(20, 0))

        style = ttk.Style()
        style.configure('TButton', padding=6, relief="flat", background=self.button_color, font=self.font_style)
        style.map('TButton', background=[('active', self.button_color)])

        self.browse_button = ttk.Button(master, text="Examinar", command=self.browse_file, style='TButton')
        self.browse_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.upload_button = ttk.Button(master, text="Subir Archivo", command=self.upload_file, style='TButton')
        self.upload_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.download_button = ttk.Button(master, text="Descargar Seleccionado", command=self.download_selected_file, style='TButton')
        self.download_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.populate_file_list()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()

    def upload_file(self):
        if hasattr(self, 'file_path'):
            try:
                with FTP() as ftp:
                    ftp.connect(self.ftp_host)
                    ftp.login(self.ftp_user, self.ftp_pass)
                    ftp.cwd('/www.RoberFtp.somee.com')
                    with open(self.file_path, 'rb') as local_file:
                        ftp.storbinary(f"STOR {os.path.basename(self.file_path)}", local_file)
                messagebox.showinfo("Éxito", "Archivo subido correctamente.")
                self.populate_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error. Detalles: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo antes de subirlo.")

    def populate_file_list(self):
        self.file_listbox.delete(0, tk.END)
        try:
            with FTP() as ftp:
                ftp.connect(self.ftp_host)
                ftp.login(self.ftp_user, self.ftp_pass)
                ftp.cwd('/www.RoberFtp.somee.com')
                file_list = ftp.nlst()
                for file in file_list:
                    self.file_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error. Detalles: {str(e)}")

    def download_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index[0])
            try:
                with FTP() as ftp:
                    ftp.connect(self.ftp_host)
                    ftp.login(self.ftp_user, self.ftp_pass)
                    ftp.cwd('/www.RoberFtp.somee.com')
                    with open(selected_file, 'wb') as local_file:
                        ftp.retrbinary(f"RETR {selected_file}", local_file.write)
                messagebox.showinfo("Éxito", "Archivo descargado correctamente.")
                self.populate_file_list()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error. Detalles: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un archivo antes de descargar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()
