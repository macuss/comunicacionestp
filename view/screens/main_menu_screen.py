import tkinter as tk
from tkinter import ttk

class MainMenuScreen(tk.Frame):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.view = view
        self.controller = None

        self.configure(bg="#F8F8F8") # Un color de fondo claro

        # Estilo para los botones grandes
        s = ttk.Style()
        s.configure('MainMenu.TButton', font=('Inter', 16, 'bold'), padding=20,
                    background='#4CAF50', foreground='white', relief='raised', borderwidth=0, borderradius=10)
        s.map('MainMenu.TButton',
              background=[('active', '#45a049')],
              foreground=[('active', 'white')])

        # Contenedor para los botones
        buttons_frame = ttk.Frame(self, padding="30 30 30 30")
        buttons_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Centrar el frame de botones

        # Título
        ttk.Label(buttons_frame, text="Selecciona una opción:", font=('Inter', 20, 'bold'), foreground='#333333').pack(pady=20)

        # Botones grandes
        ttk.Button(buttons_frame, text="Shannon-Fano", command=self._go_to_shannon_fano, style='MainMenu.TButton').pack(fill="x", pady=10, ipadx=50, ipady=10)
        ttk.Button(buttons_frame, text="Huffman", command=self._go_to_huffman, style='MainMenu.TButton').pack(fill="x", pady=10, ipadx=50, ipady=10)
        ttk.Button(buttons_frame, text="Resultados", command=self._go_to_results, style='MainMenu.TButton').pack(fill="x", pady=10, ipadx=50, ipady=10)
        ttk.Button(buttons_frame, text="Gráficos", command=self._go_to_metrics_chart, style='MainMenu.TButton').pack(fill="x", pady=10, ipadx=50, ipady=10)

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