import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class ResultsScreen(tk.Frame):
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
        self.neutral_color = "#607d8b"
        self.neutral_hover_color = "#78909c"

        self.configure(bg=self.background_color)



        s = ttk.Style()
        try:
            s.theme_use('clam')
        except tk.TclError:
            print("El tema 'clam' no está disponible. Usando el tema predeterminado.")
            s.theme_use('default')

        s.configure('TFrame', background=self.background_color)

        s.configure('Action.TButton',
                    font=('Segoe UI', 12, 'bold'),
                    padding=10,
                    background=self.primary_color,
                    foreground=self.text_color_light,
                    relief='flat',
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor=self.primary_color
                   )
        s.map('Action.TButton',
              background=[('active', self.secondary_color)],
              foreground=[('active', self.text_color_dark)],
              relief=[('pressed', 'flat')]
             )


        s.configure('Neutral.TButton',
                    font=('Segoe UI', 12, 'bold'),
                    padding=10,
                    background=self.neutral_color,
                    foreground=self.text_color_light,
                    relief='flat',
                    borderwidth=0,
                    focusthickness=0,
                    focuscolor=self.neutral_color
                   )
        s.map('Neutral.TButton',
              background=[('active', self.neutral_hover_color)],
              foreground=[('active', self.text_color_light)],
              relief=[('pressed', 'flat')]
             )

        s.configure('Result.TLabel',
                    font=('Segoe UI', 11, 'bold'),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )

        s.configure('Metrics.TLabel',
                    font=('Segoe UI', 13, 'bold'),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )
        s.configure('MetricsValue.TLabel',
                    font=('Segoe UI', 11),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )






        # controles -----------------
        control_frame = ttk.Frame(self, padding="10 10 10 10", style='TFrame')
        control_frame.pack(side="top", fill="x", padx=20, pady=10)
        ttk.Button(control_frame, text="Guardar Resultados", command=self._save_results, style='Action.TButton').pack(side="left", padx=10)
        ttk.Button(control_frame, text="Volver al Menú", command=self._go_back, style='Neutral.TButton').pack(side="right", padx=10)

        # PanedWindow para organizar
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL, style='TFrame')
        self.paned_window.pack(fill="both", expand=True, padx=20, pady=10)





        # panel Superior: Texto Original, Codificado, Decodificado ----------------------------------------------------------
        top_panel = ttk.Frame(self.paned_window, padding="15 15 15 15", style='TFrame')
        self.paned_window.add(top_panel, weight=1)

        ttk.Label(top_panel, text="Texto Original:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))

        self.original_text_display = tk.Text(top_panel, wrap="word", height=5,
                                             font=('Consolas', 10), background='#ffffff', foreground=self.text_color_dark,
                                             relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.original_text_display.pack(fill="x", pady=2, padx=5)
        self.original_text_display.config(state="disabled")

        ttk.Label(top_panel, text="Algoritmo Utilizado:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.algo_used_label = ttk.Label(top_panel, text="N/A", style='MetricsValue.TLabel')
        self.algo_used_label.pack(anchor="w", padx=5, pady=2)

        ttk.Label(top_panel, text="Texto Codificado (Bits):", style='Result.TLabel').pack(anchor="w", pady=(5, 2))


        self.encoded_text_display = tk.Text(top_panel, wrap="word", height=5,
                                            font=('Consolas', 10), background='#ffffff', foreground=self.text_color_dark,
                                            relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.encoded_text_display.pack(fill="x", pady=2, padx=5)
        self.encoded_text_display.config(state="disabled")

        ttk.Label(top_panel, text="Texto Decodificado:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))


        self.decoded_text_display = tk.Text(top_panel, wrap="word", height=5,
                                            font=('Consolas', 10), background='#ffffff', foreground=self.text_color_dark,
                                            relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.decoded_text_display.pack(fill="x", pady=2, padx=5)
        self.decoded_text_display.config(state="disabled")




        # panel Inferior: Frecuencias, Códigos, Métricas ------------------------------------------------------
        bottom_panel = ttk.Frame(self.paned_window, padding="15 15 15 15", style='TFrame')
        self.paned_window.add(bottom_panel, weight=1)

        ttk.Label(bottom_panel, text="Frecuencias de Símbolos:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))


        self.freq_text_display = tk.Text(bottom_panel, wrap="word", height=6,
                                         font=('Consolas', 9), background='#ffffff', foreground=self.text_color_dark,
                                         relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.freq_text_display.pack(fill="x", pady=2, padx=5)
        self.freq_text_display.config(state="disabled")

        ttk.Label(bottom_panel, text="Tabla de Códigos:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))

        self.codes_text_display = tk.Text(bottom_panel, wrap="word", height=8,
                                          font=('Consolas', 9), background='#ffffff', foreground=self.text_color_dark,
                                          relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.codes_text_display.pack(fill="x", pady=2, padx=5)
        self.codes_text_display.config(state="disabled")

        ttk.Label(bottom_panel, text="Métricas de Compresión:", style='Metrics.TLabel').pack(anchor="w", pady=(10, 5))
        self.avg_len_label = ttk.Label(bottom_panel, text="Longitud Promedio: N/A", style='MetricsValue.TLabel')
        self.compression_rate_label = ttk.Label(bottom_panel, text="Tasa de Compresión: N/A", style='MetricsValue.TLabel')
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


        avg_len_text = f"Longitud Promedio: {avg_len:.2f} bits/símbolo" if avg_len is not None else "Longitud Promedio: N/A"
        compression_rate_text = f"Tasa de Compresión: {compression_rate:.2f}%" if compression_rate is not None else "Tasa de Compresión: N/A"

        self.avg_len_label.config(text=avg_len_text)
        self.compression_rate_label.config(text=compression_rate_text)

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