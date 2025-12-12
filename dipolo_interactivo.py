"""
PROYECTO UNIDAD 5: ELECTROSTÁTICA
Modelado del campo eléctrico con Python - DIPOLO ELÉCTRICO INTERACTIVO

Autor: [LOPEZ BARRERA GUSTAVO ARISTOTELES
        MARTINEZ VALENZUELA FERNANDO
        CARACOSA BIRRUETA SILVER NAIM
        VEGA MENDOZA ALDO SALVADOR]
Grupo: [EQUIPO FISICA]
Fecha: Diciembre 2025

Descripción: Este programa simula el campo eléctrico producido por un dipolo
eléctrico (dos cargas de igual magnitud y signo opuesto). Permite modificar
interactivamente la posición y separación de las cargas usando una interfaz
gráfica moderna con CustomTkinter.
"""

import tkinter as tk
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import matplotlib
matplotlib.use('TkAgg')

# ============================================================================
# CONFIGURACIÓN INICIAL DEL TEMA
# ============================================================================

ctk.set_appearance_mode("dark")  # Modo oscuro por defecto
ctk.set_default_color_theme("blue")  # Tema azul

# ============================================================================
# CLASE PRINCIPAL DEL SIMULADOR
# ============================================================================

class SimuladorCampoElectrico:
    """Clase principal que maneja toda la interfaz y lógica del simulador"""
    
    def __init__(self, ventana_principal):
        """Constructor que inicializa la ventana principal y todos los componentes"""
        
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("SIMULADOR DE CAMPO ELÉCTRICO - DIPOLO")
        self.ventana_principal.geometry("1600x900")
        
        # Personalizar el color de fondo
        self.ventana_principal.configure(fg_color=("#E8EDF2", "#1a1a2e"))
        
        # ============================================================================
        # CONSTANTES Y PARÁMETROS FÍSICOS
        # ============================================================================
        
        # Constante de Coulomb (usamos k = 1 para simplificar)
        self.k = 1.0
        
        # Magnitud de las cargas
        self.q = 1.0
        
        # Posiciones iniciales de las cargas (variables de Tkinter)
        self.x1 = tk.DoubleVar(value=-1.0)
        self.y1 = tk.DoubleVar(value=0.0)
        self.x2 = tk.DoubleVar(value=1.0)
        self.y2 = tk.DoubleVar(value=0.0)
        
        # Parámetros de visualización
        self.rango = 5
        self.resolucion = 20
        
        # Crear malla de puntos
        x = np.linspace(-self.rango, self.rango, self.resolucion)
        y = np.linspace(-self.rango, self.rango, self.resolucion)
        self.X, self.Y = np.meshgrid(x, y)
        
        # Crear la interfaz gráfica
        self.crear_interfaz_usuario()
        
        # Actualizar la primera visualización
        self.actualizar_simulacion()
    
    # ============================================================================
    # FUNCIONES PARA CALCULAR EL CAMPO ELÉCTRICO
    # ============================================================================
    
    def campo_electrico(self, x, y, cargas):
        """
        Calcula el campo eléctrico en los puntos (x, y) debido a un conjunto de cargas.
        
        Parámetros:
        -----------
        x, y : arrays de numpy
            Coordenadas de los puntos donde calcular el campo
        cargas : lista de tuplas
            Cada tupla contiene (carga, pos_x, pos_y)
            
        Retorna:
        --------
        Ex, Ey : arrays de numpy
            Componentes x e y del campo eléctrico
        """
        Ex = np.zeros_like(x)
        Ey = np.zeros_like(y)
        
        for q_i, x_i, y_i in cargas:
            dx = x - x_i
            dy = y - y_i
            r_cuadrado = dx**2 + dy**2 + 1e-10
            r = np.sqrt(r_cuadrado)
            
            Ex += self.k * q_i * dx / (r_cuadrado * r)
            Ey += self.k * q_i * dy / (r_cuadrado * r)
        
        return Ex, Ey
    
    # ============================================================================
    # CREAR INTERFAZ DE USUARIO
    # ============================================================================
    
    def crear_interfaz_usuario(self):
        """Crea todos los controles de la interfaz del simulador"""
        
        # Marco principal transparente
        marco_principal = ctk.CTkFrame(self.ventana_principal, fg_color="transparent")
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ============================================================================
        # HEADER CON TÍTULO Y BOTÓN DE TEMA
        # ============================================================================
        
        header_frame = ctk.CTkFrame(
            marco_principal,
            height=60,
            corner_radius=12,
            fg_color=("#2b5797", "#0f3460")
        )
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        titulo_label = ctk.CTkLabel(
            header_frame,
            text="⚡ SIMULADOR DE CAMPO ELÉCTRICO - DIPOLO",
            font=("Roboto", 22, "bold"),
            text_color=("#ffffff", "#ffffff")
        )
        titulo_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.boton_tema = ctk.CTkButton(
            header_frame,
            text="☀️ Modo Claro",
            width=140,
            height=35,
            corner_radius=8,
            font=("Roboto", 12, "bold"),
            fg_color=("#3a7ebf", "#1f538d"),
            hover_color=("#5a9edf", "#2a6bad"),
            command=self.cambiar_tema
        )
        self.boton_tema.pack(side=tk.RIGHT, padx=20, pady=12)
        
        # ============================================================================
        # CONTENEDOR INFERIOR (PANEL + CANVAS)
        # ============================================================================
        
        contenedor_inferior = ctk.CTkFrame(marco_principal, fg_color="transparent")
        contenedor_inferior.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================================
        # PANEL DE CONTROL (IZQUIERDA)
        # ============================================================================
        
        panel_control = ctk.CTkScrollableFrame(
            contenedor_inferior,
            width=350,
            corner_radius=12,
            fg_color=("#D1DBE6", "#16213e"),
            border_width=2,
            border_color=("#3a7ebf", "#2b5797")
        )
        panel_control.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False)
        
        # Título del panel
        titulo_panel = ctk.CTkLabel(
            panel_control,
            text="💡 Panel de Control",
            font=("Roboto", 18, "bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        titulo_panel.pack(pady=15, padx=10)
        
        # ============================================================================
        # SECCIÓN: CARGA POSITIVA
        # ============================================================================
        
        separador1 = ctk.CTkFrame(panel_control, height=2, fg_color=("#a0aec0", "#34495e"))
        separador1.pack(fill=tk.X, pady=10, padx=15)
        
        label_carga_pos = ctk.CTkLabel(
            panel_control,
            text="🔴 Carga Positiva (+q)",
            font=("Roboto", 14, "bold"),
            text_color=("#c0392b", "#e74c3c")
        )
        label_carga_pos.pack(pady=(10, 5), padx=10)
        
        # Slider X1
        label_x1 = ctk.CTkLabel(
            panel_control,
            text="Posición X₁:",
            font=("Roboto", 12),
            text_color=("#2c3e50", "#e0e0e0")
        )
        label_x1.pack(pady=(10, 2), padx=10)
        
        marco_slider_x1 = ctk.CTkFrame(panel_control, fg_color=("#D1DBE6", "#16213e"))
        marco_slider_x1.pack(fill=tk.X, padx=15, pady=5)
        
        self.slider_x1 = ctk.CTkSlider(
            marco_slider_x1,
            from_=-4.5,
            to=4.5,
            variable=self.x1,
            orientation="horizontal",
            command=lambda x: self.actualizar_simulacion(),
            button_color=("#e74c3c", "#c0392b"),
            button_hover_color=("#ff6b6b", "#e74c3c"),
            progress_color=("#ff8a80", "#c0392b"),
            fg_color=("#b8c5d6", "#2c3e50"),
            width=200
        )
        self.slider_x1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        self.etiqueta_x1 = ctk.CTkLabel(
            marco_slider_x1,
            text="-1.0",
            font=("Roboto", 13, "bold"),
            width=60,
            fg_color=("#e74c3c", "#c0392b"),
            corner_radius=6,
            text_color=("#ffffff", "#ffffff")
        )
        self.etiqueta_x1.pack(side=tk.LEFT, padx=5)
        
        # Slider Y1
        label_y1 = ctk.CTkLabel(
            panel_control,
            text="Posición Y₁:",
            font=("Roboto", 12),
            text_color=("#2c3e50", "#e0e0e0")
        )
        label_y1.pack(pady=(10, 2), padx=10)
        
        marco_slider_y1 = ctk.CTkFrame(panel_control, fg_color=("#D1DBE6", "#16213e"))
        marco_slider_y1.pack(fill=tk.X, padx=15, pady=5)
        
        self.slider_y1 = ctk.CTkSlider(
            marco_slider_y1,
            from_=-4.5,
            to=4.5,
            variable=self.y1,
            orientation="horizontal",
            command=lambda x: self.actualizar_simulacion(),
            button_color=("#e74c3c", "#c0392b"),
            button_hover_color=("#ff6b6b", "#e74c3c"),
            progress_color=("#ff8a80", "#c0392b"),
            fg_color=("#b8c5d6", "#2c3e50"),
            width=200
        )
        self.slider_y1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        self.etiqueta_y1 = ctk.CTkLabel(
            marco_slider_y1,
            text="0.0",
            font=("Roboto", 13, "bold"),
            width=60,
            fg_color=("#e74c3c", "#c0392b"),
            corner_radius=6,
            text_color=("#ffffff", "#ffffff")
        )
        self.etiqueta_y1.pack(side=tk.LEFT, padx=5)
        
        # ============================================================================
        # SECCIÓN: CARGA NEGATIVA
        # ============================================================================
        
        separador2 = ctk.CTkFrame(panel_control, height=2, fg_color=("#a0aec0", "#34495e"))
        separador2.pack(fill=tk.X, pady=15, padx=15)
        
        label_carga_neg = ctk.CTkLabel(
            panel_control,
            text="🔵 Carga Negativa (−q)",
            font=("Roboto", 14, "bold"),
            text_color=("#2980b9", "#3498db")
        )
        label_carga_neg.pack(pady=(10, 5), padx=10)
        
        # Slider X2
        label_x2 = ctk.CTkLabel(
            panel_control,
            text="Posición X₂:",
            font=("Roboto", 12),
            text_color=("#2c3e50", "#e0e0e0")
        )
        label_x2.pack(pady=(10, 2), padx=10)
        
        marco_slider_x2 = ctk.CTkFrame(panel_control, fg_color=("#D1DBE6", "#16213e"))
        marco_slider_x2.pack(fill=tk.X, padx=15, pady=5)
        
        self.slider_x2 = ctk.CTkSlider(
            marco_slider_x2,
            from_=-4.5,
            to=4.5,
            variable=self.x2,
            orientation="horizontal",
            command=lambda x: self.actualizar_simulacion(),
            button_color=("#3498db", "#2980b9"),
            button_hover_color=("#5dade2", "#3498db"),
            progress_color=("#85c1e9", "#2980b9"),
            fg_color=("#b8c5d6", "#2c3e50"),
            width=200
        )
        self.slider_x2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        self.etiqueta_x2 = ctk.CTkLabel(
            marco_slider_x2,
            text="1.0",
            font=("Roboto", 13, "bold"),
            width=60,
            fg_color=("#3498db", "#2980b9"),
            corner_radius=6,
            text_color=("#ffffff", "#ffffff")
        )
        self.etiqueta_x2.pack(side=tk.LEFT, padx=5)
        
        # Slider Y2
        label_y2 = ctk.CTkLabel(
            panel_control,
            text="Posición Y₂:",
            font=("Roboto", 12),
            text_color=("#2c3e50", "#e0e0e0")
        )
        label_y2.pack(pady=(10, 2), padx=10)
        
        marco_slider_y2 = ctk.CTkFrame(panel_control, fg_color=("#D1DBE6", "#16213e"))
        marco_slider_y2.pack(fill=tk.X, padx=15, pady=5)
        
        self.slider_y2 = ctk.CTkSlider(
            marco_slider_y2,
            from_=-4.5,
            to=4.5,
            variable=self.y2,
            orientation="horizontal",
            command=lambda x: self.actualizar_simulacion(),
            button_color=("#3498db", "#2980b9"),
            button_hover_color=("#5dade2", "#3498db"),
            progress_color=("#85c1e9", "#2980b9"),
            fg_color=("#b8c5d6", "#2c3e50"),
            width=200
        )
        self.slider_y2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        self.etiqueta_y2 = ctk.CTkLabel(
            marco_slider_y2,
            text="0.0",
            font=("Roboto", 13, "bold"),
            width=60,
            fg_color=("#3498db", "#2980b9"),
            corner_radius=6,
            text_color=("#ffffff", "#ffffff")
        )
        self.etiqueta_y2.pack(side=tk.LEFT, padx=5)
        
        # ============================================================================
        # SECCIÓN: INFORMACIÓN
        # ============================================================================
        
        separador3 = ctk.CTkFrame(panel_control, height=2, fg_color=("#a0aec0", "#34495e"))
        separador3.pack(fill=tk.X, pady=15, padx=15)
        
        label_info = ctk.CTkLabel(
            panel_control,
            text="📊 Información",
            font=("Roboto", 14, "bold"),
            text_color=("#16a085", "#1abc9c")
        )
        label_info.pack(pady=(10, 5), padx=10)
        
        self.info_separacion = ctk.CTkLabel(
            panel_control,
            text="Separación: 2.00 m",
            font=("Roboto", 11),
            text_color=("#34495e", "#bdc3c7")
        )
        self.info_separacion.pack(pady=3, padx=10)
        
        # Mostrar valores de las cargas
        self.info_cargas = ctk.CTkLabel(
            panel_control,
            text=f"q₊ = +{self.q:.2f} C\nq₋ = −{self.q:.2f} C",
            font=("Roboto", 12, "bold"),
            text_color=("#8e44ad", "#9b59b6")
        )
        self.info_cargas.pack(pady=3, padx=10)
        
        self.info_constante = ctk.CTkLabel(
            panel_control,
            text=f"k = {self.k:.2f} N·m²/C²",
            font=("Roboto", 11),
            text_color=("#34495e", "#bdc3c7")
        )
        self.info_constante.pack(pady=3, padx=10)
        
        # Información física
        marco_info = ctk.CTkFrame(
            panel_control,
            corner_radius=10,
            fg_color=("#e8f0f7", "#1a2332"),
            border_width=2,
            border_color=("#16a085", "#1abc9c")
        )
        marco_info.pack(fill=tk.X, padx=15, pady=10)
        
        info_texto = ctk.CTkLabel(
            marco_info,
            text="💡 Características del Campo:\n\n"
                 "• El campo es más intenso\n  cerca de las cargas\n\n"
                 "• Las líneas de campo\n  salen de (+) y entran a (−)\n\n"
                 "• El color indica la\n  magnitud del campo\n\n"
                 "• Nunca se cruzan entre sí",
            font=("Roboto", 10),
            text_color=("#2c3e50", "#ecf0f1"),
            justify=tk.LEFT
        )
        info_texto.pack(pady=15, padx=15)
        
        # ============================================================================
        # CANVAS PARA MATPLOTLIB (DERECHA)
        # ============================================================================
        
        marco_canvas = ctk.CTkFrame(
            contenedor_inferior,
            corner_radius=12,
            fg_color=("#f7f9fc", "#0d1117"),
            border_width=2,
            border_color=("#3a7ebf", "#2b5797")
        )
        marco_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 8), facecolor='#2c3e50')
        self.ax.set_facecolor('#34495e')
        
        # Integrar matplotlib en tkinter
        self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=marco_canvas)
        self.canvas_mpl.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # ============================================================================
    # FUNCIÓN PARA CAMBIAR TEMA
    # ============================================================================
    
    def cambiar_tema(self):
        """Alterna entre modo oscuro y claro"""
        modo_actual = ctk.get_appearance_mode()
        if modo_actual == "Dark":
            ctk.set_appearance_mode("light")
            self.boton_tema.configure(text="🌙 Modo Oscuro")
        else:
            ctk.set_appearance_mode("dark")
            self.boton_tema.configure(text="☀️ Modo Claro")
    
    # ============================================================================
    # FUNCIÓN PARA ACTUALIZAR LA SIMULACIÓN
    # ============================================================================
    
    def actualizar_simulacion(self):
        """Recalcula y redibuja el campo eléctrico"""
        
        # Obtener valores actuales
        x1_val = self.x1.get()
        y1_val = self.y1.get()
        x2_val = self.x2.get()
        y2_val = self.y2.get()
        
        # Actualizar etiquetas
        self.etiqueta_x1.configure(text=f"{x1_val:.1f}")
        self.etiqueta_y1.configure(text=f"{y1_val:.1f}")
        self.etiqueta_x2.configure(text=f"{x2_val:.1f}")
        self.etiqueta_y2.configure(text=f"{y2_val:.1f}")
        
        # Calcular separación
        separacion = np.sqrt((x2_val - x1_val)**2 + (y2_val - y1_val)**2)
        self.info_separacion.configure(text=f"Separación: {separacion:.2f} m")
        
        # Definir cargas
        cargas = [
            (self.q, x1_val, y1_val),
            (-self.q, x2_val, y2_val)
        ]
        
        # Calcular campo eléctrico
        Ex, Ey = self.campo_electrico(self.X, self.Y, cargas)
        E_magnitud = np.sqrt(Ex**2 + Ey**2)
        
        # Limpiar el gráfico anterior
        self.ax.clear()
        
        # Mapa de colores
        contour = self.ax.contourf(self.X, self.Y, E_magnitud, levels=20, 
                                    cmap='viridis', alpha=0.7)
        
        # Líneas de campo (flechas)
        E_norm = np.sqrt(Ex**2 + Ey**2 + 1e-10)
        self.ax.quiver(self.X, self.Y, Ex/E_norm, Ey/E_norm, E_magnitud,
                      cmap='plasma', alpha=0.8, scale=25, width=0.004)
        
        # Dibujar cargas
        circulo_pos = Circle((x1_val, y1_val), 0.2, color='red', 
                            ec='white', linewidth=2, zorder=5)
        self.ax.add_patch(circulo_pos)
        self.ax.text(x1_val, y1_val, '+', fontsize=24, color='white',
                    ha='center', va='center', weight='bold', zorder=6)
        
        circulo_neg = Circle((x2_val, y2_val), 0.2, color='blue',
                            ec='white', linewidth=2, zorder=5)
        self.ax.add_patch(circulo_neg)
        self.ax.text(x2_val, y2_val, '−', fontsize=28, color='white',
                    ha='center', va='center', weight='bold', zorder=6)
        
        # Configuración del gráfico
        self.ax.set_xlim(-self.rango, self.rango)
        self.ax.set_ylim(-self.rango, self.rango)
        self.ax.set_xlabel('x (m)', fontsize=12, color='white')
        self.ax.set_ylabel('y (m)', fontsize=12, color='white')
        self.ax.set_title('Campo Eléctrico del Dipolo', 
                         fontsize=14, weight='bold', color='white', pad=20)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3, color='white')
        self.ax.tick_params(colors='white')
        
        # Redibujar canvas
        self.canvas_mpl.draw()


# ============================================================================
# BLOQUE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    ventana = ctk.CTk()
    app = SimuladorCampoElectrico(ventana)
    ventana.mainloop()
