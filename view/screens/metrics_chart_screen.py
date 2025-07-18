import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # pip install matplotlib

class MetricsChartScreen(tk.Frame):
    def __init__(self, parent, view):
        super().__init__(parent)
        self.view = view
        self.controller = None

        self.configure(bg="#F3E5F5")

        # controles
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side="top", fill="x", padx=10, pady=5)
        ttk.Button(control_frame, text="Generar Gráficos", command=self._generate_charts).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Volver al Menú", command=self._go_back).pack(side="right", padx=10)

        # Gráficos
        self.chart_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.ax1 = self.figure.add_subplot(121) # Longitud Promedio
        self.ax2 = self.figure.add_subplot(122) # Tasa de Compresión

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_controller(self, controller):
        self.controller = controller

    def _generate_charts(self):
        if self.controller:
            huffman_metrics = self.controller.get_huffman_metrics()
            shannon_fano_metrics = self.controller.get_shannon_fano_metrics()

            if not huffman_metrics and not shannon_fano_metrics:
                self.view.show_message("Advertencia", "No hay métricas disponibles para graficar. Comprime texto con ambos algoritmos primero.", type="warning")
                return

            self.plot_metrics(huffman_metrics, shannon_fano_metrics)



    def _go_back(self):
        if self.controller:
            self.controller.show_main_menu()

    def plot_metrics(self, huffman_metrics, shannon_fano_metrics):
        self.ax1.clear()
        self.ax2.clear()

        labels = []
        avg_lens = []
        comp_rates = []

        if huffman_metrics and huffman_metrics['avg_len'] is not None:
            labels.append("Huffman")
            avg_lens.append(huffman_metrics['avg_len'])
            comp_rates.append(huffman_metrics['compression_rate'])
        if shannon_fano_metrics and shannon_fano_metrics['avg_len'] is not None:
            labels.append("Shannon-Fano")
            avg_lens.append(shannon_fano_metrics['avg_len'])
            comp_rates.append(shannon_fano_metrics['compression_rate'])

        if not labels:
            self.ax1.text(0.5, 0.5, "No hay datos para graficar", horizontalalignment='center', verticalalignment='center', transform=self.ax1.transAxes)
            self.ax2.text(0.5, 0.5, "No hay datos para graficar", horizontalalignment='center', verticalalignment='center', transform=self.ax2.transAxes)
            self.figure.canvas.draw()
            return

        # Gráfico de Longitud Promedio
        self.ax1.bar(labels, avg_lens, color=['skyblue', 'lightcoral'])
        self.ax1.set_title('Longitud Promedio de Código')
        self.ax1.set_ylabel('Bits/Símbolo')
        for i, v in enumerate(avg_lens):
            self.ax1.text(i, v + 0.1, f"{v:.2f}", ha='center', va='bottom')
        self.ax1.set_ylim(bottom=0) # Asegurar que el eje Y comience en 0

        # Gráfico de Tasa de Compresión
        self.ax2.bar(labels, comp_rates, color=['lightgreen', 'salmon'])
        self.ax2.set_title('Tasa de Compresión (%)')
        self.ax2.set_ylabel('Porcentaje (%)')
        for i, v in enumerate(comp_rates):
            self.ax2.text(i, v + 0.5, f"{v:.2f}%", ha='center', va='bottom')
        self.ax2.set_ylim(0, 100)

        self.figure.tight_layout()
        self.figure.canvas.draw()




    def on_show(self):

        self.ax1.clear()
        self.ax2.clear()
        self.figure.canvas.draw()

        # self._generate_charts()