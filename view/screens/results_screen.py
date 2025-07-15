import tkinter as tk
from tkinter import ttk, filedialog
import os

class ResultsScreen(tk.Frame):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.view = view
        self.controller = None

        self.configure(bg="#FFFDE7") # Fondo amarillo claro

        # controles
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side="top", fill="x", padx=10, pady=5)
        ttk.Button(control_frame, text="Guardar Resultados", command=self._save_results).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Volver al Menú", command=self._go_back).pack(side="right", padx=10)





        # PanedWindow para organizar ------------------------------------------------------------------------------------------------------
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=5)

        # Panel Superior: Texto Original, Codificado, Decodificado
        top_panel = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(top_panel, weight=1)

        ttk.Label(top_panel, text="Texto Original:").pack(anchor="w", pady=2)
        self.original_text_display = tk.Text(top_panel, wrap="word", height=5, font=('Consolas', 10))
        self.original_text_display.pack(fill="x", pady=2)
        self.original_text_display.config(state="disabled")

        ttk.Label(top_panel, text="Algoritmo Utilizado:").pack(anchor="w", pady=2)
        self.algo_used_label = ttk.Label(top_panel, text="N/A", font=('Inter', 10, 'bold'))
        self.algo_used_label.pack(anchor="w", padx=5, pady=2)

        ttk.Label(top_panel, text="Texto Codificado (Bits):").pack(anchor="w", pady=2)
        self.encoded_text_display = tk.Text(top_panel, wrap="word", height=5, font=('Consolas', 10))
        self.encoded_text_display.pack(fill="x", pady=2)
        self.encoded_text_display.config(state="disabled")

        ttk.Label(top_panel, text="Texto Decodificado:").pack(anchor="w", pady=2)
        self.decoded_text_display = tk.Text(top_panel, wrap="word", height=5, font=('Consolas', 10))
        self.decoded_text_display.pack(fill="x", pady=2)
        self.decoded_text_display.config(state="disabled")




        # Panel Inferior: Frecuencias, Códigos, Métricas
        bottom_panel = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(bottom_panel, weight=1)

        ttk.Label(bottom_panel, text="Frecuencias de Símbolos:").pack(anchor="w", pady=2)
        self.freq_text_display = tk.Text(bottom_panel, wrap="word", height=6, font=('Consolas', 9))
        self.freq_text_display.pack(fill="x", pady=2)
        self.freq_text_display.config(state="disabled")

        ttk.Label(bottom_panel, text="Tabla de Códigos:").pack(anchor="w", pady=2)
        self.codes_text_display = tk.Text(bottom_panel, wrap="word", height=8, font=('Consolas', 9))
        self.codes_text_display.pack(fill="x", pady=2)
        self.codes_text_display.config(state="disabled")

        ttk.Label(bottom_panel, text="Métricas de Compresión:", font=('Inter', 12, 'bold')).pack(anchor="w", pady=5)
        self.avg_len_label = ttk.Label(bottom_panel, text="Longitud Promedio: N/A", font=('Inter', 10))
        self.avg_len_label.pack(anchor="w", padx=10)
        self.compression_rate_label = ttk.Label(bottom_panel, text="Tasa de Compresión: N/A", font=('Inter', 10))
        self.compression_rate_label.pack(anchor="w", padx=10)




    def set_controller(self, controller):
        self.controller = controller

    def _save_results(self):
        if self.controller:
            self.controller.save_results()

    def _go_back(self):
        if self.controller:
            self.controller.show_main_menu()

    def update_text_widget(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.config(state="disabled")





    def display_results(self, original_text, algorithm_used, encoded_text, decoded_text, frequencies, codes, avg_len, compression_rate):
        self.update_text_widget(self.original_text_display, original_text)
        self.algo_used_label.config(text=algorithm_used)
        self.update_text_widget(self.encoded_text_display, encoded_text)
        self.update_text_widget(self.decoded_text_display, decoded_text)

        freq_str = "\n".join([f"'{char}': {freq}" for char, freq in frequencies.items()])
        self.update_text_widget(self.freq_text_display, freq_str)

        codes_str = "\n".join([f"'{char}': {code}" for char, code in codes.items()])
        self.update_text_widget(self.codes_text_display, codes_str)

        self.avg_len_label.config(text=f"Longitud Promedio: {avg_len:.2f} bits/símbolo")
        self.compression_rate_label.config(text=f"Tasa de Compresión: {compression_rate:.2f}%")

    def clear_results(self):
        self.update_text_widget(self.original_text_display, "")
        self.algo_used_label.config(text="N/A")
        self.update_text_widget(self.encoded_text_display, "")
        self.update_text_widget(self.decoded_text_display, "")
        self.update_text_widget(self.freq_text_display, "")
        self.update_text_widget(self.codes_text_display, "")
        self.avg_len_label.config(text="Longitud Promedio: N/A")
        self.compression_rate_label.config(text="Tasa de Compresión: N/A")

    def on_show(self):

        if self.controller:
            self.display_results(
                self.controller.get_original_text(),
                self.controller.get_last_algorithm_used(),
                self.controller.get_encoded_bits(),
                self.controller.get_decoded_text(),
                self.controller.get_frequencies(),
                self.controller.get_codes(),
                self.controller.get_avg_len(),
                self.controller.get_compression_rate()
            )
        else:
            self.clear_results()