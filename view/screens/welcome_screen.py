import tkinter as tk
from tkinter import ttk

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.view = view
        self.controller = None

        self.configure(bg="#F0F0F0")

        # Contenedor central para el contenido
        center_frame = ttk.Frame(self, padding="50 50 50 50", style='Welcome.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Centra frame

        # Estilo frame central
        #self.master.master.master.tk.call("source", "azure.tcl") # Cargar tema Azure si no está cargado



        s = ttk.Style()
        s.configure('Welcome.TFrame', background='#FFFFFF', relief='raised', borderwidth=2, borderradius=15)
        s.configure('Welcome.TLabel', font=('Inter', 24, 'bold'), foreground='#333333')
        s.configure('Welcome.TButton', font=('Inter', 14, 'bold'), padding=15, background='#007BFF', foreground='white', relief='raised', borderwidth=0, borderradius=10)
        s.map('Welcome.TButton',
              background=[('active', '#0056b3')],
              foreground=[('active', 'white')])

        # Título
        ttk.Label(center_frame, text="¡Bienvenido al Compresor de Texto!", style='Welcome.TLabel').pack(pady=20)

        # Descripción,,
        ttk.Label(center_frame, text="Explora los algoritmos de compresión Huffman y Shannon-Fano.",
                  font=('Inter', 12), foreground='#555555').pack(pady=10)

        # Botón para iniciar
        ttk.Button(center_frame, text="Comenzar", command=self._go_to_main_menu, style='Welcome.TButton').pack(pady=30)



    def set_controller(self, controller):
        self.controller = controller




    def _go_to_main_menu(self):
        if self.controller:
            self.controller.show_main_menu()