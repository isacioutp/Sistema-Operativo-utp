# Laboratorio 3B — Simulación de Algoritmos de Planificación

> **Curso:** Sistemas Operativos (0689) · Grupo 1SF134
> **Docente:** Isacio Manuel Tamayo Rodríguez
> **Unidad:** 2 — Gestión de Procesos y Procesador (2.4 Planificación de Procesos)
> **Modalidad:** Individual · **Duración estimada:** 1h30 · **SO:** Linux (Ubuntu/Debian) + Python 3

---

## 🏢 Caso: "NovaTech necesita elegir un planificador"

> Sigues trabajando como **junior sysadmin** en **NovaTech**. Después de resolver la crisis del Lab 3A, tu gerente te llama a una reunión:
>
> *"Buen trabajo arreglando el servidor. Ahora tenemos otro problema: estamos construyendo un **sistema de procesamiento por lotes (batch)** para generar reportes de ventas cada noche. El servidor recibe 4 reportes simultáneos con diferentes tiempos de ejecución. Necesito que compares los algoritmos de planificación que viste en clase y me digas **cuál es el mejor para nuestro caso**, con datos reales, no solo teoría."*
>
> **Objetivo:** Simular FCFS, SJF y Round Robin para comparar sus métricas (tiempo de espera y retorno) y fundamentar una recomendación técnica a la gerencia.

---

## Requisitos previos

- Clase teórica de 2.4: algoritmos FCFS, SJF, Round Robin y prioridad.
- Python 3.8 o superior.

```bash
python3 --version
```

---

## 🎓 Método de trabajo: aprender haciendo (no solo copiar)

La lección central de este lab es que **debes poder verificar a mano** los resultados antes de confiar en el código:

```text
ANTICIPA → EJECUTA → COMPARA → INTERPRETA
```

1. **Dibuja el timeline a mano** (lapiz y papel) ANTES de correr cada algoritmo.
2. **Ejecuta** el script y compara con tu dibujo.
3. Si tu cálculo manual y el programa no coinciden: **el error es tuyo o del código** → es el momento de aprender, no de seguir adelante.
4. **Captura TODO el lab**: cada comando ejecutado y cada salida, fase por fase (Evidencias 1-4). Las capturas son parte del entregable.
5. **Interpreta al final**: primero el lab completo, y luego respondes las **Preguntas del entregable** con tus datos (números sin explicación no demuestran aprendizaje).

> 📚 **Recursos antes de empezar:**
> - Teoría previa: `Teoria_Lab3B_Algoritmos.pptx` (métricas, Gantt de cada algoritmo, quantum).
> - La **Parte A** (Lab 3A) te ayudó a ver cómo Linux planifica *de verdad*; aquí simulas la versión "de libro".

---

## Fase 1 — Entender el escenario

Los 4 reportes de ventas que el batch processing debe generar:

| Reporte | Proceso | Tiempo de llegada (s) | Tiempo de ráfaga (s) | Descripción |
|---------|---------|----------------------|---------------------|-------------|
| P1 | Generar reporte diario | 0 | 8 | Reporte principal, largo |
| P2 | Exportar CSV | 1 | 4 | Exportación rápida |
| P3 | Consolidar trimestral | 2 | 9 | El más pesado |
| P4 | Enviar notificaciones | 3 | 5 | Notificaciones a clientes |

> **Nota:** Estos tiempos son *simplificados*. En un caso real, la ráfaga representa el tiempo estimado de CPU que necesita cada tarea.

---

## Fase 2 — Código base

Crea el archivo `scheduler_sim.py`:

```python
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
    pendientes = list(procesos)
    t = 0
    resultados = []
    while pendientes:
        disponibles = [p for p in pendientes if p.llegada <= t]
        if not disponibles:
            t = min(p.llegada for p in pendientes)
            continue
        p = min(disponibles, key=lambda x: x.rafaga)
        inicio = max(t, p.llegada)
        fin = inicio + p.rafaga
        espera = inicio - p.llegada
        retorno = fin - p.llegada
        resultados.append((p.pid, espera, retorno))
        t = fin
        pendientes.remove(p)
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
```

### 2.1 Ejecuta el código

```bash
python3 scheduler_sim.py
```

**Qué mirar:** verás 6 bloques de salida. Los dos primeros son FCFS y SJF. Compara los promedios de cada uno.

> **📸 Evidencia 1:** captura de toda la salida.

---

## Fase 3 — Analizar SJF (Shortest Job First)

SJF no preemptivo: en cada paso, de los procesos que **ya llegaron** y **aún no se ejecutaron**, ejecuta el de **menor ráfaga**.

**Qué mirar en la salida de SJF:**

```
P1: espera=0   retorno=8
P2: espera=7   retorno=11
P4: espera=9   retorno=14     ← P4 se ejecuta ANTES que P3
P3: espera=15  retorno=24
```

¿Por qué P4 antes que P3? Porque P4 tiene ráfaga 5 y P3 tiene ráfaga 9. SJF elige al más corto.

**Verificación a mano (en papel):**

| t=0 | Solo llegó P1 → ejecuta P1 (0 a 8) |
|-----|-------------------------------------|
| t=8 | Llegaron todos. Menor ráfaga = P2(4) → ejecuta P2 (8 a 12) |
| t=12 | Quedan P3(9) y P4(5). Menor = P4 → ejecuta P4 (12 a 17) |
| t=17 | Solo queda P3 → ejecuta P3 (17 a 26) |

> **📸 Evidencia 2:** captura de la salida de SJF + foto de tu verificación en papel.

---

## Fase 4 — Round Robin: experimenta con el quantum

Ya ejecutaste `python3 scheduler_sim.py` en la Fase 2. Ahora **mira los 4 bloques de Round Robin** que ya salieron en esa misma salida:

```
-- Round Robin (q=1) --      ← quantum pequeño
-- Round Robin (q=3) --      ← quantum intermedio
-- Round Robin (q=5) --      ← quantum más grande
-- Round Robin (q=100) --    ← quantum gigante
```

**Qué comparar (mira los promedios):**

| Quantum | Prom. espera | Prom. retorno | ¿Qué pasa? |
|---------|-------------|---------------|------------|
| q=1 | 12.75 | 19.25 | Peor que FCFS — mucho cambio de contexto |
| q=3 | 13.50 | 20.00 | El intermedio |
| q=5 | 11.00 | 17.50 | Mejor que q=3 |
| q=100 | 8.75 | 15.25 | **Igual que FCFS** — el quantum es tan grande que nadie se interrumpe |

**Conclusión rápida:**
- q=100 se comporta como FCFS (el quantum nunca se agota)
- q=1 empeora por los cambios de contexto constantes

> **📸 Evidencia 3:** captura de los 4 bloques de Round Robin (ya los tienes del paso 2).

---

## Fase 5 — Comparación final y recomendación a la gerencia

### 5.1 Tabla comparativa

Completa con los resultados de tu ejecución:

| Algoritmo | Promedio espera (s) | Promedio retorno (s) | Ventaja | Desventaja |
|-----------|--------------------|--------------------|---------|------------|
| FCFS | | | | |
| SJF | | | | |
| RR (q=3) | | | | |

### 5.2 Informe para la gerencia

Redacta un párrafo breve (5-8 líneas) como si le hablaras a tu gerente, respondiendo:

> *"¿Cuál algoritmo recomiendas para el batch processing de reportes de NovaTech? Justifica con datos."*

Considera:
- ¿Qué algoritmo minimiza el tiempo de espera promedio?
- ¿Qué algoritmo minimiza el tiempo de retorno promedio?
- En un batch processing, ¿importa más la eficiencia total o la equidad entre procesos?

> **📸 Evidencia 4:** tabla comparativa completa + informe para la gerencia.

---

## ✅ Autocomprobación: ¿Cómo sé que lo hice bien?

| Verificación | Lo que DEBES obtener | Qué valida |
|--------------|----------------------|------------|
| Orden de SJF | `P1 → P2 → P4 → P3` (no `P1→P2→P3→P4`) | Que SJF reordena por menor ráfaga |
| Tabla comparativa | FCFS: espera **8.75** / retorno **15.25** · SJF: **7.75 / 14.25** · RR(q=3): **13.50 / 20.00** | Que los algoritmos están correctamente implementados |
| Tu timeline a mano | Coincide **exactamente** con la salida del programa | Que entiendes el algoritmo, no solo el código |
| `quantum=100` en RR | Resultados casi **idénticos a FCFS** | Que RR converge a FCFS con quantum grande |
| `quantum=1` en RR | Más equidad, pero promedios de espera/retorno peores | Que el overhead del cambio de contexto perjudica |

> Si un promedio no coincide, revisa tu verificación manual paso a paso antes de mirar el código de otro compañero. **Entender el algoritmo es la mitad del aprendizaje.**

---

## 📋 Resumen de entregables

| # | Entregable | Puntos |
|---|-----------|--------|
| 1 | Capturas de TODO el lab (Evidencias 1-4, Fases 2-5) | 10 |
| 2 | Verificación manual de SJF (Fase 3) | 10 |
| 3 | Experimento con distintos quantum (Fase 4) | 5 |
| 4 | Tabla comparativa + informe para gerencia (Fase 5) | 5 |
| 5 | **Preguntas del entregable** (sección final) | 10 |
| | **Total** | **40** |

> **📄 Archivos a subir:** `Apellido_Nombre_Lab3B.pdf` (informe con las capturas de todo el lab y las preguntas del entregable) + `Apellido_Nombre_Lab3B.py` (scheduler con las experimentaciones realizadas).

---

## 📝 Preguntas del entregable (se responden AL FINAL)

> ⚠️ **Orden de trabajo:** primero ejecuta **todas** las fases del lab tomando las capturas
> (Evidencias 1-4). Cuando ya tengas todos los resultados, responde esta sección para cerrar el
> entregable. Las preguntas se contestan con tus propias palabras y con **tus** números, no con teoría general.

### Parte A — Sobre tu simulación (usa tus resultados)

1. **FCFS vs SJF (Fase 2.1):** ¿Por qué FCFS y SJF obtienen resultados diferentes? ¿Qué hace SJF diferente con los procesos disponibles?

2. **Análisis de SJF (Fase 3):** ¿Por qué SJF obtiene mejores promedios de espera/retorno que FCFS con el WORKLOAD de NovaTech? Apóyate en tu tabla comparativa y en tu verificación manual.

3. **Experimentación con el quantum (Fase 4):** Completa con los valores de tu ejecución:

   | Quantum | Prom. espera (s) | Prom. retorno (s) | Observación |
   |---------|------------------|-------------------|-------------|
   | q=1 | | | |
   | q=3 | | | |
   | q=5 | | | |
   | q=100 | | | |

   - ¿Por qué un quantum muy grande (q=100) se comporta casi como FCFS?
   - ¿Por qué un quantum muy pequeño (q=1) genera overhead?

4. **Recomendación (Fase 5):** ¿Cuál algoritmo recomiendas para el batch processing de NovaTech y por qué? Justifica con los números de tu simulación (no solo con la teoría).

### Parte B — Preguntas técnicas

5. **SJF y el problema de la predicción:** En tu simulación conoces la ráfaga de cada proceso *antes* de ejecutarlo. En un sistema real, el kernel no conoce el tiempo exacto de ejecución de un proceso. ¿Cómo estima el kernel el tiempo restante? ¿Qué estrategia usa CFS (Completely Fair Scheduler) de Linux?

6. **Round Robin y el overhead:** Si el quantum es de 1 milisegundo y tienes 1000 procesos, ¿cuánto tiempo del CPU se gasta *solo* en cambiar de contexto? ¿Por qué un quantum demasiado pequeño es contraproducente?

7. **FCFS y el convoy effect:** Imagina que un proceso de 100 segundos llega primero, y después llegan 5 procesos de 1 segundo cada uno. ¿Cuál es el tiempo de espera promedio? ¿Por qué este fenómeno se llama "convoy effect"?

8. **SJF preemptivo (SRTF):** Si existiera una versión *preemptiva* de SJF (Shortest Remaining Time First), ¿qué pasaría si un proceso de ráfaga corta llega mientras uno de ráfaga larga se está ejecutando? ¿Se interrumpe el proceso largo?

9. **CFS de Linux:** Después de este laboratorio, explica por qué el planificador real de Linux (CFS) no es ninguno de los algoritmos que simulaste. ¿Qué lo hace diferente?

---

## 🔧 Comandos de referencia

| Comando | Función |
|---------|---------|
| `python3 scheduler_sim.py` | Ejecuta la simulación |
| `python3 -c "print(2+2)"` | Ejecuta código Python inline |
| `time python3 scheduler_sim.py` | Mide el tiempo de ejecución |

---

## 📚 Conceptos clave

| Concepto | Definición |
|----------|-----------|
| **Tiempo de espera** | Tiempo total que un proceso pasa esperando en la cola (sin ejecutarse) |
| **Tiempo de retorno** | Tiempo total desde la llegada hasta la finalización del proceso |
| **Ráfaga** | Tiempo de CPU que necesita un proceso para completarse |
| **Quantum** | Tiempo máximo que un proceso puede ejecutarse antes de ser preemptado en Round Robin |
| **Convoy effect** | Fenómeno donde procesos cortos quedan "atrapados" detrás de uno largo en FCFS |
| **CFS** | Completely Fair Scheduler — el planificador por defecto de Linux, usa virtual runtime para equidad |
