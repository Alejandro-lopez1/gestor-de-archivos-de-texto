import os
import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
import csv
from fpdf import FPDF

class TextFileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Archivos de Texto")
        self.geometry("400x200")

        self.text_area = tk.Text(self, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Nuevo", command=self.new_file)
        self.file_menu.add_command(label="Abrir", command=self.open_file)
        self.file_menu.add_command(label="Guardar", command=self.save_file)
        self.file_menu.add_command(label="Exportar como PDF", command=self.export_as_pdf)
        self.file_menu.add_command(label="Exportar como CSV", command=self.export_as_csv)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.quit)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.config(menu=self.menu_bar)

        self.current_file = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Archivos PDF", "*.pdf"), ("Archivos CSV", "*.csv")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)

        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*txt"), ("Archivos PDF", "*.pdf"), ("Archivos CSV", "*.csv")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path

    def export_as_pdf(self):
        if self.current_file:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            content = self.text_area.get(1.0, tk.END)
            for line in content.split("\n"):
                pdf.cell(200, 10, txt=line, ln=True)
            file_path = self.current_file.replace(".txt", ".pdf")
            pdf.output(file_path)
            messagebox.showinfo("Exportar PDF", "El archivo se ha exportado correctamente como PDF.")
        else:
            messagebox.showwarning("Exportar PDF", "No hay ningún archivo abierto.")

    def export_as_csv(self):
        if self.current_file:
            file_path = self.current_file.replace(".txt", ".csv")
            content = self.text_area.get(1.0, tk.END)
            lines = content.split("\n")
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                for line in lines:
                    writer.writerow(line.split("\t"))  # Suponiendo que el archivo de texto está tabulado
            messagebox.showinfo("Exportar CSV", "El archivo se ha exportado correctamente como CSV.")
        else:
            messagebox.showwarning("Exportar CSV", "No hay ningún archivo abierto.")

if __name__ == "__main__":
    app = TextFileManagerApp()
    app.mainloop()
