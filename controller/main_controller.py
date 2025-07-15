import os
from tkinter import filedialog, messagebox

#from PIL._tkinter_finder import tk
import tkinter as tk
# clases del modelo
from model.huffman import Huffman
from model.shannon_fano import ShannonFano
from model.utils import Utils


from view.main_view import MainView

class MainController:
    def __init__(self, view: MainView, huffman_model: Huffman, shannon_fano_model: ShannonFano, utils_model: Utils):
        self.view = view
        self.view.set_controller(self) # Asignar este controlador a la vista

        self.huffman_model = huffman_model
        self.shannon_fano_model = shannon_fano_model
        self.utils_model = utils_model

        self.original_text = ""
        self.encoded_bits = ""
        self.codes = {}
        self.huffman_tree_root = None # Para almacenar el árbol de Huffman para decodificación y visualización

        # Asegurarse de que el directorio para imágenes temporales exista
        self.temp_dir = "temp_images"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.huffman_tree_image_path = os.path.join(self.temp_dir, "huffman_tree.png")


    def iniciar_aplicacion(self):
        self.view.master.mainloop()

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.view.text_input.delete("1.0", tk.END)
                    self.view.text_input.insert("1.0", content)
                    self.original_text = content
                    self.view.show_message("Carga Exitosa", f"Archivo '{os.path.basename(file_path)}' cargado correctamente.")
                    self.view.clear_all_outputs()
            except Exception as e:
                self.view.show_message("Error de Carga", f"No se pudo leer el archivo: {e}", type="error")

    def comprimir_texto(self):
        self.original_text = self.view.get_text_input()
        if not self.original_text:
            self.view.show_message("Advertencia", "Por favor, introduce texto para comprimir.", type="warning")
            return

        self.view.clear_all_outputs() # Limpiar resultados anteriores

        selected_algo = self.view.get_selected_algorithm()
        frecuencias = self.utils_model.calcular_frecuencias(self.original_text)
        self.view.display_frequencies(frecuencias)

        if selected_algo == "Huffman":
            if not frecuencias: # Si el texto está vacío después de limpiar espacios
                self.view.show_message("Advertencia", "No hay caracteres válidos para comprimir (texto vacío o solo espacios).", type="warning")
                return

            self.huffman_tree_root = self.huffman_model.construir_arbol_huffman(frecuencias)
            if not self.huffman_tree_root:
                self.view.show_message("Error", "No se pudo construir el árbol de Huffman. ¿Texto vacío?", type="error")
                return

            self.codes = self.huffman_model.generar_codigos_huffman(self.huffman_tree_root)
            self.encoded_bits = self.huffman_model.codificar_huffman(self.original_text, self.codes)






            # árbol Huffman ---------------------------------
            generated_image_path = self.huffman_model.generar_arbol_graphviz(self.huffman_tree_root, self.huffman_tree_image_path)
            self.view.display_huffman_tree(generated_image_path)

        elif selected_algo == "Shannon-Fano":
            if not frecuencias:
                self.view.show_message("Advertencia", "No hay caracteres válidos para comprimir (texto vacío o solo espacios).", type="warning")
                return

            self.codes = self.shannon_fano_model.generar_codigos_shannon_fano(frecuencias)
            self.encoded_bits = self.shannon_fano_model.codificar_shannon_fano(self.original_text, self.codes)
            self.view.clear_huffman_tree_display() # Limpiar si era Huffman antes

        self.view.display_codes(self.codes)
        self.view.display_encoded_text(self.encoded_bits)







        # Calcular y mostrar métricas ----------------------------------------------------------------------
        avg_len = self.utils_model.calcular_longitud_promedio(frecuencias, self.codes)
        comp_rate = self.utils_model.calcular_tasa_compresion(self.original_text, self.encoded_bits)
        self.view.display_metrics(avg_len, comp_rate)
        self.view.show_message("Compresión Exitosa", f"Texto comprimido con {selected_algo}.")

    def descomprimir_texto(self):
        if not self.encoded_bits or not self.codes:
            self.view.show_message("Advertencia", "Primero comprime un texto para poder decodificarlo.", type="warning")
            return

        selected_algo = self.view.get_selected_algorithm()
        decoded_text = ""

        try:
            if selected_algo == "Huffman":
                if not self.huffman_tree_root:
                    self.view.show_message("Error", "No hay un árbol de Huffman para decodificar. Comprime primero.", type="error")
                    return
                decoded_text = self.huffman_model.decodificar_huffman(self.encoded_bits, self.huffman_tree_root)
            elif selected_algo == "Shannon-Fano":
                decoded_text = self.shannon_fano_model.decodificar_shannon_fano(self.encoded_bits, self.codes)

            self.view.display_decoded_text(decoded_text)
            if decoded_text == self.original_text:
                self.view.show_message("Descompresión Exitosa", "El texto ha sido decodificado correctamente.")
            else:
                self.view.show_message("Descompresión Completa", "Texto decodificado, pero difiere del original. (Revisar si hay caracteres no soportados, ej. emojis)", type="warning")

        except Exception as e:
            self.view.show_message("Error de Descompresión", f"Ocurrió un error al decodificar: {e}", type="error")









    def guardar_resultados(self):
        if not self.original_text:
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
                    f.write(self.original_text + "\n\n")
                    f.write(f"--- Algoritmo Utilizado: {self.view.get_selected_algorithm()} ---\n\n")
                    f.write(f"--- Texto Codificado (Bits) ---\n")
                    f.write(self.encoded_bits + "\n\n")
                    f.write(f"--- Tabla de Códigos ---\n")
                    for char, code in self.codes.items():
                        f.write(f"'{char}': {code}\n")
                    f.write("\n")
                    f.write(f"--- Métricas ---\n")
                    f.write(f"{self.view.avg_len_label.cget('text')}\n")
                    f.write(f"{self.view.compression_rate_label.cget('text')}\n")

                self.view.show_message("Guardado Exitoso", f"Resultados guardados en '{os.path.basename(file_path)}'.")
            except Exception as e:
                self.view.show_message("Error al Guardar", f"No se pudieron guardar los resultados: {e}", type="error")