# scheduler_sim.py
from dataclasses import dataclass

@dataclass
class Proceso:
    pid: str
    llegada: int
    rafaga: int

WORKLOAD = [
    Proceso("P1", 0, 8),
    Proceso("P2", 1, 4),
    Proceso("P3", 2, 9),
    Proceso("P4", 3, 5),
]

def fcfs(procesos):
    procesos = sorted(procesos, key=lambda p: p.llegada)
    t = 0
    resultados = []
    for p in procesos:
        inicio = max(t, p.llegada)
        fin = inicio + p.rafaga
        espera = inicio - p.llegada
        retorno = fin - p.llegada
        resultados.append((p.pid, espera, retorno))
        t = fin
    return resultados

def sjf(procesos):
    # TODO: SJF no preemptivo — en cada paso, de los procesos ya "llegados",
    # elegir el de menor ráfaga restante. Esta versión es una copia de FCFS:
    # ¡está MAL! El orden es por llegada, no por ráfaga.
    procesos = sorted(procesos, key=lambda p: p.llegada)
    t = 0
    resultados = []
    for p in procesos:
        inicio = max(t, p.llegada)
        fin = inicio + p.rafaga
        espera = inicio - p.llegada
        retorno = fin - p.llegada
        resultados.append((p.pid, espera, retorno))
        t = fin
    return resultados

def round_robin(procesos, quantum=3):
    from collections import deque
    restante = {p.pid: p.rafaga for p in procesos}
    cola = deque(sorted(procesos, key=lambda p: p.llegada))
    t = 0
    fin_de = {}
    while cola:
        p = cola.popleft()
        ejecutar = min(quantum, restante[p.pid])
        t += ejecutar
        restante[p.pid] -= ejecutar
        if restante[p.pid] > 0:
            cola.append(p)
        fin_de[p.pid] = t
    resultados = []
    for p in procesos:
        retorno = fin_de[p.pid] - p.llegada
        espera = retorno - p.rafaga
        resultados.append((p.pid, espera, retorno))
    return resultados

def resumen(nombre, resultados):
    print(f"\n-- {nombre} --")
    total_espera = total_retorno = 0
    for pid, espera, retorno in resultados:
        print(f"{pid}: espera={espera}  retorno={retorno}")
        total_espera += espera
        total_retorno += retorno
    n = len(resultados)
    print(f"Promedio espera:  {total_espera/n:.2f}")
    print(f"Promedio retorno: {total_retorno/n:.2f}")

if __name__ == "__main__":
    resumen("FCFS", fcfs(WORKLOAD))
    resumen("SJF", sjf(WORKLOAD))
    resumen("Round Robin (q=3)", round_robin(WORKLOAD))