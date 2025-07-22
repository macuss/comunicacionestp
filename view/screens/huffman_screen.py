import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os


class HuffmanScreen(tk.Frame):
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
                    font=('Consolas', 14),
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
                    font=('Segoe UI', 14, 'bold'),
                    foreground=self.text_color_dark,
                    background=self.background_color
                   )




        # frames Principales --------------------------------------------------
        self.input_frame = ttk.LabelFrame(self, text="Entrada de Texto y Controles", padding="15 15 15 15", style='Modern.TLabelframe')
        self.input_frame.pack(side="top", fill="x", padx=20, pady=10)

        self.results_frame = ttk.LabelFrame(self, text="Resultados de Huffman", padding="15 15 15 15", style='Modern.TLabelframe')
        self.results_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # entrada de texto --------------------------------------------------
        self.text_input = tk.Text(self.input_frame, wrap="word", height=8, width=80, font=('Consolas', 14),
                                  background='#ffffff', foreground=self.text_color_dark,
                                  relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.text_input.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.text_input.insert(tk.END, "Introduce tu texto aquí o carga un archivo para Huffman.")

        scrollbar_input = ttk.Scrollbar(self.input_frame, command=self.text_input.yview)
        scrollbar_input.pack(side="right", fill="y")
        self.text_input.config(yscrollcommand=scrollbar_input.set)


        button_frame = ttk.Frame(self.input_frame, style='TFrame')
        button_frame.pack(side="top", padx=10, pady=10)

        ttk.Button(button_frame, text="Cargar Archivo .txt", command=self._load_file, style='Action.TButton').pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Comprimir Huffman", command=self._compress, style='Action.TButton').pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Descomprimir Huffman", command=self._decompress, style='Action.TButton').pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Volver al Menú", command=self._go_back, style='Neutral.TButton').pack(fill="x", pady=15)

        # resultados (PanedWindow para organizar) ---------------------------------------------------------
        self.paned_window = ttk.PanedWindow(self.results_frame, orient=tk.HORIZONTAL, style='TFrame')
        self.paned_window.pack(fill="both", expand=True, padx=5, pady=5)




        # panel Izquierdo: frec, códigos, bits, decodificado --------------------------------------------------
        self.left_panel = ttk.Frame(self.paned_window, padding=5, style='TFrame')
        self.paned_window.add(self.left_panel, weight=1)

        ttk.Label(self.left_panel, text="Frecuencias de Símbolos:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.freq_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 12),
                                 background='#ffffff', foreground=self.text_color_dark,
                                 relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.freq_text.pack(fill="x", pady=2, padx=5)
        self.freq_text.config(state="disabled")

        ttk.Label(self.left_panel, text="Tabla de Códigos Huffman:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.codes_text = tk.Text(self.left_panel, wrap="word", height=8, font=('Consolas', 12),
                                  background='#ffffff', foreground=self.text_color_dark,
                                  relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.codes_text.pack(fill="x", pady=2, padx=5)
        self.codes_text.config(state="disabled")

        ttk.Label(self.left_panel, text="Texto Codificado (Bits):", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.encoded_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 12),
                                   background='#ffffff', foreground=self.text_color_dark,
                                   relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.encoded_text.pack(fill="x", pady=2, padx=5)
        self.encoded_text.config(state="disabled")

        ttk.Label(self.left_panel, text="Texto Decodificado:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))
        self.decoded_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 12),
                                   background='#ffffff', foreground=self.text_color_dark,
                                   relief='flat', borderwidth=1, highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.decoded_text.pack(fill="x", pady=2, padx=5)
        self.decoded_text.config(state="disabled")





        # panel Derecho: arbol de Huffman --------------------------------------------------
        self.right_panel = ttk.Frame(self.paned_window, padding=5, style='TFrame')
        self.paned_window.add(self.right_panel, weight=1)

        ttk.Label(self.right_panel, text="Visualización del Árbol de Huffman:", style='Result.TLabel').pack(anchor="w", pady=(5, 2))

        self.tree_canvas = tk.Canvas(self.right_panel, bg="white", borderwidth=1, relief="flat", highlightbackground='#cccccc', highlightcolor='#cccccc')
        self.tree_canvas.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_image_tk = None




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
                        self.view.show_message("Carga Exitosa",
                                               f"Archivo '{os.path.basename(file_path)}' cargado correctamente.")
                        self.clear_outputs()
                except Exception as e:
                    self.view.show_message("Error de Carga", f"No se pudo leer el archivo: {e}", type="error")



    def _compress(self):
        if self.controller:
            text = self.text_input.get("1.0", tk.END).strip()
            self.controller.set_original_text(text)
            self.controller.compress_text("Huffman")

    def _decompress(self):
        if self.controller:
            self.controller.decompress_text("Huffman")

    def _go_back(self):
        if self.controller:
            self.controller.show_main_menu()

    def clear_outputs(self):
        self.update_text_widget(self.freq_text, "")
        self.update_text_widget(self.codes_text, "")
        self.update_text_widget(self.encoded_text, "")
        self.update_text_widget(self.decoded_text, "")
        self.clear_huffman_tree_display()

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






# arbol
    def display_huffman_tree(self, image_path):
        self.clear_huffman_tree_display()
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                self.tree_canvas.update_idletasks()
                canvas_width = self.tree_canvas.winfo_width()
                canvas_height = self.tree_canvas.winfo_height()

                if canvas_width == 0 or canvas_height == 0:
                    canvas_width = 400
                    canvas_height = 400

                img_width, img_height = img.size

                scale_w = canvas_width / img_width
                scale_h = canvas_height / img_height
                scale_factor = min(scale_w, scale_h)

                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)

                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.tree_image_tk = ImageTk.PhotoImage(img)

                self.tree_canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.tree_image_tk, anchor="center")
                self.tree_canvas.image = self.tree_image_tk

            except Exception as e:
                self.view.show_message("Error de Imagen", f"No se pudo cargar la imagen del árbol: {e}", type="error")
        else:
            self.tree_canvas.create_text(self.tree_canvas.winfo_width() / 2, self.tree_canvas.winfo_height() / 2,
                                         text="Árbol no disponible.", fill="gray",
                                         font=('Segoe UI', 12))



    def clear_huffman_tree_display(self):
        self.tree_canvas.delete("all")
        self.tree_image_tk = None





    def on_show(self):
        if self.controller and self.controller.get_original_text():
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", self.controller.get_original_text())
        self.clear_outputs()