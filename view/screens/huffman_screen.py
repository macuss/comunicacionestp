import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os


class HuffmanScreen(tk.Frame):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.view = view
        self.controller = None

        self.configure(bg="#E0F7FA")




        # --- Frames Principales ----------------------------------------------
        self.input_frame = ttk.LabelFrame(self, text="Entrada de Texto y Controles", padding=10)
        self.input_frame.pack(side="top", fill="x", padx=10, pady=5)

        self.results_frame = ttk.LabelFrame(self, text="Resultados de Huffman", padding=10)
        self.results_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)




        # --- Entrada de Texto -------------------------------------
        self.text_input = tk.Text(self.input_frame, wrap="word", height=8, width=80, font=('Consolas', 10))
        self.text_input.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.text_input.insert(tk.END, "Introduce tu texto aquí o carga un archivo para Huffman.")

        scrollbar_input = ttk.Scrollbar(self.input_frame, command=self.text_input.yview)
        scrollbar_input.pack(side="right", fill="y")
        self.text_input.config(yscrollcommand=scrollbar_input.set)




        # --- Botones de Carga/Acción --------------------------------------------
        s = ttk.Style()
        s.configure('Back.TButton', font=('Inter', 10, 'bold'),
                    background='#6c757d', foreground='white',  # Colores de fondo y texto
                    relief='raised', borderwidth=0, borderradius=5)
        s.map('Back.TButton',
              background=[('active', '#545b62')],  # Color al pasar el ratón
              foreground=[('active', 'white')])

        button_frame = ttk.Frame(self.input_frame)
        button_frame.pack(side="top", padx=5, pady=5)
        ttk.Button(button_frame, text="Cargar Archivo .txt", command=self._load_file).pack(fill="x", pady=2)
        ttk.Button(button_frame, text="Comprimir Huffman", command=self._compress).pack(fill="x", pady=2)
        ttk.Button(button_frame, text="Descomprimir Huffman", command=self._decompress).pack(fill="x", pady=2)
        ttk.Button(button_frame, text="Volver al Menú", command=self._go_back, style='Back.TButton').pack(fill="x", pady=10)





        # resultados (PanedWindow para organizar) ---
        self.paned_window = ttk.PanedWindow(self.results_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=5, pady=5)



        # Panel Izquierdo: frecuencias, códigos, bits, decodificado ---------------------
        self.left_panel = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(self.left_panel, weight=1)

        ttk.Label(self.left_panel, text="Frecuencias de Símbolos:").pack(anchor="w", pady=2)
        self.freq_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 9))
        self.freq_text.pack(fill="x", pady=2)
        self.freq_text.config(state="disabled")

        ttk.Label(self.left_panel, text="Tabla de Códigos Huffman:").pack(anchor="w", pady=2)
        self.codes_text = tk.Text(self.left_panel, wrap="word", height=8, font=('Consolas', 9))
        self.codes_text.pack(fill="x", pady=2)
        self.codes_text.config(state="disabled")

        ttk.Label(self.left_panel, text="Texto Codificado (Bits):").pack(anchor="w", pady=2)
        self.encoded_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 9))
        self.encoded_text.pack(fill="x", pady=2)
        self.encoded_text.config(state="disabled")

        ttk.Label(self.left_panel, text="Texto Decodificado:").pack(anchor="w", pady=2)
        self.decoded_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 9))
        self.decoded_text.pack(fill="x", pady=2)
        self.decoded_text.config(state="disabled")





        # Panel Derecho: Visualización Árbol de Huffman -------------
        self.right_panel = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(self.right_panel, weight=1)

        ttk.Label(self.right_panel, text="Visualización del Árbol de Huffman:").pack(anchor="w", pady=2)

        self.tree_canvas = tk.Canvas(self.right_panel, bg="white", borderwidth=2, relief="groove")
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



# ARBOL
    def display_huffman_tree(self, image_path):
        self.clear_huffman_tree_display()
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                # Escala imagen para ajustarse al canvas
                canvas_width = self.tree_canvas.winfo_width()
                canvas_height = self.tree_canvas.winfo_height()


                if canvas_width == 0: canvas_width = 400
                if canvas_height == 0: canvas_height = 400

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
                                         font=('Arial', 12))





    def clear_huffman_tree_display(self):
        self.tree_canvas.delete("all")
        self.tree_image_tk = None


    def on_show(self):
        if self.controller and self.controller.get_original_text():
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", self.controller.get_original_text())
        self.clear_outputs()