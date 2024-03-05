import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

RANDOM_SEED = 42

# Creando el entorno de simulación
env = simpy.Environment()

# Creando los recursos: RAM y CPU
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)
interval = 10
random.seed(RANDOM_SEED)

# Lista para almacenar los tiempos de los procesos
process_times = []

# Función para imprimir los datos
def print_data(data):
    for i, value in enumerate(data):
        print(f"Proceso {i+1}: {value}")

# Definición del proceso
def process(env, name, RAM, CPU):
    memory = random.randint(1, 10)  # Memoria requerida
    instructions = random.randint(1, 10)  # Número de instrucciones

    start = env.now  # Tiempo de inicio

    yield env.timeout(random.expovariate(1.0 / interval))  # Tiempo de llegada

    yield RAM.get(memory)  # Solicitar RAM

    while instructions > 0:
        with CPU.request() as req:  # Solicitar CPU
            yield req
            for _ in range(min(instructions, 3)):  # Ejecutar instrucciones
                yield env.timeout(1)
                instructions -= 1

        if instructions == 0:  # Si el proceso ha terminado
            yield RAM.put(memory)  # Devolver la RAM
            process_times.append(env.now - start)  # Guardar el tiempo del proceso
            break

        next_state = random.randint(1, 21)  # Decidir el siguiente estado
        if next_state == 1:  # Si el proceso entra en espera
            yield env.timeout(random.expovariate(1.0 / interval))  # Tiempo de espera

# Creando los procesos
for i in range(200):
    env.process(process(env, f'Proceso {i}', RAM, CPU))

# Ejecutando la simulación
env.run()

# Calculando estadísticas
average_time = np.mean(process_times)
standard_deviation = np.std(process_times)

print(f'Tiempo promedio: {average_time}')
print(f'Desviación estándar: {standard_deviation}')

# Creando la gráfica
plt.figure(figsize=(10, 6))
plt.hist(process_times, bins=20, alpha=0.5, color='g')
plt.axvline(average_time, color='r', linestyle='dashed', linewidth=2)
plt.title('Tiempo de los procesos')
plt.xlabel('Tiempo')
plt.ylabel('Número de procesos')
plt.grid(True)
plt.show()