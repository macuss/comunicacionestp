import os
import tkinter as tk # Importar tkinter como tk para tk.END
from tkinter import filedialog, messagebox

# Importar clases del modelo
from model.huffman import Huffman
from model.shannon_fano import ShannonFano
from model.utils import Utils

# Importar la vista principal
from view.main_view import MainView

class MainController:
    def __init__(self, view: MainView, huffman_model: Huffman, shannon_fano_model: ShannonFano, utils_model: Utils):
        self.view = view
        self.view.set_controller(self)

        self.huffman_model = huffman_model
        self.shannon_fano_model = shannon_fano_model
        self.utils_model = utils_model

        # variables de estado del controlador
        self._original_text = ""
        self._last_algorithm_used = "N/A"
        self._encoded_bits = ""
        self._decoded_text = ""
        self._codes = {}
        self._frequencies = {}
        self._huffman_tree_root = None # Para almacenar el árbol de Huffman
        self._avg_len = None
        self._compression_rate = None

        # métricas específicas para cada algoritmo (para la pantalla de gráficos)
        self._huffman_metrics = {'avg_len': None, 'compression_rate': None}
        self._shannon_fano_metrics = {'avg_len': None, 'compression_rate': None}


        # que el directorio para imágenes temporales exista
        self.temp_dir = "temp_images"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.huffman_tree_image_path = os.path.join(self.temp_dir, "huffman_tree.png")

    def iniciar_aplicacion(self):

        self.view.master.mainloop()




    # --- Métodos para cambiar de pantalla ---
    def show_main_menu(self):
        self.view.show_screen("main_menu")

    def show_huffman_screen(self):
        self.view.show_screen("huffman")

    def show_shannon_fano_screen(self):
        self.view.show_screen("shannon_fano")

    def show_results_screen(self):
        self.view.show_screen("results")

    def show_metrics_chart_screen(self):
        self.view.show_screen("metrics_chart")

    def on_screen_shown(self, screen_name):
        screen_instance = self.view.get_screen(screen_name)
        if hasattr(screen_instance, 'on_show'):
            screen_instance.on_show()




    # getters y setters para el estado global ---/////////////
    def set_original_text(self, text):
        self._original_text = text

    def get_original_text(self):
        return self._original_text

    def get_last_algorithm_used(self):
        return self._last_algorithm_used

    def get_encoded_bits(self):
        return self._encoded_bits

    def get_decoded_text(self):
        return self._decoded_text

    def get_codes(self):
        return self._codes

    def get_frequencies(self):
        return self._frequencies

    def get_avg_len(self):
        return self._avg_len

    def get_compression_rate(self):
        return self._compression_rate

    def get_huffman_metrics(self):
        return self._huffman_metrics

    def get_shannon_fano_metrics(self):
        return self._shannon_fano_metrics

    # lógica de Compresión/Descompresión ------------------------------------------
    def compress_text(self, algorithm_name):

        #compresión del texto utilizando el algoritmo seleccionado.
        current_screen = self.view.current_screen # Obtener la pantalla activa

        if not self._original_text:
            self.view.show_message("Advertencia", "Por favor, introduce texto para comprimir.", type="warning")
            return

        self._frequencies = self.utils_model.calcular_frecuencias(self._original_text)
        if not self._frequencies:
            self.view.show_message("Advertencia", "No hay caracteres válidos para comprimir (texto vacío o solo espacios).", type="warning")
            return

        self._last_algorithm_used = algorithm_name
        self._encoded_bits = ""
        self._codes = {}
        self._huffman_tree_root = None
        self._avg_len = None
        self._compression_rate = None

        if algorithm_name == "Huffman":
            self._huffman_tree_root = self.huffman_model.construir_arbol_huffman(self._frequencies)
            if not self._huffman_tree_root:
                self.view.show_message("Error", "No se pudo construir el árbol de Huffman. ¿Texto vacío?", type="error")
                return

            self._codes = self.huffman_model.generar_codigos_huffman(self._huffman_tree_root)
            self._encoded_bits = self.huffman_model.codificar_huffman(self._original_text, self._codes)

            # generar y mostrar el árbol de Huffman en la pantalla de Huffman
            generated_image_path = self.huffman_model.generar_arbol_graphviz(self._huffman_tree_root, self.huffman_tree_image_path)
            if current_screen and hasattr(current_screen, 'display_huffman_tree'):
                current_screen.display_huffman_tree(generated_image_path)

        elif algorithm_name == "Shannon-Fano":
            self._codes = self.shannon_fano_model.generar_codigos_shannon_fano(self._frequencies)
            self._encoded_bits = self.shannon_fano_model.codificar_shannon_fano(self._original_text, self._codes)
            # shannon-Fano no tiene árbol visual, así que se limpia si se estaba mostrando uno
            if current_screen and hasattr(current_screen, 'clear_huffman_tree_display'):
                current_screen.clear_huffman_tree_display()

        # actualizar la pantalla actual con los resultados
        if current_screen:
            if hasattr(current_screen, 'display_frequencies'):
                current_screen.display_frequencies(self._frequencies)
            if hasattr(current_screen, 'display_codes'):
                current_screen.display_codes(self._codes)
            if hasattr(current_screen, 'display_encoded_text'):
                current_screen.display_encoded_text(self._encoded_bits)

        # calcula y almacena las métricas
        if self._codes: # asegurarse de que se hayan generado códigos
            self._avg_len = self.utils_model.calcular_longitud_promedio(self._frequencies, self._codes)
            self._compression_rate = self.utils_model.calcular_tasa_compresion(self._original_text, self._encoded_bits)
        else:
            self._avg_len = 0.0
            self._compression_rate = 0.0


        if algorithm_name == "Huffman":
            self._huffman_metrics['avg_len'] = self._avg_len
            self._huffman_metrics['compression_rate'] = self._compression_rate
        elif algorithm_name == "Shannon-Fano":
            self._shannon_fano_metrics['avg_len'] = self._avg_len
            self._shannon_fano_metrics['compression_rate'] = self._compression_rate

        self.view.show_message("Compresión Exitosa", f"Texto comprimido con {algorithm_name}.")
        self._decoded_text = ""

    def decompress_text(self, algorithm_name):

        if not self._encoded_bits or not self._codes:
            self.view.show_message("Advertencia", "Primero comprime un texto para poder decodificarlo.", type="warning")
            return

        self._decoded_text = ""
        current_screen = self.view.current_screen

        try:
            if algorithm_name == "Huffman":
                if not self._huffman_tree_root:
                    self.view.show_message("Error", "No hay un árbol de Huffman para decodificar. Comprime primero.", type="error")
                    return
                self._decoded_text = self.huffman_model.decodificar_huffman(self._encoded_bits, self._huffman_tree_root)
            elif algorithm_name == "Shannon-Fano":
                self._decoded_text = self.shannon_fano_model.decodificar_shannon_fano(self._encoded_bits, self._codes)

            if current_screen and hasattr(current_screen, 'display_decoded_text'):
                current_screen.display_decoded_text(self._decoded_text)

            if self._decoded_text == self._original_text:
                self.view.show_message("Descompresión Exitosa", "El texto ha sido decodificado correctamente.")
            else:
                self.view.show_message("Descompresión Completa", "Texto decodificado, pero difiere del original. (Revisar si hay caracteres no soportados)", type="warning")

        except Exception as e:
            self.view.show_message("Error de Descompresión", f"Ocurrió un error al decodificar: {e}", type="error")

    def save_results(self):

        if not self._original_text or not self._encoded_bits or not self._codes:
            self.view.show_message("Advertencia", "No hay resultados para guardar. Comprime un texto primero.", type="warning")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"--- Texto Original ---\n")
                    f.write(self._original_text + "\n\n")
                    f.write(f"--- Algoritmo Utilizado: {self._last_algorithm_used} ---\n\n")
                    f.write(f"--- Texto Codificado (Bits) ---\n")
                    f.write(self._encoded_bits + "\n\n")
                    f.write(f"--- Tabla de Códigos ---\n")
                    for char, code in self._codes.items():
                        f.write(f"'{char}': {code}\n")
                    f.write("\n")
                    f.write(f"--- Métricas ---\n")
                    f.write(f"Longitud Promedio: {self._avg_len:.2f} bits/símbolo\n")
                    f.write(f"Tasa de Compresión: {self._compression_rate:.2f}%\n")

                self.view.show_message("Guardado Exitoso", f"Resultados guardados en '{os.path.basename(file_path)}'.")
            except Exception as e:
                self.view.show_message("Error al Guardar", f"No se pudieron guardar los resultados: {e}", type="error")