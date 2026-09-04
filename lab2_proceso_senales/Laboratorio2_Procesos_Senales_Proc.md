# 🧪 LABORATORIO #2: Gestión de Procesos, Señales y la Interfaz `/proc`

> **Curso:** Sistemas Operativos (0689) · **Grupo:** 1SF134
> **Docente:** Isacio Manuel Tamayo Rodríguez
> **Unidad:** 2 — Gestión de Procesos y Procesador
> **Modalidad:** Individual
> **Duración estimada:** 2 horas
> **Sistema Operativo:** Linux (Ubuntu / Debian recomendado)

------

## 📋 Tabla de contenidos

1. [Objetivos del laboratorio](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#1--objetivos-del-laboratorio)
2. [Requisitos previos y Setup](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#2--requisitos-previos-y-setup)
3. [Fase 1 — Carga, pipelines, jerarquía y estados de procesos](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#3--fase-1--carga-pipelines-jerarquía-y-estados-de-procesos)
4. [Fase 2 — Señales POSIX y captura con `trap`](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#4--fase-2--señales-posix-y-captura-con-trap)
5. [Fase 3 — `/proc`: información del proceso, FD y métricas](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#5--fase-3--proc-información-del-proceso-fd-y-métricas)
6. [Cuestionario técnico](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#6--cuestionario-técnico)
7. [Instrucciones y formato de entrega](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#7--instrucciones-y-formato-de-entrega)
8. [Rúbrica de evaluación](https://chatgpt.com/c/6a9adebf-4884-83e8-b5e7-8d6c393b1afa#8--rúbrica-de-evaluación)

------

# 1. 🎯 Objetivos del laboratorio

Al finalizar este laboratorio práctico, el estudiante estará capacitado para:

- **Manipular la ejecución de procesos** en Linux identificando PIDs, PPIDs y porcentajes de uso de CPU.
- **Diagnosticar y corregir fallas en pipelines de comandos CLI** para extraer y filtrar métricas de rendimiento reales.
- **Analizar la jerarquía de procesos** mediante la relación padre-hijo y herramientas de visualización.
- **Interpretar los estados del ciclo de vida de un proceso** (`Running`, `Sleeping`, `Zombie`, etc.) mediante herramientas del sistema.
- **Evaluar el comportamiento de las señales POSIX** y el mecanismo de captura mediante `trap`.
- **Inspeccionar información expuesta por el Kernel** mediante el sistema de archivos virtual `/proc`.
- **Analizar descriptores de archivos** (`stdin`, `stdout`, `stderr`) asociados a un proceso.
- **Interpretar métricas de ejecución**, como los cambios de contexto voluntarios e involuntarios.
- **Comprender la diferencia entre un archivo convencional y un pseudo-archivo de `/proc`**.

------

# 2. 🛠️ Requisitos previos y Setup

## Requisitos del entorno

- Máquina virtual o entorno Linux nativo.
- Ubuntu/Debian recomendado.
- Usuario con permisos administrativos para utilizar `sudo`.
- Terminal de comandos.
- Editor de texto como `nano` o `vim`.

> ⚠️ **Importante — Seguridad**
>
> Los comandos de terminación utilizados durante este laboratorio deben ejecutarse **únicamente sobre procesos creados durante la práctica**.
>
> No utilices `kill`, `pkill`, `killall` u otros comandos de terminación sobre procesos del sistema que no hayas creado.

## Configuración inicial

Antes de comenzar, actualiza los repositorios e instala las herramientas utilizadas durante el laboratorio:

```bash
sudo apt update && sudo apt install -y procps psmisc coreutils
```

| Paquete     | Utilidades incluidas          | Propósito                                  |
| ----------- | ----------------------------- | ------------------------------------------ |
| `procps`    | `ps`, `top`, `pgrep`, `pkill` | Consulta y monitoreo de procesos           |
| `psmisc`    | `pstree`, `fuser`, `killall`  | Visualización e interacción con procesos   |
| `coreutils` | `sha256sum`, `sleep`, `cp`    | Generación de carga y pruebas con archivos |

> 💡 **Nota**
>
> Los resultados obtenidos durante el laboratorio pueden variar ligeramente dependiendo de la distribución, versión del Kernel, cantidad de CPU, procesos activos y carga actual del sistema.

------

# 3. 🧪 FASE 1 — Carga, pipelines, jerarquía y estados de procesos

## 💡 Marco conceptual

Un **programa** es un conjunto de instrucciones almacenado de forma persistente. Cuando el sistema operativo carga esas instrucciones y les asigna recursos para su ejecución, se crea un **proceso**.

El Kernel mantiene diferentes estructuras internas para administrar cada proceso. Estas estructuras contienen información relacionada con su identificación, estado, recursos, contexto de ejecución y otros elementos necesarios para su administración.

Linux expone parte de esta información mediante interfaces como `/proc`.

------

## 3.1 — Generación y verificación de carga sintética

Ejecuta el siguiente bucle:

```bash
for i in {1..4}; do (sha256sum /dev/urandom > /dev/null &); done
```

Este comando crea cuatro procesos `sha256sum` que permanecerán procesando datos.

### ¿Qué ocurre?

- **`/dev/urandom`** proporciona un flujo continuo de datos pseudoaleatorios generado por el Kernel.
- **`sha256sum`** calcula continuamente el hash SHA-256 de los datos recibidos.
- **`> /dev/null`** descarta la salida estándar.
- **`&`** ejecuta el proceso en segundo plano.

### Verificación

Ejecuta:

```bash
ps aux | grep sha256sum
```

> 📄 **Entregable**
>
> 1. Registra los PIDs de los cuatro procesos `sha256sum`.
> 2. Registra el `%CPU` mostrado para cada proceso.
> 3. Explica por qué puede aparecer una línea correspondiente al propio comando `grep sha256sum`.
>
> La salida puede variar dependiendo del momento exacto en que ejecutes el comando y de los procesos activos en tu sistema.

------

## 3.2 — 🚨 RETO DE DEBUGGING #1: Corrección de Pipeline

Un administrador intenta obtener los **tres procesos que actualmente presentan mayor consumo de CPU** utilizando:

```bash
ps aux --sort=-%cpu | awk '{print $2, $3, $11}' | head -n 3
```

### El problema

Al ejecutar el pipeline, observa que la salida no contiene tres procesos reales.

Por ejemplo:

```text
PID %CPU COMMAND
5102 98.5 sha256sum
5103 98.2 sha256sum
```

### 🔎 Análisis

Analiza cada etapa del pipeline:

```text
ps
 ↓
awk
 ↓
head
```

Determina:

- ¿Qué información aparece en la primera línea?
- ¿Por qué esa línea afecta el resultado de `head`?
- ¿Cuántos procesos reales quedan finalmente en pantalla?

### 🎯 Tu objetivo

Diseña un pipeline corregido que:

1. No incluya la cabecera.
2. Ordene los procesos por consumo de CPU.
3. Muestre únicamente los tres procesos reales con mayor consumo.
4. Mantenga únicamente las columnas necesarias.

> 📄 **Entregable**
>
> - Pipeline corregido.
> - Explicación de cada etapa.
> - Explicación de por qué el pipeline original produce un resultado incorrecto.

------

## 3.3 — Análisis de estados del Kernel

Los procesos pueden encontrarse en diferentes estados dependiendo de si están utilizando la CPU, esperando recursos, detenidos o finalizados.

Ejecuta:

```bash
ps -eo pid,ppid,stat,comm
```

### Estados principales

| Código  | Estado                  | Descripción                                                  |
| ------- | ----------------------- | ------------------------------------------------------------ |
| **`R`** | *Running / Runnable*    | El proceso está ejecutándose o listo para ejecutarse.        |
| **`S`** | *Interruptible Sleep*   | El proceso está esperando un evento y puede ser despertado por determinadas señales. |
| **`D`** | *Uninterruptible Sleep* | El proceso está esperando una operación que el Kernel considera no interrumpible, normalmente relacionada con E/S. |
| **`T`** | *Stopped*               | El proceso se encuentra detenido.                            |
| **`Z`** | *Zombie*                | El proceso terminó su ejecución, pero su padre todavía no ha recogido su estado de salida. |

> 📄 **Entregable**
>
> Selecciona tres procesos de tu lista.
>
> 1. Registra su PID, PPID, estado y nombre.
> 2. Consulta:
>
> ```bash
> man ps
> ```
>
> 1. Investiga la sección **PROCESS STATE CODES**.
> 2. Explica el significado de los caracteres adicionales que aparezcan junto al estado principal, por ejemplo `+`, `s` o `<`.

------

## 3.4 — Inspección de la jerarquía de procesos

En una instalación convencional de Ubuntu/Debian que utiliza `systemd`, este suele ocupar el **PID 1** y actuar como proceso inicial del espacio de usuario.

Los procesos posteriores pueden organizarse mediante relaciones padre-hijo.

### Paso 1 — Identificar el último proceso `sha256sum`

```bash
pgrep -n sha256sum
```

Registra el PID obtenido.

### Paso 2 — Mostrar su árbol de procesos

```bash
pstree -p -s $(pgrep -n sha256sum)
```

> 📄 **Entregable**
>
> 1. Incluye el árbol obtenido.
> 2. Identifica el PID de tu intérprete de comandos.
> 3. Identifica el proceso `sha256sum`.
> 4. Explica la relación padre-hijo entre ambos.
> 5. Determina cómo se relaciona esta jerarquía con el PID 1.

------

## 3.5 — Limpieza de carga mediante tuberías

Una vez finalizadas las actividades de esta fase, elimina los procesos `sha256sum` creados durante la práctica:

```bash
pgrep sha256sum | xargs kill -s SIGTERM
```

Verifica:

```bash
ps aux | grep sha256sum
```

> 📄 **Entregable**
>
> Explica:
>
> 1. ¿Qué información produce `pgrep`?
> 2. ¿Qué hace `xargs`?
> 3. ¿Qué relación existe entre la salida de `pgrep` y los argumentos recibidos por `kill`?
> 4. ¿Qué significa enviar `SIGTERM`?

------

# 4. 🧩 FASE 2 — Señales POSIX y captura con `trap`

## 💡 Marco conceptual

Una **señal** es una notificación asíncrona utilizada por el sistema operativo o por otros procesos para comunicar determinados eventos a un proceso.

Dependiendo de la señal, el proceso puede:

- Ejecutar la acción predeterminada.
- Ignorarla.
- Capturarla y ejecutar un manejador.

En Bash, `trap` permite definir acciones que serán ejecutadas cuando el shell reciba determinadas señales.

```text
[ Kernel / Proceso / Terminal ]
              │
              │ Señal POSIX
              ▼
       [ Proceso receptor ]
              │
       ┌──────┼───────────┐
       ▼      ▼           ▼
  Acción    Ignorar    Capturar
  default              con trap
```

------

## 4.1 — Creación del script de pruebas

Crea:

```bash
nano servicio_senales.sh
```

Escribe:

```bash
#!/bin/bash

# Captura de SIGINT y SIGTERM
trap 'echo "[!] Petición de terminación interceptada e ignorada."' SIGINT SIGTERM

echo "Servicio de pruebas iniciado. PID de este proceso: $$"

while true; do
    sleep 2
done
```

Guarda el archivo.

------

## 4.2 — 🚨 RETO DE DEBUGGING #2: Error de permisos

Intenta ejecutar el script:

```bash
./servicio_senales.sh &
```

Es posible que recibas:

```text
bash: ./servicio_senales.sh: Permission denied
```

### 🔎 Análisis

Consulta los permisos:

```bash
ls -l servicio_senales.sh
```

Determina:

- ¿Qué permisos tiene actualmente el archivo?
- ¿Qué significa cada grupo de permisos?
- ¿Por qué el sistema no permite ejecutarlo directamente?

### 🎯 Tu objetivo

Investiga qué mecanismo de permisos de Linux debes utilizar para permitir la ejecución del script **sin cambiar su propietario**.

> 📄 **Entregable**
>
> 1. Salida de `ls -l` antes del cambio.
> 2. Comando utilizado.
> 3. Salida de `ls -l` después del cambio.
> 4. Explicación de qué permiso fue modificado.
> 5. Ejecución exitosa del script.

------

## 4.3 — Evaluación de resistencia a señales

Ejecuta nuevamente:

```bash
./servicio_senales.sh &
```

Registra el PID mostrado por el script.

### Prueba 1 — SIGINT

```bash
kill -2 <PID_DEL_SCRIPT>
```

### Prueba 2 — SIGTERM

```bash
kill -15 <PID_DEL_SCRIPT>
```

### Verificación

```bash
ps aux | grep servicio_senales
```

> 📄 **Entregable**
>
> Describe qué ocurre en tu ejecución después de enviar cada señal.
>
> Explica:
>
> 1. ¿Qué función cumple `trap`?
> 2. ¿Qué acción habría ocurrido normalmente con estas señales?
> 3. ¿Por qué el script continúa ejecutándose?
>
> Si el comportamiento no es inmediato, analiza qué proceso está ejecutándose y vuelve a consultar su estado.

------

## 4.4 — Destrucción incondicional del proceso

Ahora debes finalizar definitivamente el script.

Investiga:

```bash
man 7 signal
```

o:

```bash
kill -l
```

Identifica la señal que:

- No puede ser capturada.
- No puede ser ignorada.
- No puede ser bloqueada por el proceso receptor.
- Es procesada directamente por el Kernel.

### 🎯 Tu objetivo

Identifica el nombre y número de la señal y utilízala para finalizar el proceso.

Después verifica:

```bash
ps aux | grep servicio_senales
```

> 📄 **Entregable**
>
> 1. Nombre de la señal.
> 2. Número de la señal.
> 3. Comando utilizado.
> 4. Evidencia de que el proceso terminó.
> 5. Explicación de por qué `trap` no puede interceptar esta señal.

------

# 5. 🔬 FASE 3 — `/proc`: información del proceso, FD y métricas

## 💡 Marco conceptual

`/proc` es un **sistema de archivos virtual (procfs)** proporcionado por el Kernel y conectado a la infraestructura VFS de Linux.

Sus entradas no representan necesariamente archivos convencionales almacenados en disco. Muchos de sus contenidos se generan dinámicamente cuando un programa los consulta.

Para cada proceso activo podemos encontrar información en:

```text
/proc/<PID>/
```

Por ejemplo:

```text
/proc/<PID>/status
/proc/<PID>/limits
/proc/<PID>/fd/
```

Estas interfaces permiten consultar información relacionada con el proceso directamente desde el sistema operativo.

------

## 5.1 — Despliegue de un proceso con redirección de flujos

Ejecuta:

```bash
sleep 10000 > /dev/null 2>&1 &
```

Obtén el PID:

```bash
echo $!
```

Guarda este PID porque será utilizado durante toda la fase.

------

## 5.2 — Inspección de descriptores de archivo

Accede al directorio del proceso:

```bash
cd /proc/<PID_DEL_SLEEP>/
```

Consulta sus descriptores:

```bash
ls -l fd/
```

Los tres descriptores estándar son:

| FD   | Canal POSIX | Función          |
| ---- | ----------- | ---------------- |
| `0`  | `stdin`     | Entrada estándar |
| `1`  | `stdout`    | Salida estándar  |
| `2`  | `stderr`    | Salida de error  |

> 📄 **Entregable**
>
> Completa:

| Descriptor | Canal POSIX | Ruta o dispositivo |
| ---------- | ----------- | ------------------ |
| `0`        | `stdin`     |                    |
| `1`        | `stdout`    |                    |
| `2`        | `stderr`    |                    |

### Pregunta de análisis

¿Por qué los descriptores `1` y `2` apuntan hacia `/dev/null`?

Relaciona tu respuesta con:

```bash
sleep 10000 > /dev/null 2>&1 &
```

------

## 5.3 — Auditoría de cambios de contexto

Consulta:

```bash
grep -i "switches" status
```

Encontrarás métricas como:

```text
voluntary_ctxt_switches
nonvoluntary_ctxt_switches
```

### 💡 ¿Qué es un cambio de contexto?

Un **cambio de contexto** ocurre cuando el sistema operativo cambia la ejecución de un proceso o hilo a otro, preservando la información necesaria para posteriormente continuar la ejecución.

Un cambio puede producirse porque un proceso:

- Cede voluntariamente la CPU.
- Necesita esperar por una operación.
- Es desplazado por el planificador.

> 📄 **Entregable**
>
> 1. Define con tus palabras qué es un cambio de contexto.
> 2. Explica la diferencia entre un cambio voluntario e involuntario.
> 3. Registra los valores obtenidos para `sleep`.
> 4. ¿Cuál de los dos valores es mayor en tu ejecución?
> 5. Propón una explicación relacionada con el comportamiento del proceso `sleep`.

> 💡 **Importante:** No existe un valor universal esperado. Los resultados dependen del sistema y del momento de observación.

------

## 5.4 — Comparativa: `ps` vs `/proc`

Consulta el proceso mediante `ps`:

```bash
ps -p <PID_DEL_SLEEP> -o pid,ppid,stat,comm
```

Ahora consulta directamente `/proc`:

```bash
grep -E "^(Name|State|Pid|PPid):" status
```

Completa:

| Campo  | Valor reportado por `ps` | Valor en `/proc/<PID>/status` |
| ------ | ------------------------ | ----------------------------- |
| PID    |                          |                               |
| PPID   |                          |                               |
| Estado |                          |                               |
| Nombre |                          |                               |

### Pregunta de reflexión

> ¿De dónde obtiene `ps` la información que muestra?
>
> ¿Qué relación existe entre la información presentada por `ps` y la información disponible en `/proc`?

------

## 5.5 — Evaluación de límites del proceso

Consulta:

```bash
cat limits | head -n 12
```

Localiza las entradas relacionadas con:

- `Max open files`
- `Max processes`

> 📄 **Entregable**
>
> 1. Registra los valores encontrados.
> 2. Explica qué representa el **Soft Limit**.
> 3. Explica qué representa el **Hard Limit**.
> 4. Explica por qué los límites de recursos son importantes en un sistema operativo multiusuario.
> 5. ¿Qué problemas podría provocar que un proceso pudiera consumir recursos indefinidamente?

------

## 5.6 — 🔬 EXPERIMENTO: El tamaño "fantasma" de `/proc`

Consulta:

```bash
ls -lh status
```

Ahora copia el contenido:

```bash
cp status ~/status_copia.txt
```

Comprueba el tamaño:

```bash
ls -lh ~/status_copia.txt
```

### 📄 Entregable

Compara:

```text
/proc/<PID>/status
```

con:

```text
~/status_copia.txt
```

Responde:

1. ¿Qué tamaño muestra el pseudo-archivo?
2. ¿Qué tamaño tiene la copia?
3. ¿Por qué puede aparecer `0 bytes` en el pseudo-archivo aunque pueda leerse una cantidad considerable de texto?
4. ¿Por qué la copia sí posee un tamaño real?
5. Explica conceptualmente qué ocurre cuando un programa utiliza la llamada al sistema `read()` para leer información desde `/proc`.

> 💡 **Concepto clave**
>
> La información presentada por `/proc` puede generarse dinámicamente por el Kernel cuando es solicitada. No debe confundirse con un archivo convencional almacenado físicamente en el disco.

------

## 5.7 — Destrucción del proceso y verificación de `/proc`

Finaliza el proceso:

```bash
kill -SIGKILL <PID_DEL_SLEEP>
```

Comprueba:

```bash
ps -p <PID_DEL_SLEEP>
```

Después intenta acceder nuevamente:

```bash
ls /proc/<PID_DEL_SLEEP>
```

> 📄 **Entregable**
>
> 1. Registra el resultado.
> 2. Explica qué ocurrió con el proceso.
> 3. Explica qué ocurrió con `/proc/<PID>`.
> 4. Relaciona la existencia de las entradas del proceso en `/proc` con su ciclo de vida.

------

# 6. ❓ Cuestionario técnico

Responde las siguientes **9 preguntas** utilizando tus propias palabras y fundamentando técnicamente tus respuestas.

### 1. Cambios de contexto

Describe:

- Un escenario que pueda provocar un `voluntary_ctxt_switch`.
- Un escenario que pueda provocar un `nonvoluntary_ctxt_switch`.

Explica por qué ocurre cada uno.

------

### 2. Naturaleza de `/proc`

¿Por qué los pseudo-archivos de `/proc` pueden reportar un tamaño de `0 bytes` aunque al leerlos proporcionen información?

------

### 3. Procesos Zombie

Responde:

- ¿Qué representa técnicamente un proceso Zombie?
- ¿Por qué `kill -9` no elimina un proceso que ya está en estado `Z`?
- ¿Qué debe ocurrir para que desaparezca la entrada del proceso?

------

### 4. Manejo de señales

Explica cómo cambia el comportamiento de un proceso cuando utiliza `trap` para manejar una señal frente al comportamiento predeterminado de esa señal.

Utiliza como referencia el script desarrollado en el laboratorio.

------

### 5. SIGTERM vs SIGKILL

Explica la diferencia entre:

```text
SIGTERM
```

y:

```text
SIGKILL
```

considerando:

- Acción predeterminada.
- Posibilidad de captura.
- Posibilidad de ignorar la señal.
- Participación del proceso receptor.

------

### 6. Descriptores de archivos

Desde la perspectiva de un analista de ciberseguridad o investigador forense:

> ¿Qué información útil puede proporcionar la inspección de `/proc/<PID>/fd/` de un proceso sospechoso?

Incluye al menos dos ejemplos.

------

### 7. `ps`, `top`, `htop` y `/proc`

Explica la relación conceptual entre las herramientas de monitoreo:

```text
ps
top
htop
```

y la información expuesta por `/proc`.

------

### 8. Ciclo de vida de procesos

Explica brevemente el significado de:

- `R`
- `S`
- `Z`

Incluye un ejemplo de cuándo podría observarse cada estado.

------

### 9. Límites de recursos

Explica qué función cumple:

```text
/proc/<PID>/limits
```

y qué problemas de estabilidad o seguridad podrían producirse si los procesos no tuvieran mecanismos para limitar el consumo de recursos.

------

# 7. 📤 Instrucciones y formato de entrega

## Requisitos

- **Formato:** exclusivamente PDF.
- **Nomenclatura:**

```text
Apellido_Nombre_Lab2.pdf
```

Ejemplo:

```text
Tamayo_Isacio_Lab2.pdf
```

## 📋 Checklist

Antes de entregar, verifica:

-  Carátula oficial.
-  PIDs y `%CPU` de los procesos generados.
-  Análisis del proceso `grep`.
-  Pipeline corregido del Reto de Debugging #1.
-  Explicación del pipeline corregido.
-  Análisis de estados de procesos.
-  Árbol de procesos mediante `pstree`.
-  Relación padre-hijo identificada.
-  Evidencia de limpieza de los procesos.
-  Análisis del Reto de Debugging #2.
-  Permisos antes y después de modificar el script.
-  Evidencia de `SIGINT`.
-  Evidencia de `SIGTERM`.
-  Explicación del comportamiento de `trap`.
-  Identificación y ejecución de `SIGKILL`.
-  Tabla de descriptores `0`, `1` y `2`.
-  Análisis de `voluntary_ctxt_switches`.
-  Análisis de `nonvoluntary_ctxt_switches`.
-  Tabla comparativa `ps` vs `/proc`.
-  Análisis de `/proc/<PID>/limits`.
-  Experimento de `/proc` y copia local.
-  Explicación del comportamiento del pseudo-archivo.
-  Verificación de eliminación del proceso.
-  Cuestionario técnico completo.

> 💡 **Recomendación sobre evidencias**
>
> No es necesario incluir una captura de pantalla para cada comando. Incluye únicamente las evidencias solicitadas y asegúrate de que sean legibles y estén acompañadas de una explicación.

------

# 8. 📊 Rúbrica de evaluación

| Componente                        | Criterios evaluados                                          | Puntuación  |
| --------------------------------- | ------------------------------------------------------------ | ----------- |
| **Fase 1 — Procesos y Pipelines** | Generación de carga, identificación de procesos, estados, jerarquía mediante `pstree`, limpieza y resolución justificada del Reto de Debugging #1. | **25 pts**  |
| **Fase 2 — Señales y `trap`**     | Resolución justificada del Reto de Debugging #2, permisos, comportamiento de `SIGINT` y `SIGTERM`, uso de `trap` e identificación de `SIGKILL`. | **25 pts**  |
| **Fase 3 — `/proc`**              | Descriptores de archivo, comparación `ps`/`proc`, cambios de contexto, límites de recursos y experimento del pseudo-archivo. | **30 pts**  |
| **Cuestionario técnico**          | Comprensión conceptual, fundamentación técnica, capacidad de análisis y redacción propia. | **20 pts**  |
| **Total**                         |                                                              | **100 pts** |

------

## 🧑‍🏫 Nota para el estudiante

Este laboratorio no busca únicamente que ejecutes comandos.

En cada actividad debes seguir el ciclo:

```text
EJECUTAR
   ↓
OBSERVAR
   ↓
INTERPRETAR
   ↓
INVESTIGAR
   ↓
EXPLICAR
```

Los resultados pueden variar entre equipos. **Lo importante no es obtener exactamente los mismos números que otro estudiante, sino ser capaz de interpretar lo que tu sistema está mostrando y justificar técnicamente por qué ocurre.**
