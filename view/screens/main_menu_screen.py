import tkinter as tk
from tkinter import ttk

class MainMenuScreen(tk.Frame):
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


        s.configure('TFrame', background=self.background_color)


        s.configure('Modern.TButton',
                    font=('Segoe UI', 16, 'bold'),
                    padding=15,
                    background=self.primary_color,
                    foreground=self.text_color_light,
                    relief='flat',
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor=self.primary_color
                   )

        s.map('Modern.TButton',
              background=[('active', self.secondary_color)],
              foreground=[('active', self.text_color_dark)],
              relief=[('pressed', 'flat')]
             )


        s.configure('Title.TLabel',
                    font=('Segoe UI', 24, 'bold'),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )


        buttons_frame = ttk.Frame(self, padding="40 40 40 40")

        buttons_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        ttk.Label(buttons_frame, text="¡Bienvenido! Elige una opción:", style='Title.TLabel').pack(pady=30)

        ttk.Button(buttons_frame, text="Codificación Shannon-Fano", command=self._go_to_shannon_fano, style='Modern.TButton').pack(fill="x", pady=12, ipadx=60, ipady=12)
        ttk.Button(buttons_frame, text="Codificación Huffman", command=self._go_to_huffman, style='Modern.TButton').pack(fill="x", pady=12, ipadx=60, ipady=12)
        ttk.Button(buttons_frame, text="Ver Resultados", command=self._go_to_results, style='Modern.TButton').pack(fill="x", pady=12, ipadx=60, ipady=12)
        ttk.Button(buttons_frame, text="Mostrar Gráficos", command=self._go_to_metrics_chart, style='Modern.TButton').pack(fill="x", pady=12, ipadx=60, ipady=12)




    def set_controller(self, controller):
        self.controller = controller

    def _go_to_shannon_fano(self):
        if self.controller:
            self.controller.show_shannon_fano_screen()

    def _go_to_huffman(self):
        if self.controller:
            self.controller.show_huffman_screen()

    def _go_to_results(self):
        if self.controller:
            self.controller.show_results_screen()

    def _go_to_metrics_chart(self):
        if self.controller:
            self.controller.show_metrics_chart_screen()