import tkinter as tk
from model.huffman import Huffman
from model.shannon_fano import ShannonFano


from model.utils import Utils
from view.main_view import MainView
from controller.main_controller import MainController
import os




if __name__ == "__main__":
    temp_image_dir = "temp_images"
    os.makedirs(temp_image_dir, exist_ok=True)

    root = tk.Tk()


    #  modelos
    huffman_model = Huffman()
    shannon_fano_model = ShannonFano()
    utils_model = Utils()



    #  vista
    view = MainView(root)

    # controlador
    controller = MainController(view, huffman_model, shannon_fano_model, utils_model)


    def on_closing():
        image_path = os.path.join(temp_image_dir, "huffman_tree.png")
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError as e:
                print(f"Error al eliminar archivo temporal: {e}")

        try:
            if not os.listdir(temp_image_dir):
                os.rmdir(temp_image_dir)
        except OSError as e:
            print(f"Error al eliminar directorio temporal: {e}")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)






    controller.iniciar_aplicacion()