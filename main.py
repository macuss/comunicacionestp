import tkinter as tk
from model.huffman import Huffman
from model.shannon_fano import ShannonFano
from model.utils import Utils
from view.main_view import MainView
from controller.main_controller import MainController
import os

if __name__ == "__main__":
    # Crear la carpeta temporal si no existe
    temp_image_dir = "temp_images"
    os.makedirs(temp_image_dir, exist_ok=True)

    root = tk.Tk()

    try:

        current_dir = os.path.dirname(os.path.abspath(__file__))
        azure_theme_path = os.path.join(current_dir, "azure.tcl")


        # Theme Azure: https://github.com/rdbende/Azure-ttk-theme/blob/main/azure.tcl


        root.tk.call("source", azure_theme_path)  # Cargar el archivo TCL
        root.tk.call("set_theme", "light")
    except Exception as e:
        print(f"Advertencia: No se pudo cargar el tema. La interfaz usará el tema por defecto. Error: {e}")




    # modelos
    huffman_model = Huffman()
    shannon_fano_model = ShannonFano()
    utils_model = Utils()

    # vista principal que gestiona las pantallas
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
            if os.path.exists(temp_image_dir) and not os.listdir(temp_image_dir):
                os.rmdir(temp_image_dir)
        except OSError as e:
            print(f"Error al eliminar directorio temporal: {e}")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)





    controller.iniciar_aplicacion()