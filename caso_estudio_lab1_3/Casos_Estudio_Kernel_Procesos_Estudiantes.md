# Caso de Estudio — Kernel y Procesos

**Curso:** Sistemas Operativos (0689)  
**Grupo:** 1SF134  
**Docente:** Isacio Manuel Tamayo Rodríguez

## Propósito de la actividad

Analizar situaciones reales relacionadas con el funcionamiento del sistema operativo, enfocándose en el **kernel, los procesos y los recursos del sistema**.

La actividad busca que el estudiante pueda explicar, con sus propias palabras:

- Qué está haciendo el proceso.
- Qué hace el kernel.
- Qué recurso del sistema está involucrado.
- Qué ocurre internamente en el sistema operativo.

> **Importante:** El análisis debe mantenerse principalmente en el funcionamiento del sistema operativo. La seguridad puede mencionarse únicamente cuando aparezca de forma natural en el caso.

---

# Caso 1 — Fork Bomb: creación masiva de procesos

## Situación

Un proceso comienza a crear continuamente procesos hijos. La cantidad de procesos aumenta rápidamente hasta que el sistema comienza a quedarse sin recursos y deja de responder normalmente.

## Preguntas guía

1. ¿Qué ocurre cuando un proceso crea un proceso hijo?
2. ¿Cómo se relacionan el proceso padre y sus hijos?
3. ¿Qué información debe mantener el kernel sobre cada proceso?
4. ¿Qué recursos consume cada nuevo proceso?
5. ¿Qué ocurre cuando se alcanzan los límites de procesos o recursos?
6. ¿Qué papel tiene el scheduler en esta situación?

## Pregunta para discusión

**¿Por qué el sistema operativo necesita establecer límites para la creación de procesos?**

---

# Caso 2 — OOM Killer: cuando Linux se queda sin memoria

## Situación

Un sistema Linux tiene muy poca memoria disponible. Varios procesos continúan solicitando memoria hasta que el sistema alcanza una situación crítica y el kernel debe tomar una decisión para recuperar memoria.

## Preguntas guía

1. ¿Qué significa que un proceso utilice memoria?
2. ¿Qué ocurre cuando varios procesos solicitan más memoria?
3. ¿Cómo sabe el kernel cuánta memoria está disponible?
4. ¿Qué es el OOM Killer?
5. ¿Por qué el kernel puede decidir terminar un proceso?
6. ¿Qué consecuencias tiene terminar ese proceso?

## Pregunta para discusión

**Si ustedes fueran el kernel, ¿qué proceso considerarían para terminar y por qué?**

---

# Caso 3 — PID 1 y systemd: el proceso principal de Linux

## Situación

Durante el arranque de Linux aparece un proceso con **PID 1**. Este proceso participa en la gestión de servicios y procesos del sistema.

## Preguntas guía

1. ¿Qué significa PID?
2. ¿Por qué el PID 1 es especial?
3. ¿Qué función cumple systemd?
4. ¿Cómo se relacionan los procesos padre e hijo?
5. ¿Qué ocurre cuando un proceso padre termina antes que su hijo?
6. ¿Qué papel puede cumplir PID 1 en estas situaciones?

## Pregunta para discusión

**¿Qué podría ocurrir en un sistema Linux si el proceso PID 1 terminara inesperadamente?**

---

# Caso 4 — Scheduler de Linux: cómo se decide qué proceso utiliza la CPU

## Situación

En un sistema existen muchos procesos listos para ejecutarse, pero la CPU tiene una capacidad limitada. El kernel debe decidir qué proceso recibe tiempo de CPU.

## Preguntas guía

1. ¿Qué significa que un proceso esté listo para ejecutarse?
2. ¿Qué función cumple el scheduler?
3. ¿Cómo decide el sistema qué proceso ejecutar?
4. ¿Qué ocurre con los procesos que no están utilizando la CPU?
5. ¿Qué relación existe entre scheduler y context switch?
6. ¿Por qué el sistema necesita cambiar entre procesos?

## Pregunta para discusión

**Si tuvieran 20 procesos y una sola CPU, ¿cómo decidirían cuál debe ejecutarse primero?**

---

# Caso 5 — Context Switch: cambio entre procesos

## Situación

La CPU está ejecutando un proceso, pero el kernel necesita detenerlo temporalmente y permitir que otro proceso utilice la CPU.

## Preguntas guía

1. ¿Por qué es necesario cambiar de un proceso a otro?
2. ¿Qué información debe guardar el sistema antes de cambiar?
3. ¿Qué relación tiene el PCB con el context switch?
4. ¿Qué información debe restaurarse cuando el proceso vuelve a ejecutarse?
5. ¿Qué trabajo realiza el kernel durante este cambio?
6. ¿Por qué un context switch tiene un costo?

## Pregunta para discusión

**¿Qué podría ocurrir si el sistema realizara cambios de contexto miles de veces por segundo?**

---

# Caso 6 — Procesos padre e hijo: fork(), wait() y exit()

## Situación

Un proceso crea un proceso hijo. Posteriormente, el hijo termina su ejecución y el proceso padre puede esperar por su finalización.

## Preguntas guía

1. ¿Qué ocurre cuando se ejecuta `fork()`?
2. ¿Cómo se identifica al proceso padre y al proceso hijo?
3. ¿Qué función cumple `exit()`?
4. ¿Qué función cumple `wait()`?
5. ¿Qué es un proceso zombie?
6. ¿Qué información mantiene el kernel sobre estos procesos?
7. ¿Qué puede ocurrir si el proceso padre termina antes que el hijo?

## Pregunta para discusión

**¿Por qué el kernel necesita que el proceso padre pueda recoger el estado de terminación del hijo mediante `wait()`?**

---

# Caso 7 — Señales en Linux: comunicación y control de procesos

## Situación

Un proceso necesita recibir una señal enviada por otro proceso o por el propio sistema operativo. Dependiendo de la señal, el proceso puede terminar, detenerse, continuar o ejecutar un comportamiento definido.

## Preguntas guía

1. ¿Qué es una señal?
2. ¿Qué papel cumple el kernel cuando una señal es enviada?
3. ¿Qué diferencia existe entre una acción por defecto, ignorar una señal y capturarla?
4. ¿Qué diferencia existe entre `SIGTERM` y `SIGKILL`?
5. ¿Qué relación tienen las señales con el estado de un proceso?
6. ¿Qué permite hacer `trap` en un programa de shell?

## Pregunta para discusión

**¿Por qué existen señales que un proceso no puede capturar o ignorar?**

---

# Caso 8 — User Space vs Kernel Space

## Situación

Un programa necesita utilizar un recurso administrado por el sistema operativo. El programa no puede acceder directamente a determinadas funciones privilegiadas, por lo que debe solicitar el servicio al kernel.

## Preguntas guía

1. ¿Qué es User Space?
2. ¿Qué es Kernel Space?
3. ¿Por qué existe esta separación?
4. ¿Qué es una system call o syscall?
5. ¿Qué ocurre cuando un proceso realiza una syscall?
6. ¿Qué trabajo realiza el kernel antes de devolver el resultado al proceso?

## Pregunta para discusión

**¿Por qué un proceso no debería poder acceder directamente a cualquier recurso del computador?**

---

# Diagrama general para analizar el caso

Utilicen y adapten el siguiente modelo a su caso:

**PROCESO → SYSCALL / INTERACCIÓN → KERNEL → RECURSO DEL SISTEMA → RESULTADO → PROCESO**

El diagrama debe mostrar claramente qué ocurre en su caso y qué parte corresponde al proceso y cuál al kernel.

---

# Entregable

Cada grupo debe preparar una presentación de **4 a 5 diapositivas**:

### Diapositiva 1 — Portada
- Curso
- Grupo
- Integrantes
- Tema asignado

### Diapositiva 2 — Explicación del caso
Expliquen el caso con sus propias palabras y respondan las preguntas guía más importantes.

### Diapositiva 3 — Análisis desde Sistemas Operativos
Expliquen:

- Qué proceso o procesos están involucrados.
- Qué hace el kernel.
- Qué recurso del sistema está involucrado.
- Qué ocurre internamente en el sistema operativo.

### Diapositiva 4 — Diagrama
Presenten una adaptación del modelo:

**Proceso → Kernel → Recurso → Resultado**

Pueden agregar una quinta diapositiva si necesitan ampliar la explicación.

---

# Presentación

Cada grupo debe explicar su caso de manera clara y técnica, pero comprensible.

Todos los integrantes deben participar en la presentación y conocer el contenido del trabajo.

Durante la presentación el docente podrá realizar una pregunta relacionada con el funcionamiento del sistema operativo.

---

# Pregunta de cierre

Al finalizar el análisis, el grupo debe poder responder:

> **En su caso, ¿qué parte del trabajo la realiza el proceso y qué parte la realiza el kernel?**
