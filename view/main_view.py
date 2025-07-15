import tkinter as tk
from tkinter import ttk

# Importar las nuevas clases de pantalla
from view.screens.welcome_screen import WelcomeScreen
from view.screens.main_menu_screen import MainMenuScreen
from view.screens.huffman_screen import HuffmanScreen
from view.screens.shannon_fano_screen import ShannonFanoScreen
from view.screens.results_screen import ResultsScreen
from view.screens.metrics_chart_screen import MetricsChartScreen

class MainView:
    def __init__(self, master):
        self.master = master
        master.title("Compresor Huffman y Shannon-Fano")
        master.geometry("1000x800") # Tamaño inicial
        master.resizable(True, True)

        self.controller = None # Se asignará desde el controlador

        # Diccionario para almacenar las instancias de cada pantalla
        self.screens = {}
        self.current_screen = None

        # Contenedor principal donde se mostrarán las pantallas
        self.container = ttk.Frame(master)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._create_screens()

    def set_controller(self, controller):
        self.controller = controller
        # Pasar el controlador a cada pantalla para que puedan interactuar
        for screen_name, screen_instance in self.screens.items():
            screen_instance.set_controller(controller)

    def _create_screens(self):
        """Crea todas las instancias de las pantallas y las almacena."""
        self.screens["welcome"] = WelcomeScreen(self.container, self)
        self.screens["main_menu"] = MainMenuScreen(self.container, self)
        self.screens["huffman"] = HuffmanScreen(self.container, self)
        self.screens["shannon_fano"] = ShannonFanoScreen(self.container, self)
        self.screens["results"] = ResultsScreen(self.container, self)
        self.screens["metrics_chart"] = MetricsChartScreen(self.container, self)

        # Colocar todas las pantallas en la misma celda de la cuadrícula, pero ocultas
        for name, screen in self.screens.items():
            screen.grid(row=0, column=0, sticky="nsew")

        self.show_screen("welcome") # Mostrar la pantalla de bienvenida al inicio

    def show_screen(self, name):
        """
        Muestra la pantalla especificada por su nombre y oculta la actual.
        Args:
            name (str): El nombre de la pantalla a mostrar (ej. "welcome", "main_menu").
        """
        if name in self.screens:
            if self.current_screen:
                self.current_screen.pack_forget() # Oculta la pantalla actual si usa pack
                self.current_screen.grid_forget() # Oculta la pantalla actual si usa grid

            screen = self.screens[name]
            screen.grid(row=0, column=0, sticky="nsew") # Muestra la nueva pantalla
            self.current_screen = screen
            screen.tkraise() # Asegura que la pantalla esté en la parte superior

            # Notificar al controlador que la pantalla ha cambiado
            if self.controller:
                self.controller.on_screen_shown(name)
        else:
            print(f"Error: Pantalla '{name}' no encontrada.") # Para depuración
            # Aquí podrías mostrar un messagebox de error si lo deseas

    def get_screen(self, name):
        """Permite al controlador obtener una instancia de pantalla."""
        return self.screens.get(name)

    def show_message(self, title, message, type="info"):
        """Muestra un messagebox genérico."""
        if type == "info":
            tk.messagebox.showinfo(title, message)
        elif type == "error":
            tk.messagebox.showerror(title, message)
        elif type == "warning":
            tk.messagebox.showwarning(title, message)