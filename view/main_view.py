import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk  # pip install Pillow
import os


class MainView:
    def __init__(self, master):
        self.master = master
        master.title("Compresor Huffman y Shannon-Fano")
        master.geometry("1000x800")
        master.resizable(True, True)

        self.controller = None  # Se asignará desde el controlador

        # --- Frames Principales ---
        self.input_frame = ttk.LabelFrame(master, text="Entrada de Texto")
        self.input_frame.pack(side="top", fill="x", padx=10, pady=5)

        self.controls_frame = ttk.Frame(master)
        self.controls_frame.pack(side="top", fill="x", padx=10, pady=5)

        self.results_frame = ttk.LabelFrame(master, text="Resultados de Compresión")
        self.results_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        # --- Entrada de Texto ---
        self.text_input = tk.Text(self.input_frame, wrap="word", height=8, width=80, font=('Consolas', 10))
        self.text_input.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.text_input.insert(tk.END, "Introduce tu texto aquí o carga un archivo.")

        scrollbar_input = ttk.Scrollbar(self.input_frame, command=self.text_input.yview)
        scrollbar_input.pack(side="right", fill="y")
        self.text_input.config(yscrollcommand=scrollbar_input.set)

        # --- Botones de Carga/Guardado ---
        self.load_button = ttk.Button(self.input_frame, text="Cargar Archivo .txt", command=self._load_file)
        self.load_button.pack(side="bottom", fill="x", padx=5, pady=2)

        # --- Controles de Algoritmo ---
        self.algo_selection = tk.StringVar(value="Huffman")  # Valor por defecto
        ttk.Radiobutton(self.controls_frame, text="Huffman", variable=self.algo_selection, value="Huffman").pack(
            side="left", padx=10)
        ttk.Radiobutton(self.controls_frame, text="Shannon-Fano", variable=self.algo_selection,
                        value="Shannon-Fano").pack(side="left", padx=10)

        self.compress_button = ttk.Button(self.controls_frame, text="Comprimir", command=self._compress)
        self.compress_button.pack(side="left", padx=20)

        self.decompress_button = ttk.Button(self.controls_frame, text="Descomprimir", command=self._decompress)
        self.decompress_button.pack(side="left", padx=20)

        self.save_button = ttk.Button(self.controls_frame, text="Guardar Resultados", command=self._save_results)
        self.save_button.pack(side="left", padx=20)

        # --- Resultados (PanedWindow para organizar) ---
        self.paned_window = ttk.PanedWindow(self.results_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=5, pady=5)

        # Panel Izquierdo: Frecuencias, Códigos, Bits, Decodificado
        self.left_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_panel, weight=1)

        self.freq_label = ttk.Label(self.left_panel, text="Frecuencias de Símbolos:")
        self.freq_label.pack(anchor="w", padx=5, pady=2)
        self.freq_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 9))
        self.freq_text.pack(fill="x", padx=5, pady=2)
        self.freq_text.config(state="disabled")

        self.codes_label = ttk.Label(self.left_panel, text="Tabla de Códigos:")
        self.codes_label.pack(anchor="w", padx=5, pady=2)
        self.codes_text = tk.Text(self.left_panel, wrap="word", height=8, font=('Consolas', 9))
        self.codes_text.pack(fill="x", padx=5, pady=2)
        self.codes_text.config(state="disabled")

        self.encoded_label = ttk.Label(self.left_panel, text="Texto Codificado (Bits):")
        self.encoded_label.pack(anchor="w", padx=5, pady=2)
        self.encoded_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 9))
        self.encoded_text.pack(fill="x", padx=5, pady=2)
        self.encoded_text.config(state="disabled")

        self.decoded_label = ttk.Label(self.left_panel, text="Texto Decodificado:")
        self.decoded_label.pack(anchor="w", padx=5, pady=2)
        self.decoded_text = tk.Text(self.left_panel, wrap="word", height=6, font=('Consolas', 9))
        self.decoded_text.pack(fill="x", padx=5, pady=2)
        self.decoded_text.config(state="disabled")

        self.metrics_label = ttk.Label(self.left_panel, text="Métricas:")
        self.metrics_label.pack(anchor="w", padx=5, pady=2)
        self.avg_len_label = ttk.Label(self.left_panel, text="Longitud Promedio: N/A")
        self.avg_len_label.pack(anchor="w", padx=10)
        self.compression_rate_label = ttk.Label(self.left_panel, text="Tasa de Compresión: N/A")
        self.compression_rate_label.pack(anchor="w", padx=10)

        # Panel Derecho: Visualización del Árbol de Huffman
        self.right_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_panel, weight=1)

        self.tree_label_title = ttk.Label(self.right_panel, text="Visualización del Árbol de Huffman:")
        self.tree_label_title.pack(anchor="w", padx=5, pady=2)

        self.tree_canvas = tk.Canvas(self.right_panel, bg="white", borderwidth=2, relief="groove")
        self.tree_canvas.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_image_tk = None  # Para mantener la referencia de la imagen

    def set_controller(self, controller):
        self.controller = controller

    def _load_file(self):
        if self.controller:
            self.controller.cargar_archivo()

    def _compress(self):
        if self.controller:
            self.controller.comprimir_texto()

    def _decompress(self):
        if self.controller:
            self.controller.descomprimir_texto()

    def _save_results(self):
        if self.controller:
            self.controller.guardar_resultados()

    def get_text_input(self):
        return self.text_input.get("1.0", tk.END).strip()

    def get_selected_algorithm(self):
        return self.algo_selection.get()

    def clear_all_outputs(self):
        self.update_text_widget(self.freq_text, "")
        self.update_text_widget(self.codes_text, "")
        self.update_text_widget(self.encoded_text, "")
        self.update_text_widget(self.decoded_text, "")
        self.avg_len_label.config(text="Longitud Promedio: N/A")
        self.compression_rate_label.config(text="Tasa de Compresión: N/A")
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

    def display_metrics(self, avg_len, compression_rate):
        self.avg_len_label.config(text=f"Longitud Promedio: {avg_len:.2f} bits/símbolo")
        self.compression_rate_label.config(text=f"Tasa de Compresión: {compression_rate:.2f}%")

    def display_huffman_tree(self, image_path):
        self.clear_huffman_tree_display()
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                # Escalar la imagen para ajustarse al canvas
                canvas_width = self.tree_canvas.winfo_width()
                canvas_height = self.tree_canvas.winfo_height()

                # Evitar división por cero si el canvas no tiene tamaño todavía
                if canvas_width == 0: canvas_width = 400  # Default para primera carga
                if canvas_height == 0: canvas_height = 400

                img_width, img_height = img.size

                # Calcular el factor de escala manteniendo la proporción
                scale_w = canvas_width / img_width
                scale_h = canvas_height / img_height
                scale_factor = min(scale_w, scale_h)

                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)

                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.tree_image_tk = ImageTk.PhotoImage(img)

                self.tree_canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.tree_image_tk,
                                              anchor="center")
                self.tree_canvas.image = self.tree_image_tk  # Prevenir garbage collection
            except Exception as e:
                messagebox.showerror("Error de Imagen", f"No se pudo cargar la imagen del árbol: {e}")
        else:
            self.tree_canvas.create_text(self.tree_canvas.winfo_width() / 2, self.tree_canvas.winfo_height() / 2,
                                         text="Árbol no disponible o algoritmo no es Huffman.", fill="gray",
                                         font=('Arial', 12))

    def clear_huffman_tree_display(self):
        self.tree_canvas.delete("all")
        self.tree_image_tk = None  # Liberar la referencia a la imagen anterior

    def show_message(self, title, message, type="info"):
        if type == "info":
            messagebox.showinfo(title, message)
        elif type == "error":
            messagebox.showerror(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)