# ⚡ Simulador Interactivo de Campo Eléctrico - Dipolo

## 📋 Datos Generales

**Nombre del estudiante:** [Tu nombre completo aquí]  
**Grupo:** [Tu grupo]  
**Materia:** Física - Electrostática  
**Institución:** [Tu institución]  
**Fecha:** Diciembre 2025

**Título del proyecto:** *Modelado del Campo Eléctrico de un Dipolo con Python - Simulador Interactivo*

---

## 🔬 Descripción Física del Modelo Elegido

### Distribución de Carga Utilizada

Para este proyecto se eligió modelar un **dipolo eléctrico**, que consiste en un sistema de dos cargas puntuales de igual magnitud pero signo opuesto:

- **Carga positiva:** +q (representada en color rojo)
- **Carga negativa:** -q (representada en color azul)

Las cargas están separadas por una distancia variable que puede ser controlada mediante la interfaz gráfica del simulador.

### Justificación de la Elección

El dipolo eléctrico es uno de los sistemas más importantes en electrostática por las siguientes razones:

1. **Relevancia Física:** Los dipolos son fundamentales en la naturaleza. Muchas moléculas (como el agua H₂O) son dipolos permanentes, lo que explica propiedades como la polaridad y las interacciones intermoleculares.

2. **Aplicaciones Prácticas:** 
   - Antenas de radio y telecomunicaciones
   - Análisis de moléculas en química
   - Comprensión de materiales dieléctricos
   - Base para entender momentos dipolares

3. **Complejidad Intermedia:** El dipolo representa un paso natural después de estudiar cargas puntuales individuales, mostrando cómo interactúan sistemas de múltiples cargas.

4. **Simetría Interesante:** El campo eléctrico de un dipolo exhibe patrones de simetría únicos que facilitan su análisis y visualización.

5. **Principio de Superposición:** Permite demostrar claramente cómo el campo eléctrico total es la suma vectorial de los campos individuales de cada carga.

---

## 📐 Modelo Matemático

### Expresión del Campo Eléctrico para una Carga Puntual

El campo eléctrico **E** producido por una carga puntual *q* en un punto del espacio ubicado a una distancia *r* de la carga está dado por la **Ley de Coulomb**:

```
E⃗ = k · q / r² · r̂
```

Donde:
- **k** = Constante de Coulomb = 8.99 × 10⁹ N·m²/C² (en el simulador usamos k = 1 para simplificar)
- **q** = Magnitud de la carga (en Coulombs)
- **r** = Distancia desde la carga hasta el punto de interés
- **r̂** = Vector unitario que apunta desde la carga hacia el punto

En componentes cartesianas (x, y), el campo eléctrico se puede expresar como:

```
Ex = k · q · (x - x₀) / [(x - x₀)² + (y - y₀)²]^(3/2)
Ey = k · q · (y - y₀) / [(x - x₀)² + (y - y₀)²]^(3/2)
```

Donde (x₀, y₀) es la posición de la carga.

### Principio de Superposición

Para calcular el campo eléctrico total producido por **múltiples cargas** (como en el caso del dipolo), aplicamos el **Principio de Superposición**:

> *"El campo eléctrico total en un punto es la suma vectorial de los campos eléctricos producidos por cada carga individual."*

**Proceso de cálculo:**

1. **Para cada carga** en el sistema (en nuestro caso, dos cargas: +q y -q):
   - Calculamos el vector campo eléctrico que esa carga produce en el punto de interés
   - Usamos la fórmula de Coulomb mostrada arriba

2. **Sumamos vectorialmente** todas las contribuciones:
   ```
   E⃗_total = E⃗₁ + E⃗₂ + E⃗₃ + ... + E⃗ₙ
   ```

3. **En componentes:**
   ```
   Ex_total = Ex₁ + Ex₂ + Ex₃ + ... + Exₙ
   Ey_total = Ey₁ + Ey₂ + Ey₃ + ... + Eyₙ
   ```

4. **Magnitud del campo total:**
   ```
   |E⃗_total| = √(Ex_total² + Ey_total²)
   ```

Para el dipolo específicamente, sumamos la contribución de la carga positiva (+q) y la carga negativa (-q) en cada punto del espacio, obteniendo así el patrón característico del campo dipolar.

---

## 💻 Descripción del Código

### Estructura General del Programa

El simulador está desarrollado en Python utilizando las siguientes bibliotecas:

- **CustomTkinter:** Para crear la interfaz gráfica moderna
- **NumPy:** Para cálculos numéricos eficientes
- **Matplotlib:** Para visualización del campo eléctrico
- **Tkinter:** Base para la interfaz gráfica

### Componentes Principales

#### 1. **Definición de las Cargas**

```python
# Magnitud de la carga
self.q = 1.0

# Posiciones de las cargas (controladas por sliders)
self.x1 = tk.DoubleVar(value=-1.0)  # Posición X de carga +
self.y1 = tk.DoubleVar(value=0.0)   # Posición Y de carga +
self.x2 = tk.DoubleVar(value=1.0)   # Posición X de carga -
self.y2 = tk.DoubleVar(value=0.0)   # Posición Y de carga -

# Lista de cargas: (magnitud, x, y)
cargas = [
    (self.q, x1_val, y1_val),   # Carga positiva
    (-self.q, x2_val, y2_val)   # Carga negativa
]
```

#### 2. **Generación de la Malla de Puntos**

Se crea una malla bidimensional de puntos donde se evaluará el campo eléctrico:

```python
# Rango del espacio a visualizar
self.rango = 5  # De -5 a +5 metros en ambos ejes
self.resolucion = 20  # 20 puntos en cada dirección

# Crear malla con numpy
x = np.linspace(-self.rango, self.rango, self.resolucion)
y = np.linspace(-self.rango, self.rango, self.resolucion)
self.X, self.Y = np.meshgrid(x, y)
```

Esto genera una cuadrícula de 20×20 = 400 puntos donde se calculará el campo.

#### 3. **Cálculo del Campo Eléctrico**

La función `campo_electrico()` implementa el principio de superposición:

```python
def campo_electrico(self, x, y, cargas):
    # Inicializar componentes del campo en cero
    Ex = np.zeros_like(x)
    Ey = np.zeros_like(y)
    
    # Para cada carga en el sistema
    for q_i, x_i, y_i in cargas:
        # Vector distancia desde la carga hasta cada punto
        dx = x - x_i
        dy = y - y_i
        
        # Distancia (con epsilon para evitar división por cero)
        r_cuadrado = dx**2 + dy**2 + 1e-10
        r = np.sqrt(r_cuadrado)
        
        # Aplicar Ley de Coulomb y sumar contribución
        Ex += self.k * q_i * dx / (r_cuadrado * r)
        Ey += self.k * q_i * dy / (r_cuadrado * r)
    
    return Ex, Ey
```

#### 4. **Visualización Gráfica**

El campo se visualiza usando dos técnicas complementarias:

**a) Mapa de colores (magnitud):**
```python
E_magnitud = np.sqrt(Ex**2 + Ey**2)
self.ax.contourf(self.X, self.Y, E_magnitud, levels=20, 
                 cmap='viridis', alpha=0.7)
```

**b) Flechas vectoriales (dirección):**
```python
E_norm = np.sqrt(Ex**2 + Ey**2 + 1e-10)
self.ax.quiver(self.X, self.Y, Ex/E_norm, Ey/E_norm, E_magnitud,
               cmap='plasma', alpha=0.8)
```

#### 5. **Interactividad**

Se implementaron **4 sliders** que permiten modificar en tiempo real:
- Posición X₁ de la carga positiva
- Posición Y₁ de la carga positiva
- Posición X₂ de la carga negativa
- Posición Y₂ de la carga negativa

Cada vez que se mueve un slider, se ejecuta `actualizar_simulacion()` que recalcula y redibuja todo el campo eléctrico instantáneamente.

### Flujo de Ejecución

1. Usuario inicia el programa
2. Se crea la interfaz gráfica con CustomTkinter
3. Se calculan las posiciones iniciales del dipolo
4. Se genera la malla de puntos
5. Se calcula el campo eléctrico en cada punto
6. Se visualiza con matplotlib (colores + flechas)
7. Usuario mueve sliders → Se repiten pasos 3-6 en tiempo real

---

## 📊 Resultados y Gráficas

### Figura 1: Dipolo en Configuración Horizontal

![Dipolo Horizontal](figura1_dipolo_horizontal.png)

**Configuración:**
- Carga positiva: (-1.0, 0.0)
- Carga negativa: (+1.0, 0.0)
- Separación: 2.0 metros

**Observaciones:**

1. **Simetría Bilateral:** El campo eléctrico presenta simetría perfecta respecto al eje Y (vertical) que pasa por el punto medio entre las cargas. Esto es característico de un dipolo horizontal.

2. **Intensidad del Campo:**
   - **Regiones de campo intenso (amarillo/verde):** Se concentran alrededor de cada carga, especialmente en las zonas inmediatamente adyacentes
   - **Campo máximo:** La intensidad es máxima en las posiciones de las cargas y disminuye con la distancia según 1/r²
   - **Región central:** Entre las dos cargas existe una zona de campo muy intenso debido a la superposición de ambos campos

3. **Dirección de las Líneas de Campo:**
   - Las flechas muestran que el campo **emerge radialmente** de la carga positiva (roja)
   - Las flechas **convergen radialmente** hacia la carga negativa (azul)
   - En la zona intermedia, el campo apunta horizontalmente de + hacia -
   - Las líneas nunca se cruzan, cumpliendo el principio físico fundamental

4. **Comportamiento Asintótico:** A grandes distancias (esquinas del gráfico), el campo se debilita considerablemente (colores oscuros) y las líneas de campo se vuelven aproximadamente paralelas.

5. **Plano Perpendicular Bisector:** Sobre el eje Y, el campo eléctrico apunta horizontalmente, alejándose del centro hacia los extremos superiores e inferiores.

### Figura 2: Dipolo en Configuración Vertical

![Dipolo Vertical](figura2_dipolo_vertical.png)

**Configuración:**
- Carga positiva: (0.0, -1.5)
- Carga negativa: (0.0, +1.5)
- Separación: 3.0 metros

**Observaciones:**

1. **Rotación de Simetría:** El patrón completo se ha rotado 90° respecto a la Figura 1. Ahora la simetría es respecto al eje X (horizontal).

2. **Mayor Separación:**
   - Al aumentar la distancia entre cargas a 3.0 m (vs 2.0 m anterior), el campo en la región central se "alarga" verticalmente
   - Las zonas de campo intenso cerca de cada carga se mantienen similares
   - La transición entre las influencias de ambas cargas es más gradual

3. **Invariancia de Propiedades:**
   - La magnitud del campo en puntos equidistantes a las cargas es idéntica en ambas configuraciones
   - Solo cambió la orientación espacial, no las propiedades físicas intrínsecas
   - Esto confirma que el dipolo puede existir en cualquier orientación

4. **Patrón Vectorial:** Las flechas ahora apuntan verticalmente en la región central (de arriba hacia abajo), y se curvan hacia los lados en las regiones periféricas.

5. **Verificación del Modelo:** Ambas figuras confirman que el simulador reproduce correctamente el comportamiento teórico esperado para un dipolo eléctrico.

### Comparación Entre Configuraciones

| Aspecto | Horizontal (2.0m) | Vertical (3.0m) |
|---------|-------------------|-----------------|
| Simetría | Respecto eje Y | Respecto eje X |
| Separación | 2.0 metros | 3.0 metros |
| Campo central | Compacto | Alargado |
| Orientación líneas | Horizontal | Vertical |
| Intensidad máxima | Igual | Igual |

Estas visualizaciones demuestran la **flexibilidad del simulador** y validan que el modelo matemático implementado es correcto.

---

## 🎓 Conclusiones

### Aprendizajes Obtenidos

1. **Principio de Superposición en Acción:**
   - Comprobamos experimentalmente que el campo eléctrico total es la suma vectorial de los campos individuales
   - Esta propiedad se manifestó claramente al observar cómo el campo resultante muestra características de ambas cargas

2. **Comportamiento del Campo Eléctrico:**
   - El campo eléctrico disminuye con el cuadrado de la distancia (1/r²), lo cual se observó en el degradado de colores
   - Las líneas de campo siempre salen de cargas positivas y entran a cargas negativas
   - La densidad de líneas de campo es proporcional a la intensidad

3. **Importancia de la Visualización:**
   - Las representaciones gráficas (colores + vectores) permiten comprender intuitivamente conceptos abstractos
   - La combinación de mapas de calor y flechas vectoriales proporciona información completa sobre magnitud y dirección

4. **Programación Científica:**
   - Aprendimos a usar NumPy para cálculos vectoriales eficientes
   - Implementamos visualizaciones científicas con Matplotlib
   - Creamos interfaces gráficas interactivas con CustomTkinter

### Validación Teórica

**¿El comportamiento del campo coincidió con lo esperado teóricamente?**

**Sí, completamente.** El simulador reprodujo fielmente todos los comportamientos teóricos esperados:

✅ **Dirección:** Las líneas de campo van de + a - como predice la teoría  
✅ **Intensidad:** Decae con 1/r² según la Ley de Coulomb  
✅ **Simetría:** El dipolo exhibe simetría bilateral como indica la teoría  
✅ **Superposición:** El campo total es la suma vectorial correcta  
✅ **Continuidad:** No hay discontinuidades ni cruces de líneas de campo  

### Comportamiento del Dipolo Móvil (Puntos Extra)

Gracias a los **sliders interactivos**, pudimos observar en tiempo real cómo cambia el campo eléctrico al modificar las posiciones de las cargas:

#### **1. Al acercar las cargas (separación menor):**
- El campo en la región central se vuelve más intenso y compacto
- Las líneas de campo están más "apretadas" entre las cargas
- A grandes distancias, el dipolo se comporta casi como una carga puntual única
- El patrón se concentra más en el centro

#### **2. Al alejar las cargas (separación mayor):**
- El campo central se "estira" y se vuelve menos intenso
- Las zonas de influencia de cada carga se distinguen mejor
- La región de transición es más amplia y gradual
- El patrón característico del dipolo se hace más evidente

#### **3. Al rotar el dipolo (cambiar orientación):**
- Todo el patrón de campo rota con las cargas
- La simetría se mantiene pero cambia de eje
- Las propiedades físicas son invariantes bajo rotación
- Esto demuestra que la orientación del dipolo determina la dirección del campo resultante

#### **4. Al mover las cargas en direcciones diferentes:**
- Se pueden crear configuraciones asimétricas
- Aunque ya no es estrictamente un dipolo "perfecto", el simulador sigue funcionando
- Esto demuestra la flexibilidad del código basado en el principio de superposición

### Reflexión Final

Este proyecto demostró la potencia de combinar:
- **Física teórica** (Ley de Coulomb, principio de superposición)
- **Matemáticas** (cálculo vectorial, álgebra)
- **Programación** (Python, NumPy, visualización)
- **Diseño de interfaces** (interactividad, usabilidad)

El resultado fue un simulador educativo que no solo calcula correctamente el campo eléctrico, sino que permite **explorar interactivamente** cómo las distribuciones de carga afectan el campo, facilitando una comprensión profunda de los conceptos de electrostática.

La experiencia de ver en tiempo real cómo responde el campo eléctrico a los cambios en las posiciones de las cargas reforzó significativamente nuestra comprensión intuitiva de estos fenómenos físicos fundamentales.

---

## 🚀 Instalación y Uso

### Requisitos

```bash
pip install customtkinter numpy matplotlib
```

### Ejecución

```bash
python dipolo_interactivo.py
```

### Controles

- **Sliders X₁, Y₁:** Controlan la posición de la carga positiva (+q)
- **Sliders X₂, Y₂:** Controlan la posición de la carga negativa (-q)
- **Botón de tema:** Alterna entre modo claro y oscuro
- **Panel de información:** Muestra en tiempo real la separación entre cargas y propiedades físicas

---

## 📚 Referencias

1. Serway, R. A., & Jewett, J. W. (2018). *Physics for Scientists and Engineers*. Cengage Learning.
2. Griffiths, D. J. (2017). *Introduction to Electrodynamics*. Cambridge University Press.
3. Halliday, D., Resnick, R., & Walker, J. (2013). *Fundamentals of Physics*. Wiley.
4. Documentación de NumPy: https://numpy.org/doc/
5. Documentación de Matplotlib: https://matplotlib.org/
6. Documentación de CustomTkinter: https://github.com/TomSchimansky/CustomTkinter

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos para la materia de Electrostática.

---

## 👨‍💻 Autor

**[Tu nombre]**  
[Tu correo electrónico]  
[Tu institución]  
Diciembre 2025
