import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class ShannonFanoScreen(tk.Frame):
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

        s.configure('Modern.TLabelframe',
                    background=self.background_color,
                    foreground=self.text_color_dark,
                    relief='flat',
                    borderwidth=1,
                    font=('Segoe UI', 14, 'bold')
                   )
        s.configure('Modern.TLabelframe.Label',
                    background=self.background_color,
                    foreground=self.text_color_dark,
                    font=('Segoe UI', 14, 'bold')
                   )

        s.configure('Modern.TText',
                    background='#ffffff',
                    foreground=self.text_color_dark,
                    font=('Consolas', 10),
                    relief='flat',
                    borderwidth=1,
                    bordercolor='#cccccc'
                   )

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
                    font=('Segoe UI', 16, 'bold'),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )

        self.input_frame = ttk.LabelFrame(self, text="Entrada de Texto y Controles", padding="15 15 15 15", style='Modern.TLabelframe')
        self.input_frame.pack(side="top", fill="x", padx=20, pady=10)

        self.results_frame = ttk.LabelFrame(self, text="Resultados de Shannon-Fano", padding="15 15 15 15", style='Modern.TLabelframe')
        self.results_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.text_input = tk.Text(self.input_frame, wrap="word", height=8, width=80, font=('Consolas', 16),
                                  background='#ffffff', foreground=self.text_color_dark,
                                  relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.text_input.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.text_input.insert(tk.END, "Introduce tu texto aquí o carga un archivo para Shannon-Fano.")

        scrollbar_input = ttk.Scrollbar(self.input_frame, command=self.text_input.yview)
        scrollbar_input.pack(side="right", fill="y")
        self.text_input.config(yscrollcommand=scrollbar_input.set)

        button_frame = ttk.Frame(self.input_frame, style='TFrame')
        button_frame.pack(side="top", padx=10, pady=10)

        ttk.Button(button_frame, text="Cargar Archivo .txt", command=self._load_file, style='Action.TButton').pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Comprimir Shannon-Fano", command=self._compress, style='Action.TButton').pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Descomprimir Shannon-Fano", command=self._decompress, style='Action.TButton').pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Volver al Menú", command=self._go_back, style='Neutral.TButton').pack(fill="x", pady=15)

        ttk.Label(self.results_frame, text="Frecuencias de Símbolos:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.freq_text = tk.Text(self.results_frame, wrap="word", height=6, font=('Consolas', 16),
                                 background='#ffffff', foreground=self.text_color_dark,
                                 relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.freq_text.pack(fill="x", pady=2, padx=5)
        self.freq_text.config(state="disabled")

        ttk.Label(self.results_frame, text="Tabla de Códigos Shannon-Fano:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.codes_text = tk.Text(self.results_frame, wrap="word", height=8, font=('Consolas', 16),
                                  background='#ffffff', foreground=self.text_color_dark,
                                  relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.codes_text.pack(fill="x", pady=2, padx=5)
        self.codes_text.config(state="disabled")

        ttk.Label(self.results_frame, text="Texto Codificado (Bits):", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.encoded_text = tk.Text(self.results_frame, wrap="word", height=6, font=('Consolas', 16),
                                   background='#ffffff', foreground=self.text_color_dark,
                                   relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.encoded_text.pack(fill="x", pady=2, padx=5)
        self.encoded_text.config(state="disabled")

        ttk.Label(self.results_frame, text="Texto Decodificado:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.decoded_text = tk.Text(self.results_frame, wrap="word", height=6, font=('Consolas', 16),
                                   background='#ffffff', foreground=self.text_color_dark,
                                   relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.decoded_text.pack(fill="x", pady=2, padx=5)
        self.decoded_text.config(state="disabled")

    def set_controller(self, controller):
        self.controller = controller

    def _load_file(self):
        if self.controller:
            file_path = filedialog.askopenfilename(
                filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.text_input.delete("1.0", tk.END)
                        self.text_input.insert("1.0", content)
                        self.controller.set_original_text(content)
                        self.view.show_message("Carga Exitosa", f"Archivo '{os.path.basename(file_path)}' cargado correctamente.")
                        self.clear_outputs()
                except Exception as e:
                    self.view.show_message("Error de Carga", f"No se pudo leer el archivo: {e}", type="error")

    def _compress(self):
        if self.controller:
            text = self.text_input.get("1.0", tk.END).strip()
            self.controller.set_original_text(text)
            self.controller.compress_text("Shannon-Fano")

    def _decompress(self):
        if self.controller:
            self.controller.decompress_text("Shannon-Fano")

    def _go_back(self):
        if self.controller:
            self.controller.show_main_menu()

    def clear_outputs(self):
        self.update_text_widget(self.freq_text, "")
        self.update_text_widget(self.codes_text, "")
        self.update_text_widget(self.encoded_text, "")
        self.update_text_widget(self.decoded_text, "")

    def update_text_widget(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", content)
        widget.config(state="disabled")

    def display_frequencies(self, frequencies):
        freq_str = "\n".join([f"'{char}': {freq}" for char, freq in frequencies.items()])
        self.update_text_widget(self.freq_text, freq_str)

    def display_codes(self, codes):
        codes_str = "\n".join([f"'{char}': {code}" for char, code in codes.items()])
        self.update_text_widget(self.codes_text, codes_str)

    def display_encoded_text(self, encoded_text):
        self.update_text_widget(self.encoded_text, encoded_text)

    def display_decoded_text(self, decoded_text):
        self.update_text_widget(self.decoded_text, decoded_text)

    def on_show(self):
        if self.controller and self.controller.get_original_text():
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", self.controller.get_original_text())
        self.clear_outputs()