#!/usr/bin/env python
# coding: utf-8

# In[15]:


import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# SIMULADOR DE TRÁFICO DE DRONES EN CIUDADES INTELIGENTES
# =========================================================


# =========================================================
# INFORMACIÓN INICIAL
# =========================================================

print("===================================================")
print("   SIMULADOR DE TRÁFICO DE DRONES AUTÓNOMOS")
print("===================================================")

print("\nSECTOR ANALIZADO:")
print("Área aproximada: 1 km² de espacio aéreo urbano")

print("\nRANGOS RECOMENDADOS")
print("---------------------------------------------------")
print("Tasa de entrada λ : 1 - 15 drones/minuto")
print("Tasa de salida μ  : 5 - 30 % de drones/minuto")
print("Cantidad inicial  : 0 - 60 drones")
print("Nivel de viento   : 0 - 10")
print("Batería inicial   : 0 - 100 %")
print("Velocidad segura  : 10 - 20 m/s")
print("Riesgo crítico    : > 7")
print("Batería mínima segura : 20 %")
print("---------------------------------------------------")

# =========================================================
# ENTRADAS DEL USUARIO
# =========================================================

tasa_entrada = float(
    input("\nIngrese la tasa de entrada λ (drones/minuto): ")
)

tasa_salida_porcentaje = float(
    input("Ingrese la tasa de salida μ (% de drones que salen por minuto): ")
)

drones_iniciales = float(
    input("Ingrese la cantidad inicial de drones: ")
)

nivel_viento = float(
    input("Ingrese el nivel de viento (0-10): ")
)

bateria_inicial = float(
    input("Ingrese la batería inicial (%): ")
)

# =========================================================
# CONVERSIÓN DE PORCENTAJE A DECIMAL
# =========================================================

# Ejemplo:
# 20% -> 0.20

tasa_salida = tasa_salida_porcentaje / 100

# =========================================================
# PARÁMETROS DEL MODELO
# =========================================================

# Influencia del viento
k = 0.05 + (nivel_viento * 0.01)

# Parámetros del riesgo
alpha = 0.02
beta = 0.1

# Sistema de estabilización automática
gamma = 0.15

# Velocidad ideal del dron
velocidad_objetivo = 15   # m/s

# Tiempo de simulación
tiempo_inicial = 0
tiempo_final = 60      # minutos
dt = 0.1               # minutos

# Vector de tiempo
t = np.arange(tiempo_inicial, tiempo_final, dt)

# =========================================================
# VARIABLES DEL SISTEMA
# =========================================================

N = np.zeros(len(t))   # Número de drones
V = np.zeros(len(t))   # Velocidad promedio
C = np.zeros(len(t))   # Riesgo de colisión
B = np.zeros(len(t))   # Batería

# =========================================================
# CONDICIONES INICIALES
# =========================================================

N[0] = drones_iniciales
V[0] = 15              # m/s
C[0] = 1               # índice de riesgo
B[0] = bateria_inicial

# =========================================================
# MÉTODO DE EULER
# =========================================================

for i in range(len(t)-1):

    # -----------------------------------------------------
    # ECUACIÓN DEL NÚMERO DE DRONES
    # -----------------------------------------------------

    dN = tasa_entrada - tasa_salida * N[i]

    # -----------------------------------------------------
    # ECUACIÓN DE VELOCIDAD (MODELO MEJORADO)
    # -----------------------------------------------------


    dV = -k * N[i] + gamma * (velocidad_objetivo - V[i])

    # -----------------------------------------------------
    # ECUACIÓN DEL RIESGO
    # -----------------------------------------------------

    dC = alpha * N[i] - beta * C[i]

    # -----------------------------------------------------
    # ECUACIÓN DE BATERÍA
    # -----------------------------------------------------

    dB = -k * B[i]

    # =====================================================
    # ACTUALIZACIÓN DE VARIABLES
    # =====================================================

    N[i+1] = N[i] + dN * dt

    V[i+1] = V[i] + dV * dt

    C[i+1] = C[i] + dC * dt

    B[i+1] = B[i] + dB * dt

    # =====================================================
    # RESTRICCIONES FÍSICAS
    # =====================================================

    # Un dron no puede tener velocidad negativa

    if V[i+1] < 0:
        V[i+1] = 0

    # La batería tampoco puede ser negativa

    if B[i+1] < 0:
        B[i+1] = 0

# =========================================================
# RESULTADOS FINALES
# =========================================================

drones_finales = N[-1]
velocidad_final = V[-1]
riesgo_final = C[-1]
bateria_final = B[-1]

# =========================================================
# INTERPRETACIÓN DEL SISTEMA
# =========================================================

print("\n===================================================")
print("           RESULTADOS DE LA SIMULACIÓN")
print("===================================================")

print(f"Número final de drones después de {tiempo_final} minutos: {drones_finales:.2f} drones")

print(f"Velocidad final después de {tiempo_final} minutos: {velocidad_final:.2f} m/s")

print(f"Riesgo de colisión final: {riesgo_final:.2f}")

print(f"Batería restante después de {tiempo_final} minutos: {bateria_final:.2f} %")

print("\nINTERPRETACIÓN DEL SISTEMA")
print("---------------------------------------------------")

# =========================================================
# CONGESTIÓN
# =========================================================

if drones_finales <= 20:
    print("• Tráfico aéreo BAJO.")
    print("  El sector mantiene rutas despejadas y buena movilidad.")

elif drones_finales <= 50:
    print("• Tráfico aéreo MODERADO.")
    print("  Los drones deben realizar pequeñas correcciones de trayectoria.")

else:
    print("• Tráfico aéreo ALTO.")
    print("  Existe congestión aérea y riesgo de saturación.")

# =========================================================
# VELOCIDAD
# =========================================================

if velocidad_final >= 10:
    print("• Velocidad adecuada.")
    print("  Los drones operan dentro de rangos seguros.")

elif velocidad_final >= 5:
    print("• Velocidad reducida.")
    print("  La congestión comienza a afectar el desplazamiento.")

elif velocidad_final > 0:
    print("• Velocidad crítica.")
    print("  El tráfico es demasiado denso y limita la movilidad.")

else:
    print("• Drones detenidos.")
    print("  La congestión o las condiciones externas impiden el movimiento.")

# =========================================================
# RIESGO
# =========================================================

if riesgo_final <= 3:
    print("• Riesgo de colisión BAJO.")
    print("  El sistema mantiene una operación segura.")

elif riesgo_final <= 7:
    print("• Riesgo de colisión MODERADO.")
    print("  Se requieren ajustes de navegación.")

else:
    print("• Riesgo de colisión ALTO.")
    print("  El sistema necesita redireccionamiento urgente.")

# =========================================================
# BATERÍA
# =========================================================

if bateria_final >= 30:
    print("• Autonomía energética adecuada.")

elif bateria_final >= 20:
    print("• Batería en nivel preventivo.")
    print("  Se recomienda planificar recarga.")

elif bateria_final > 0:
    print("• Nivel crítico de batería.")
    print("  Los drones deben regresar inmediatamente.")

else:
    print("• Batería agotada.")
    print("  El dron no puede continuar operando.")

# =========================================================
# VIENTO
# =========================================================

if nivel_viento <= 3:
    print("• Condiciones climáticas favorables.")

elif nivel_viento <= 6:
    print("• Viento moderado.")
    print("  Los drones realizan correcciones leves.")

else:
    print("• Viento fuerte.")
    print("  La estabilidad del vuelo se ve afectada.")

# =========================================================
# GRÁFICAS
# =========================================================

plt.figure(figsize=(12,8))

# Número de drones
plt.subplot(2,2,1)
plt.plot(t, N)
plt.title("Número de drones")
plt.xlabel("Tiempo (min)")
plt.ylabel("Drones")

# Velocidad
plt.subplot(2,2,2)
plt.plot(t, V)
plt.title("Velocidad promedio")
plt.xlabel("Tiempo (min)")
plt.ylabel("Velocidad (m/s)")

# Riesgo
plt.subplot(2,2,3)
plt.plot(t, C)
plt.title("Riesgo de colisión")
plt.xlabel("Tiempo (min)")
plt.ylabel("Índice de riesgo")

# Batería
plt.subplot(2,2,4)
plt.plot(t, B)
plt.title("Nivel de batería")
plt.xlabel("Tiempo (min)")
plt.ylabel("Batería (%)")

plt.tight_layout()
plt.show()


# In[ ]:




