import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
import statistics

FIXED_MEMORY = 100
CPU_THREADS = 2
RANDOM_SEED = 77
CPU_REQUESTS = [25,50,100,150,200]

class proceso:

    def __init__(self, name, env, ram, procesador):
        self.name = name    
        self.memoria = np.random.randint(1, 10)
        self.num_instruc = np.random.randint(1, 10)
        self.env = env
        self.ram = ram
        self.procesador = procesador
        self.estado = "new"
        print(f'{self.name}: {self.estado} con {self.num_instruc} instrucciones')

    def pedir_memoria(self):
        print(f"{self.name}: Solicitando {self.memoria} de memoria RAM.")
        yield self.ram.get(self.memoria)
        self.estado = "ready"
        print(f'{self.name}: {self.estado}')

    def usar_cpu(self):
        with self.procesador.request() as req:
            # print(f"{self.name}: Solicitando CPU.")
            yield req
            # print(f"{self.name}: Utilizando CPU para {self.num_instruc} instrucciones.")
            self.estado = "running"
            self.count = 0
            print(f'{self.name}: {self.estado} {self.num_instruc} instrucciones')
            while self.num_instruc > 0 and self.count < 3:
                yield self.env.timeout(1)
                self.num_instruc -= 1
                self.count+=1
            self.estado = "terminate" if self.num_instruc == 0  else self.estado

    def pedir_io(self):
        
        yield self.env.timeout(1)
        self.estado = "waiting";
        print(f"{self.name}: {self.estado} Realizando operaciones de I/O.")

    def run(self):
        start_time = env.now
        yield self.env.process(self.pedir_memoria())
        
        while self.num_instruc > 0:
            
            yield self.env.timeout(1)  # Tiempo para cambiar de estado
            yield self.env.process(self.usar_cpu())
            print(f'{self.name}: {self.estado}')
            
            if np.random.randint(1, 2) == 1:  # Solo 1 o 2 para I/O o volver a "ready"
                yield self.env.process(self.pedir_io())
        # print(f"{self.name}: Terminado. Liberando {self.memoria} de memoria RAM.")
        yield self.ram.put(self.memoria)
        final_time = env.now
        tiempos_computadora.append(final_time - start_time)
        
        
        
        

def simular(env, RAM, CPU, procesos):
    tiempos_computadora.clear() 
    for i in range(procesos):
        name = f'task_{i+1}'
        newProcess = proceso(name, env, RAM, CPU)
        env.process(newProcess.run())
        yield env.timeout(random.expovariate(1))
    yield env.timeout(1)

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
resultados_promedio = []
resultados_desviacion = []
tiempos_computadora = []
for num_procesos in CPU_REQUESTS:
    env = simpy.Environment()
    RAM = simpy.Container(env, capacity=FIXED_MEMORY, init=FIXED_MEMORY)
    CPU = simpy.Resource(env, capacity=CPU_THREADS)
    env.process(simular(env, RAM, CPU, num_procesos))
    env.run()
    promedio_tiempo = statistics.mean(tiempos_computadora)
    desviacion_estandar = statistics.stdev(tiempos_computadora)

    resultados_promedio.append(promedio_tiempo)
    resultados_desviacion.append(desviacion_estandar)
    
for i, num_procesos in enumerate(CPU_REQUESTS):
    print(f"Procesos: {num_procesos}, Tiempo Promedio: {resultados_promedio[i]:.2f}, Desviación Estándar: {resultados_desviacion[i]:.2f}")

plt.plot(CPU_REQUESTS, resultados_promedio, label='Tiempo Promedio')
plt.errorbar(CPU_REQUESTS, resultados_promedio, yerr=resultados_desviacion, fmt='o', label='Desviación Estándar')
plt.xlabel('Número de Procesos')
plt.ylabel('Tiempo')
plt.title('Tiempo promedio y Desviación Estándar en función del número de procesos')
plt.legend()
plt.show()