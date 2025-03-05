import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

class FileEncrypter:
    def __init__(self, root):
        self.root = root
        self.root.title("Cifrador de Archivos")
        self.root.geometry("400x300")
        
        # Variable para almacenar la clave
        self.key = None
        
        # Elementos de la interfaz
        self.label = tk.Label(root, text="Cifrador de Archivos", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.select_button = tk.Button(root, text="Seleccionar Archivo", command=self.select_file)
        self.select_button.pack(pady=5)
        
        self.file_label = tk.Label(root, text="Ningún archivo seleccionado", wraplength=350)
        self.file_label.pack(pady=5)
        
        self.generate_key_button = tk.Button(root, text="Generar Clave", command=self.generate_key)
        self.generate_key_button.pack(pady=5)
        
        self.key_label = tk.Label(root, text="Clave no generada", wraplength=350)
        self.key_label.pack(pady=5)
        
        self.encrypt_button = tk.Button(root, text="Cifrar Archivo", command=self.encrypt_file, state="disabled")
        self.encrypt_button.pack(pady=5)
        
        self.decrypt_button = tk.Button(root, text="Descifrar Archivo", command=self.decrypt_file, state="disabled")
        self.decrypt_button.pack(pady=5)
        
        self.selected_file = None

    def select_file(self):
        self.selected_file = filedialog.askopenfilename()
        if self.selected_file:
            self.file_label.config(text=f"Archivo: {os.path.basename(self.selected_file)}")
            if self.key:
                self.encrypt_button.config(state="normal")
                self.decrypt_button.config(state="normal")

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.key_label.config(text=f"Clave: {self.key.decode()}")
        if self.selected_file:
            self.encrypt_button.config(state="normal")
            self.decrypt_button.config(state="normal")
        messagebox.showinfo("Clave Generada", 
                          "Guarda esta clave en un lugar seguro.\nLa necesitarás para descifrar el archivo.")

    def encrypt_file(self):
        if not self.selected_file or not self.key:
            messagebox.showerror("Error", "Selecciona un archivo y genera una clave primero")
            return
        
        try:
            fernet = Fernet(self.key)
            with open(self.selected_file, 'rb') as file:
                file_data = file.read()
            encrypted_data = fernet.encrypt(file_data)
            
            output_file = self.selected_file + '.encrypted'
            with open(output_file, 'wb') as file:
                file.write(encrypted_data)
            
            messagebox.showinfo("Éxito", f"Archivo cifrado guardado como:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cifrar: {str(e)}")

    def decrypt_file(self):
        if not self.selected_file or not self.key:
            messagebox.showerror("Error", "Selecciona un archivo y genera una clave primero")
            return
        
        try:
            fernet = Fernet(self.key)
            with open(self.selected_file, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            
            output_file = self.selected_file.replace('.encrypted', '_decrypted')
            with open(output_file, 'wb') as file:
                file.write(decrypted_data)
            
            messagebox.showinfo("Éxito", f"Archivo descifrado guardado como:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descifrar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncrypter(root)
    root.mainloop()