import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import random
import math


class GeneradorNumerosAleatorios:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Números Aleatorios")
        self.root.geometry("1200x800")
        
        # Variables para almacenar los datos generados
        self.numeros_generados = []
        self.distribucion_actual = tk.StringVar(value="uniforme")
        self.intervalos = tk.IntVar(value=10)
        
        # Crear marco principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo para controles
        panel_izquierdo = ttk.LabelFrame(main_frame, text="Parámetros", padding="10")
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Selección de distribución
        ttk.Label(panel_izquierdo, text="Distribución:").grid(row=0, column=0, sticky=tk.W, pady=5)
        distribuciones = ["uniforme", "exponencial", "normal"]
        distribucion_combo = ttk.Combobox(panel_izquierdo, textvariable=self.distribucion_actual, values=distribuciones, state="readonly")
        distribucion_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        distribucion_combo.bind("<<ComboboxSelected>>", self.actualizar_parametros)
        
        # Tamaño de muestra
        ttk.Label(panel_izquierdo, text="Tamaño de muestra:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tamano_muestra = ttk.Entry(panel_izquierdo)
        self.tamano_muestra.insert(0, "1000")
        self.tamano_muestra.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Frame para parámetros específicos de cada distribución
        self.params_frame = ttk.LabelFrame(panel_izquierdo, text="Parámetros específicos", padding="10")
        self.params_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Parámetros para uniforme (valores iniciales)
        self.param_a = ttk.Entry(self.params_frame)
        self.param_a.insert(0, "0")
        self.param_b = ttk.Entry(self.params_frame)
        self.param_b.insert(0, "1")
        
        # Parámetros para exponencial
        self.param_lambda = ttk.Entry(self.params_frame)
        self.param_lambda.insert(0, "1")
        
        # Parámetros para normal
        self.param_mu = ttk.Entry(self.params_frame)
        self.param_mu.insert(0, "0")
        self.param_sigma = ttk.Entry(self.params_frame)
        self.param_sigma.insert(0, "1")
        
        # Inicialmente mostrar parámetros de uniforme
        self.mostrar_params_uniforme()
        
        # Número de intervalos para el histograma
        ttk.Label(panel_izquierdo, text="Intervalos:").grid(row=3, column=0, sticky=tk.W, pady=5)
        intervalos_opciones = [10, 15, 20, 30]
        intervalos_combo = ttk.Combobox(panel_izquierdo, textvariable=self.intervalos, values=intervalos_opciones, state="readonly")
        intervalos_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Botón para generar números
        generar_btn = ttk.Button(panel_izquierdo, text="Generar Números", command=self.generar_numeros)
        generar_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Panel derecho para visualización
        panel_derecho = ttk.Frame(main_frame)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área para mostrar números generados
        ttk.Label(panel_derecho, text="Números Generados (primeros 100):").pack(anchor=tk.W, pady=5)
        self.numeros_text = scrolledtext.ScrolledText(panel_derecho, width=40, height=10)
        self.numeros_text.pack(fill=tk.X, pady=5)
        
        # Área para el histograma
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=panel_derecho)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área para la tabla de frecuencias
        ttk.Label(panel_derecho, text="Tabla de Frecuencias:").pack(anchor=tk.W, pady=5)
        self.tabla_frame = ttk.Frame(panel_derecho)
        self.tabla_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def mostrar_params_uniforme(self):
        # Limpiar frame de parámetros
        for widget in self.params_frame.winfo_children():
            widget.grid_forget()
        
        ttk.Label(self.params_frame, text="a (mínimo):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.param_a.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(self.params_frame, text="b (máximo):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.param_b.grid(row=1, column=1, sticky=tk.W, pady=5)
    
    def mostrar_params_exponencial(self):
        # Limpiar frame de parámetros
        for widget in self.params_frame.winfo_children():
            widget.grid_forget()
        
        ttk.Label(self.params_frame, text="λ (lambda):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.param_lambda.grid(row=0, column=1, sticky=tk.W, pady=5)
    
    def mostrar_params_normal(self):
        # Limpiar frame de parámetros
        for widget in self.params_frame.winfo_children():
            widget.grid_forget()
        
        ttk.Label(self.params_frame, text="μ (media):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.param_mu.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Label(self.params_frame, text="σ (desviación):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.param_sigma.grid(row=1, column=1, sticky=tk.W, pady=5)
    
    def actualizar_parametros(self, event=None):
        distribucion = self.distribucion_actual.get()
        if distribucion == "uniforme":
            self.mostrar_params_uniforme()
        elif distribucion == "exponencial":
            self.mostrar_params_exponencial()
        elif distribucion == "normal":
            self.mostrar_params_normal()
    
    def generar_numeros(self):
        try:
            n = min(int(self.tamano_muestra.get()), 1000000)
            distribucion = self.distribucion_actual.get()
            
            if distribucion == "uniforme":
                a = float(self.param_a.get())
                b = float(self.param_b.get())
                if a >= b:
                    raise ValueError("El valor de 'a' debe ser menor que 'b'")
                self.numeros_generados = self.uniforme(a, b, n)
                titulo = f"Distribución Uniforme [{a}, {b})"
            
            elif distribucion == "exponencial":
                lambda_val = float(self.param_lambda.get())
                if lambda_val <= 0:
                    raise ValueError("Lambda debe ser mayor que 0")
                self.numeros_generados = self.exponencial(lambda_val, n)
                titulo = f"Distribución Exponencial [λ={lambda_val}]"
            
            elif distribucion == "normal":
                mu = float(self.param_mu.get())
                sigma = float(self.param_sigma.get())
                if sigma <= 0:
                    raise ValueError("Sigma debe ser mayor que 0")
                self.numeros_generados = self.normal_box_muller(mu, sigma, n)
                titulo = f"Distribución Normal [μ={mu}, σ={sigma}]"
            
            self.numeros_generados = np.round(self.numeros_generados, 4)
            
            self.numeros_text.delete(1.0, tk.END)
            numeros_mostrar = self.numeros_generados[:100]
            texto_numeros = ", ".join([str(num) for num in numeros_mostrar])
            if n > 100:
                texto_numeros += "... (y " + str(n - 100) + " más)"
            self.numeros_text.insert(tk.END, texto_numeros)
            
            self.generar_histograma(titulo, distribucion, a if distribucion == "uniforme" else None, 
                                   b if distribucion == "uniforme" else None)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def uniforme(self, a, b, n):
        return [a + (b - a) * random.random() for _ in range(n)]

    def exponencial(self, lambda_val, n):
        return [-(1 / lambda_val) * math.log(1 - random.random()) for _ in range(n)]

    def normal_box_muller(self, mu, sigma, n):
        numeros = []
        for _ in range(n // 2):
            u1, u2 = random.random(), random.random()
            z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            numeros.append(mu + sigma * z1)
            numeros.append(mu + sigma * z2)
        if len(numeros) < n:
            u1, u2 = random.random(), random.random()
            z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            numeros.append(mu + sigma * z1)
        return numeros
    
    def generar_histograma(self, titulo, distribucion, a=None, b=None):
        # Limpiar gráfico anterior
        self.ax.clear()
        
        # Obtener número de intervalos
        n_bins = self.intervalos.get()
        
        # Calcular límites de los intervalos según la distribución
        if distribucion == "uniforme":
            # Para distribución uniforme, respetamos exactamente los límites a y b
            bins = np.linspace(a, b, n_bins + 1)
        elif distribucion == "exponencial":
            # Para exponencial, tomamos el parámetro lambda
            lambda_val = float(self.param_lambda.get())
            # El mínimo es siempre 0 para exponencial
            min_val = 0
            # El máximo podemos calcularlo para cubrir un porcentaje alto de la distribución
            # Por ejemplo, para cubrir aprox. el 99% de los valores
            max_val = np.percentile(self.numeros_generados, 99.5)
            bins = np.linspace(min_val, max_val, n_bins + 1)
        elif distribucion == "normal":
            # Para normal, usamos los parámetros mu y sigma
            mu = float(self.param_mu.get())
            sigma = float(self.param_sigma.get())
            # Definimos límites a ±4 sigmas desde la media para cubrir ~99.99% de los datos
            min_val = mu - 4 * sigma
            max_val = mu + 4 * sigma
            bins = np.linspace(min_val, max_val, n_bins + 1)
        
        # Crear histograma con límites explícitos
        counts, bins, patches = self.ax.hist(self.numeros_generados, bins=bins, edgecolor='black', alpha=0.7, rwidth=0.9)
        
        # Configurar el gráfico
        self.ax.set_title(titulo)
        self.ax.set_xlabel("Valor")
        self.ax.set_ylabel("Frecuencia")
        
        # Mejorar la visualización de los límites en el eje x
        # Mostrar todos los límites de los intervalos
        self.ax.set_xticks(bins)
        # Formatear etiquetas
        self.ax.set_xticklabels([f"{b:.4f}" for b in bins], rotation=45)
        
        # Añadir líneas verticales para cada límite de intervalo
        for bin_edge in bins:
            self.ax.axvline(x=bin_edge, color='gray', linestyle='--', alpha=0.5)
        
        # Añadir anotaciones para mostrar claramente cada intervalo
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        for i in range(len(bin_centers)):
            # Formato del intervalo según la distribución
            intervalo_texto = f"[{bins[i]:.2f}, {bins[i+1]:.2f})"
            self.ax.annotate(intervalo_texto,
                           xy=(bin_centers[i], max(counts)/2 if len(counts) > 0 and max(counts) > 0 else 1),
                           ha='center', va='center',
                           rotation=90, color='blue', alpha=0.5)
        
        # Añadir grid
        self.ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.7)
        
        # Ajustar diseño para evitar cortar etiquetas
        plt.tight_layout()
        
        # Actualizar canvas
        self.canvas.draw()
        
        # Generar y mostrar tabla de frecuencias
        self.mostrar_tabla_frecuencias(counts, bins, distribucion)
    
    def mostrar_tabla_frecuencias(self, counts, bins, distribucion):
        # Limpiar tabla anterior
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()
        
        # Crear tabla de frecuencias
        columns = ("Intervalo", "Límite Inferior", "Límite Superior", "Frecuencia", "Frecuencia Relativa")
        tabla = ttk.Treeview(self.tabla_frame, columns=columns, show='headings')
        
        # Configurar encabezados
        for col in columns:
            tabla.heading(col, text=col)
            tabla.column(col, width=120, anchor=tk.CENTER)
        
        # Insertar datos
        total = sum(counts)
        for i in range(len(counts)):
            intervalo = f"Intervalo {i+1}"
            lim_inf = round(bins[i], 4)
            lim_sup = round(bins[i+1], 4)
            
            # Formato especial para distribución uniforme para enfatizar intervalos semi-abiertos
            if distribucion == "uniforme":
                rango_intervalo = f"[{lim_inf}, {lim_sup})"
            else:
                rango_intervalo = f"[{lim_inf}, {lim_sup}]"
                
            frecuencia = int(counts[i])
            frec_relativa = round(counts[i] / total, 4)
            
            tabla.insert('', tk.END, values=(intervalo, lim_inf, lim_sup, frecuencia, frec_relativa))
        
        # Añadir una nota explicativa para distribución uniforme
        if distribucion == "uniforme":
            nota_frame = ttk.Frame(self.tabla_frame)
            nota_frame.pack(fill=tk.X, pady=5)
            nota_label = ttk.Label(nota_frame, text="Nota: Los intervalos son semi-abiertos [a, b) donde el límite inferior se incluye pero el superior no.")
            nota_label.pack(anchor=tk.W)
        
        # Añadir barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.tabla_frame, orient=tk.VERTICAL, command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y barra de desplazamiento
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tabla.pack(expand=True, fill=tk.BOTH)

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorNumerosAleatorios(root)
    root.mainloop()