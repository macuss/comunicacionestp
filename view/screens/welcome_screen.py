import tkinter as tk
from tkinter import ttk

class WelcomeScreen(tk.Frame):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.view = view
        self.controller = None

        self.primary_color = "#6c5ce7"
        self.secondary_color = "#a29bfe"
        self.accent_color = "#00b894"
        self.background_color = "#f5f6fa"
        self.text_color_dark = "#2d3436"
        self.text_color_light = "#ffffff"

        self.configure(bg=self.background_color)

        s = ttk.Style()
        try:
            s.theme_use('clam')
        except tk.TclError:
            print("El tema 'clam' no está disponible. Usando el tema predeterminado.")
            s.theme_use('default')

        s.configure('Welcome.TFrame',
                    background=self.background_color,
                    font=('Segoe UI', 38, 'bold'),
                    relief='flat',
                    borderwidth=0
                   )
        center_frame = ttk.Frame(self, padding="60 60 60 60", style='Welcome.TFrame')
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        s.configure('WelcomeTitle.TLabel',
                    font=('Segoe UI', 38, 'bold'),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )

        s.configure('WelcomeDescription.TLabel',
                    font=('Segoe UI', 30),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )

        s.configure('Welcome.TButton',
                    font=('Segoe UI', 20, 'bold'),
                    padding=18,
                    background=self.primary_color,
                    foreground=self.text_color_light,
                    relief='flat',
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor=self.primary_color
                   )
        s.map('Welcome.TButton',
              background=[('active', self.secondary_color)],
              foreground=[('active', self.text_color_dark)],
              relief=[('pressed', 'flat')]
             )

        ttk.Label(center_frame, text="Comunicaciones 2025", style='WelcomeTitle.TLabel').pack(pady=(20, 5))

        ttk.Label(center_frame, text="TP Integrador: Algoritmos de Compresión", style='WelcomeDescription.TLabel').pack(pady=(5, 10))

        ttk.Label(center_frame, text="Implementación de Huffman y Shannon-Fano.", style='WelcomeDescription.TLabel').pack(pady=(5, 30))

        ttk.Button(center_frame, text="Comenzar", command=self._go_to_main_menu, style='Welcome.TButton').pack(pady=20)

    def set_controller(self, controller):
        self.controller = controller

    def _go_to_main_menu(self):
        if self.controller:
            self.controller.show_main_menu()
