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
        master.geometry("1000x800")
        master.resizable(True, True)

        self.controller = None

        # dicc para almacenar las instancias de cada pantalla
        self.screens = {}
        self.current_screen = None


        # contenedor principal donde se mostrarán las pantallas --------------------
        self.container = ttk.Frame(master)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._create_screens()

    def set_controller(self, controller):
        self.controller = controller
        # Pasa el controlador a cada pantalla para que puedan interactuar
        for screen_name, screen_instance in self.screens.items():
            screen_instance.set_controller(controller)

    def _create_screens(self):

        self.screens["welcome"] = WelcomeScreen(self.container, self)
        self.screens["main_menu"] = MainMenuScreen(self.container, self)
        self.screens["huffman"] = HuffmanScreen(self.container, self)
        self.screens["shannon_fano"] = ShannonFanoScreen(self.container, self)
        self.screens["results"] = ResultsScreen(self.container, self)
        self.screens["metrics_chart"] = MetricsChartScreen(self.container, self)



        # todas las pantallas en la misma celda de la cuadrícula, pero ocultas
        for name, screen in self.screens.items():
            screen.grid(row=0, column=0, sticky="nsew")

        self.show_screen("welcome")

    def show_screen(self, name):

        if name in self.screens:
            if self.current_screen:
                self.current_screen.pack_forget()
                self.current_screen.grid_forget()

            screen = self.screens[name]
            screen.grid(row=0, column=0, sticky="nsew")
            self.current_screen = screen
            screen.tkraise() #


            if self.controller:
                self.controller.on_screen_shown(name)
        else:
            print(f"Error: Pantalla '{name}' no encontrada.")


    def get_screen(self, name):
        return self.screens.get(name)



    def show_message(self, title, message, type="info"):

        if type == "info":
            tk.messagebox.showinfo(title, message)
        elif type == "error":
            tk.messagebox.showerror(title, message)
        elif type == "warning":
            tk.messagebox.showwarning(title, message)