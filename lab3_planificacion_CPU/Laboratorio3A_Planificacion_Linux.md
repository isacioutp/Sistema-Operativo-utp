# Laboratorio 3A — Planificación Real en Linux

> **Curso:** Sistemas Operativos (0689) · Grupo 1SF134
> **Docente:** Isacio Manuel Tamayo Rodríguez
> **Unidad:** 2 — Gestión de Procesos y Procesador (2.4 Planificación de Procesos)
> **Modalidad:** Individual · **Duración estimada:** 1h30 · **SO:** Linux (Ubuntu/Debian)

---

## 🏢 Caso: "El servidor de NovaTech se está incendiando"

> Eres **junior sysadmin** en **NovaTech**, una empresa de e-commerce. El lunes a las 8:00 AM recibes un ticket urgente:
>
> *"El servidor de producción responde muy lento. Los clientes se quejan de que la página tarda más de 10 segundos en cargar. El equipo de desarrollo dice que el servicio de recomendaciones (`sha256sum` como placeholder de un proceso pesado de IA) está comiendo toda la CPU y no hay forma de detenerlo sin que se caiga todo."*
>
> Tu gerente te dice: **"Necesito que entiendas cómo Linux decide qué proceso usa la CPU, y que puedas manipular eso en tiempo real. No podemos reiniciar el servidor hasta las 2 AM."**
>
> **Objetivo:** Aprender a diagnosticar y manipular la planificación de CPU en Linux para priorizar procesos críticos y degradar los que consumen recursos en exceso.

---

## Requisitos previos

- Clase teórica de 2.4: criterios de planificación, tipos de planificador, algoritmos FCFS/SJF/Round Robin/Prioridad.
- VM Linux del Lab 1 funcionando.
- Herramientas instaladas: `util-linux` (provee `chrt`, `taskset`), `coreutils` (provee `nice`, `renice`).

```bash
sudo apt update && sudo apt install -y util-linux
```

---

## 🎓 Método de trabajo: aprender haciendo (no solo copiar)

Para cada paso de este laboratorio sigue el ciclo **AE-CI**:

```text
ANTICIPA → EJECUTA → COMPARA → INTERPRETA
```

1. **Anticipa:** antes de ejecutar el comando, escribe en una línea qué crees que vas a ver y por qué.
2. **Ejecuta:** corre el comando tal cual está indicado.
3. **Compara:** cuando lo que viste no coincide con lo que anticipaste, **ahí está la lección**. Detente y pregúntate por qué.
4. **Interpreta:** completa los entregables con tus propias palabras, no copiando la salida.

> 📚 **Recursos antes de empezar:**
> - Teoría previa: `Teoria_Lab3A_Linux.pptx` (nice, renice, chrt, taskset, CFS).
> - ¿Quieres *ensayar* el lab antes de hacerlo de verdad? El módulo opcional `opcional_ansible/` despliega esta misma carga en un servidor por control remoto.

---

## Fase 1 — Diagnosticar: ¿Quién está usando la CPU?

### 1.1 Genera un proceso pesado (simula el servicio de recomendaciones)

```bash
sha256sum /dev/urandom > /dev/null &
echo "PID: $!"
```

### 1.2 Revisa su prioridad actual

```bash
ps -eo pid,ni,pri,cmd | grep sha256sum
```

| Columna | Significado |
|---------|-------------|
| `NI` | **Niceness**: valor de -20 (máxima prioridad) a 19 (mínima). Es lo que el *usuario* puede sugerir. |
| `PRI` | **Prioridad real** que el kernel asigna al proceso (calculada a partir de `NI` y otros factores). |

> **📄 Entregable:** ¿Cuál es el niceness por defecto de un proceso nuevo? ¿Qué significa que sea 0?

---

## Fase 2 — Degradar el proceso problemático con `nice`

Tu gerente te dice: *"No podemos matarlo, pero necesitamos que consuma menos CPU."*

### 2.1 Lanza un proceso con prioridad baja

```bash
nice -n 10 sha256sum /dev/urandom > /dev/null &
echo "PID: $!"
```

### 2.2 Compara las prioridades

```bash
ps -eo pid,ni,pri,cmd | grep sha256sum
```

> **📄 Entregable:**
> 1. ¿Cuál es el niceness del proceso lanzado con `nice -n 10`?
> 2. ¿Qué valor de `PRI` tiene comparado con el proceso normal?
> 3. ¿Qué significa en la práctica que un proceso tenga niceness 10?

### 2.3 Intenta subir la prioridad de un proceso que ya está corriendo

```bash
renice -n -5 -p <PID_DEL_PROCESO>
```

Obtendrás algo como:

```
renice: failed to set priority for <PID> (...): Permission denied
```

### 🔎 Análisis

- ¿Por qué Linux te deja *bajar* tu propia prioridad (aumentar NI) pero no *subirla* (bajar NI por debajo de 0)?
- ¿Qué pasaría si cualquier usuario pudiera asignarse niceness -20?
- ¿Qué comando del Lab 2 podrías usar para ejecutar esto con privilegios elevados?

> **📄 Entregable:** Explica la razón técnica de este comportamiento y el comando para resolverlo.

---

## Fase 3 — Diagnosticar la política de planificación con `chrt`

### 3.1 Consulta la política actual

```bash
chrt -p <PID>
```

Verás algo como:

```
pid <PID>'s current scheduling policy: SCHED_OTHER
pid <PID>'s current scheduling priority: 0
```

`SCHED_OTHER` es la política de uso general de Linux (**no** es tiempo real).

### 3.2 Intenta cambiar a política de tiempo real

```bash
chrt -f -p 10 <PID>
```

Probablemente fallará por permisos. Las políticas de tiempo real (`SCHED_FIFO`, `SCHED_RR`) le dan a un proceso **prioridad absoluta** sobre todos los procesos normales.

> **📄 Entregable:** ¿Qué pasaría si un proceso con `SCHED_FIFO` entra en un loop infinito? ¿Qué le ocurre al resto del sistema?

---

## Fase 4 — Afinidad de CPU con `taskset`

Tu gerente descubre que otro proceso crítico (base de datos) necesita un núcleo dedicado.

### 4.1 Ancla un proceso al núcleo 0

```bash
taskset -c 0 sha256sum /dev/urandom > /dev/null &
PID=$!
echo "PID: $PID"
```

### 4.2 Verifica

```bash
taskset -p $PID
```

### 4.3 Observa con `htop`

Abre `htop` (tecla `F2` → `Columns` → activar `CPU`). Verás que el proceso solo aparece en el núcleo 0.

> **📄 Entregable:**
> 1. ¿Qué uso de CPU muestra cada núcleo en `htop`?
> 2. ¿En qué situaciones reales sería útil limitar un proceso a un solo núcleo?
> 3. ¿Qué pasaría si tu servidor tiene 2 núcleos y anclas un proceso pesado al núcleo 0? ¿Cómo afecta esto al rendimiento general?

---

## Fase 5 — Limpieza

```bash
pkill sha256sum
```

Verifica:

```bash
ps aux | grep sha256sum
```

---

## ✅ Autocomprobación: ¿Cómo sé que lo hice bien?

Antes de entregar, verifica que observaste lo esperado:

| Paso | Lo que DEBES ver | Lo que significa |
|------|------------------|------------------|
| 1.2 `ps -eo pid,ni,pri` | Un proceso nuevo con `NI=0` y su `PRI` (≈20 en kernel 4.15/Ubuntu Bionic) | Por defecto nadie "sugiere" prioridad → ni 0 |
| 2.2 `nice -n 10` | El segundo proceso con `NI=10` y `PRI` mayor que el normal | Más `NI` → "amable"/poco urgente → pri peor (número mayor) |
| 2.3 `renice -n -5` | `Permission denied` | Subir prioridad es operación privilegiada |
| 3.1 `chrt -p` | `SCHED_OTHER`, prioridad 0 | Política normal, no tiempo real |
| 3.2 `chrt -f` | Error de permisos | FIFO es privilegiada |
| 4.2 `taskset -p` | Muestra solo el núcleo (ej. `0-0`) donde anclaste el proceso | Afinidad correcta |

> Si algún valor no coincide con lo esperado, **no es un error del laboratorio**: es una oportunidad de investigar por qué tu sistema particular se comporta así (versión de kernel, cfg, etc.). Eso se explica en tu entrega.

## 📋 Resumen de entregables

| # | Entregable | Puntos |
|---|-----------|--------|
| 1 | Niceness por defecto y su significado (1.2) | 3 |
| 2 | Comparación de prioridades con `nice -n 10` (2.2) | 4 |
| 3 | Análisis del error de permisos con `renice -n -5` (2.3) | 5 |
| 4 | Análisis de `chrt` y políticas de tiempo real (3.2) | 4 |
| 5 | Análisis de `taskset` y afinidad de CPU (4.3) | 5 |
| 6 | **Cuestionario técnico** (ver abajo) | 4 |
| | **Total** | **25** |

> **📄 Archivo a subir:** `Apellido_Nombre_Lab3A.pdf` (informe completo).

---

## ❓ Cuestionario técnico

Responde con tus propias palabras y fundamentación técnica:

1. **Niceness y prioridad:** Un usuario lanza un proceso con `nice -n 15` y otro con `nice -n -5` (usando `sudo`). Explica qué sucede cuando ambos compiten por la CPU al mismo tiempo.

2. **Políticas de planificación:** ¿Por qué `SCHED_OTHER` es suficiente para la mayoría de los procesos? ¿En qué escenario necesitarías `SCHED_FIFO` o `SCHED_RR`?

3. **Afinidad de CPU:** Si tu servidor tiene 4 núcleos y un proceso de machine learning que consume mucha memoria caché, ¿tiene sentido anclarlo a un solo núcleo? Argumenta tu respuesta considerando locality of reference.

4. **Seguridad:** Si un atacante pudiera usar `nice -n -20` y `chrt -f` sin restricciones, ¿qué tipo de ataque de denegación de servicio podría ejecutar?

---

## 🔧 Comandos de referencia

| Comando | Función |
|---------|---------|
| `nice -n <valor> <comando>` | Ejecuta un comando con niceness específico |
| `renice -n <valor> -p <PID>` | Cambia el niceness de un proceso en ejecución |
| `chrt -p <PID>` | Muestra la política de planificación |
| `chrt -f -p <prioridad> <PID>` | Cambia a política FIFO en tiempo real |
| `taskset -c <núcleos> <comando>` | Ejecuta en núcleos específicos |
| `taskset -p <PID>` | Muestra la afinidad actual |
| `ps -eo pid,ni,pri,cmd` | Lista procesos con prioridades |
