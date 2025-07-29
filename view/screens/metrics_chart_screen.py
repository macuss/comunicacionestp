import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MetricsChartScreen(tk.Frame):
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


        s.configure('Chart.TFrame',
                    background='#ffffff',
                    relief='flat',
                    borderwidth=1,
                    bordercolor='#cccccc'
                   )

        # Controles
        control_frame = ttk.Frame(self, padding="10 10 10 10", style='TFrame')
        control_frame.pack(side="top", fill="x", padx=20, pady=10)
        ttk.Button(control_frame, text="Generar Gráficos", command=self._generate_charts, style='Action.TButton').pack(side="left", padx=10)
        ttk.Button(control_frame, text="Volver al Menú", command=self._go_back, style='Neutral.TButton').pack(side="right", padx=10)

        # Gráficos
        self.chart_frame = ttk.Frame(self, style='Chart.TFrame') # Aplicar el estilo al chart_frame
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)


        self.figure = plt.Figure(figsize=(10, 6), dpi=100, facecolor=self.background_color)
        self.ax1 = self.figure.add_subplot(121)
        self.ax2 = self.figure.add_subplot(122)


        self._configure_axes_style(self.ax1)
        self._configure_axes_style(self.ax2)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)




    def _configure_axes_style(self, ax):

        ax.set_facecolor('#ffffff')
        ax.tick_params(axis='x', colors=self.text_color_dark)
        ax.tick_params(axis='y', colors=self.text_color_dark)
        ax.spines['bottom'].set_color(self.text_color_dark)
        ax.spines['top'].set_color(self.text_color_dark)
        ax.spines['right'].set_color(self.text_color_dark)
        ax.spines['left'].set_color(self.text_color_dark)
        ax.xaxis.label.set_color(self.text_color_dark)
        ax.yaxis.label.set_color(self.text_color_dark)
        ax.title.set_color(self.text_color_dark)
        plt.setp(ax.get_xticklabels(), fontname="Segoe UI")
        plt.setp(ax.get_yticklabels(), fontname="Segoe UI")
        ax.title.set_fontname("Segoe UI")
        ax.xaxis.label.set_fontname("Segoe UI")
        ax.yaxis.label.set_fontname("Segoe UI")


    def set_controller(self, controller):
        self.controller = controller



    def _generate_charts(self):
        if self.controller:
            huffman_metrics = self.controller.get_huffman_metrics()
            shannon_fano_metrics = self.controller.get_shannon_fano_metrics()

            if (not huffman_metrics or huffman_metrics['avg_len'] is None) and \
               (not shannon_fano_metrics or shannon_fano_metrics['avg_len'] is None):
                self.view.show_message("Advertencia", "No hay métricas disponibles para graficar. Comprime texto con ambos algoritmos primero.", type="warning")
                self.ax1.clear()
                self.ax2.clear()
                self.ax1.text(0.5, 0.5, "No hay datos para graficar", horizontalalignment='center', verticalalignment='center', transform=self.ax1.transAxes, color=self.text_color_dark, fontname="Segoe UI")
                self.ax2.text(0.5, 0.5, "No hay datos para graficar", horizontalalignment='center', verticalalignment='center', transform=self.ax2.transAxes, color=self.text_color_dark, fontname="Segoe UI")
                self.figure.canvas.draw()
                return

            self.plot_metrics(huffman_metrics, shannon_fano_metrics)

    def _go_back(self):
        if self.controller:
            self.controller.show_main_menu()

    def plot_metrics(self, huffman_metrics, shannon_fano_metrics):
        self.ax1.clear()
        self.ax2.clear()


        self._configure_axes_style(self.ax1)
        self._configure_axes_style(self.ax2)

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
            self.ax1.text(0.5, 0.5, "No hay datos para graficar", horizontalalignment='center', verticalalignment='center', transform=self.ax1.transAxes, color=self.text_color_dark, fontname="Segoe UI")
            self.ax2.text(0.5, 0.5, "No hay datos para graficar", horizontalalignment='center', verticalalignment='center', transform=self.ax2.transAxes, color=self.text_color_dark, fontname="Segoe UI")
            self.figure.canvas.draw()
            return


        bar_colors_avg_len = [self.primary_color, self.accent_color]
        bar_colors_comp_rate = [self.secondary_color, self.primary_color]

        # longitud Promedio
        bars1 = self.ax1.bar(labels, avg_lens, color=bar_colors_avg_len)
        self.ax1.set_title('Longitud Promedio de Código', fontsize=14, fontname="Segoe UI")
        self.ax1.set_ylabel('Bits/Símbolo', fontsize=12, fontname="Segoe UI")
        for bar in bars1:
            yval = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval:.2f}", ha='center', va='bottom', color=self.text_color_dark, fontname="Segoe UI")
        self.ax1.set_ylim(bottom=0)
        self.ax1.grid(axis='y', linestyle='--', alpha=0.7, color='#e0e0e0') # Rejilla sutil

        # tasa de Compresión
        bars2 = self.ax2.bar(labels, comp_rates, color=bar_colors_comp_rate)
        self.ax2.set_title('Tasa de Compresión (%)', fontsize=14, fontname="Segoe UI")
        self.ax2.set_ylabel('Porcentaje (%)', fontsize=12, fontname="Segoe UI")
        for bar in bars2:
            yval = bar.get_height()
            self.ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval:.2f}%", ha='center', va='bottom', color=self.text_color_dark, fontname="Segoe UI")
        self.ax2.set_ylim(0, 100)
        self.ax2.grid(axis='y', linestyle='--', alpha=0.7, color='#e0e0e0') # Rejilla sutil

        self.figure.tight_layout()
        self.figure.canvas.draw()

    def on_show(self):

        self.ax1.clear()
        self.ax2.clear()
        self._configure_axes_style(self.ax1)
        self._configure_axes_style(self.ax2)
        self.figure.canvas.draw()


        self._generate_charts()