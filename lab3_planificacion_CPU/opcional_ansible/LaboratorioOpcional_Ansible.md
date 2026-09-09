# 📦 Módulo opcional — Ansible: prepara los Labs 3A y 3B desde el control

> **Curso:** Sistemas Operativos (0689) · Grupo 1SF134
> **Docente:** Isacio Manuel Tamayo Rodríguez
> **Modalidad:** Opcional · Bonus · Es **previo y complementario** a los Labs 3A y 3B
> **Estimado:** 1h – 2h

---

## 🎯 ¿Para qué sirve este módulo?

Tres objetivos en uno:

1. **Preparar el Lab 3A (Planificación real en Linux).** El Lab 3A te pide lanzar procesos, observar `NI`/`PRI` y jugar con `nice`, `renice`, `chrt` y `taskset`. Este módulo te hace **ensayarlo antes**: despliegas la misma carga sintética en un "servidor de producción" pero desde un punto central (Ansible), así cuando llegues al lab ya sabes qué vas a ver.
2. **Preparar el Lab 3B (Simulación de algoritmos).** El Lab 3B te pide simular FCFS, SJF y Round Robin y corregir el `sjf()` que viene con un bug. Este módulo **despliega y ejecuta la simulación en el servidor** por control remoto: verás el bug (FCFS = SJF) y usarás Ansible como mini-pipeline de *"edita → despliega → verifica"* para confirmar tu corrección.
3. **Aprender automatización de infraestructura.** Ansible es la herramienta que usa un equipo de operaciones real para configurar cientos de servidores idénticos con un solo comando.

> 🏢 **Contexto NovaTech:** tras la crisis del servidor, el equipo operativo decidió "nada de configurar máquinas a mano". Te piden aprender Ansible *antes* de que toque la planificación, para desplegar por control remoto tanto los procesos de prueba (3A) como el código de la simulación (3B).

> ✅ **Independiente del Lab 1:** este módulo trae su **propia máquina virtual** (`Vagrantfile`). No necesitas la VM del Lab 1 ni su carpeta.

---

## 🛠️ Requisitos

| Componente | Herramienta |
|------------|-------------|
| Control node (donde escribes) | Tu máquina anfitriona Linux |
| Managed node (lo que configuras) | La VM **de este módulo** (`vagrant up` aquí) |
| Conexión | SSH puerto **2202** (ya fijado en el Vagrantfile) |
| Herramienta | `ansible-core` + `ansible` (Python) |

### 1. Instalar Ansible en el control node

```bash
python3 -m venv ~/ansible-venv
source ~/ansible-venv/bin/activate
pip install --upgrade pip
pip install ansible
ansible --version
```

> Activa el venv en cada sesión: `source ~/ansible-venv/bin/activate`.

### 2. Levantar el "servidor" de este módulo (VM propia)

```bash
cd lab3_planificacion_CPU/opcional_ansible
vagrant up
```

> La VM se llama `vm-layout-ansible` y usa el puerto **2202**, así que puede convivir con la del Lab 1 (puerto 2222). Guarda la clave SSH de Vagrant en el agente para que Ansible no pida contraseña:

```bash
ssh-add ~/.vagrant.d/insecure_private_key
```

---

## 🧠 Marco conceptual (5 minutos)

| Concepto | Qué es |
|----------|--------|
| **Control node** | La máquina donde instalas Ansible y ejecutas comandos. |
| **Managed node** | La máquina que Ansible configura… **a través de SSH**. Sin agente. |
| **Inventario** | Lista de hosted nodes y sus datos de conexión. |
| **Módulo** | Pieza de acción atómica (`apt`, `shell`, `cron`, `service`…). |
| **Playbook** | Archivo YAML que encadena tareas (módulos) sobre unos hosts. |
| **Idempotencia** | Ejecutar N veces produce el mismo estado; solo cambia lo que faltaba. |

```text
 [ tu laptop / control ] --SSH:2202--> [ vm-layout-ansible / managed ]
   ansible -m ping                       (solo Python + SSH en la VM)
```

> 💡 **La clave:** Ansible describe el **estado deseado**, no los pasos. "Me aseguro de que `htop` esté instalado" → si ya está, no hace nada.

---

## Paso 1 — Inventario y conectividad

El archivo `inventario.ini` ya apunta a la VM de este módulo:

```ini
[novatech]
vm-ansible ansible_host=127.0.0.1 ansible_port=2202 ansible_user=vagrant
```

Prueba la conexión:

```bash
ansible -i inventario.ini -m ping novatech
```

```text
vm-ansible | SUCCESS => { "changed": false, "ping": "pong" }
```

---

## Paso 2 — Idempotencia: las herramientas del curso

```yaml
# playbooks/herramientas.yml
---
- name: Asegurar herramientas de Sistemas Operativos
  hosts: novatech
  become: true

  tasks:
    - name: Actualizar índice de paquetes
      ansible.builtin.apt:
        update_cache: true

    - name: Instalar herramientas base del curso
      ansible.builtin.apt:
        name:
          - build-essential
          - htop
          - strace
          - procps
          - tree
        state: present
```

```bash
ansible-playbook -i inventario.ini playbooks/herramientas.yml
```

**Ejecútalo una segunda vez.** Observa `Play recap`:

- 1ª vez: `changed=2` (actualizó + instaló)
- 2ª vez: `changed=0` → nada que hacer, el estado deseado ya se cumple.

> **📄 Entregable:** captura de las dos ejecuciones + frase explicando la idempotencia.

---

## Paso 3 — 🎯 Prep del Lab 3A: despliega carga sintética por control remoto

Este playbook replica el **paso A.1 del Lab 3A** (`sha256sum /dev/urandom`) pero lanzándolo en el servidor desde tu control node, con tres variantes de prioridad:

```bash
ansible-playbook -i inventario.ini playbooks/preparacion_3A.yml
```

El playbook (contenido en `playbooks/preparacion_3A.yml`) lanza:

| Proceso | Cómo se lanza | Qué enseña del Lab 3A |
|---------|---------------|------------------------|
| `sha256sum` | normal | estado por defecto (`ni=0`) |
| `sha256sum` | `nice -n 10` | A.2 degradar prioridad |
| `sha256sum` | `taskset -c 0` | A.4 afinidad de CPU |

Y al final imprime `ps -eo pid,ni,pri,comm`, la misma tabla que usarás en la clase.

### Practica como en el Lab 3A, pero sobre el "parque de servidores"

Con la carga viva, un solo comando central consulta todos los nodos:

```bash
# A.1 — prioridades de toda la flota
ansible -i inventario.ini novatech -m shell -a "ps -eo pid,ni,pri,comm --sort=-ni | head"

# A.3 — política de planificación del último sha256sum
ansible -i inventario.ini novatech -m shell -a "chrt -p \$(pgrep -n sha256sum)"

# A.4 — afinidad de CPU
ansible -i inventario.ini novatech -m shell -a "taskset -pc \$(pgrep -n sha256sum)"
```

Limpia la carga cuando termines:

```bash
ansible -i inventario.ini novatech -m shell -a "pkill -f sha256sum || true"
```

> **📄 Entregable:** captura de la tabla `ps` que imprime el playbook y de al menos un ad-hoc (`chrt` o `taskset`). La clave: *mismo resultado que en el Lab 3A, pero sin entrar por SSH a la máquina*.

---

## Paso 4 — 🎯 Prep del Lab 3B: despliega y depura la simulación

Este paso te adelanta el **bug del Lab 3B** y lo convierte en un mini-pipeline de DevOps: *editas el código en tu control node → lo despliegas con un comando → verificas la salida en el servidor*.

### 4.1 Despliega y ejecuta la simulación

```bash
ansible-playbook -i inventario.ini playbooks/simulacion_3B.yml
```

El playbook:
1. Copia `files/scheduler_sim.py` → `/home/vagrant/laboratorios/` del servidor.
2. Ejecuta `python3 scheduler_sim.py`.
3. Muestra la salida completa.

**Observa:** los bloques `FCFS` y `SJF` son **idénticos** (espera 8.75, retorno 15.25). Ese es el bug que corregirás en el Lab 3B: `sjf()` está copiado de `fcfs()`.

### 4.2 Mini-CI de DevOps: corrige el `sjf()` y vuélvelo a desplegar

1. Edita `files/scheduler_sim.py` en tu **control node** (en la carpeta local del módulo).
2. Corrige `sjf()`: en cada paso, elige el proceso de **menor ráfaga entre los ya llegados**.
3. Redespliega y verifica:

```bash
ansible-playbook -i inventario.ini playbooks/simulacion_3B.yml
```

4. Confirma que ahora SJF **mejora** los promedios (espera 7.75, retorno 14.25).

> Verifica que el cambio llegó al servidor con un checador de idempotencia/estado:
>
> ```bash
> ansible -i inventario.ini novatech -m command -a "md5sum /home/vagrant/laboratorios/scheduler_sim.py"
> ```
>
> Compara el hash con tu archivo local: `md5sum files/scheduler_sim.py`. Si coinciden, lo que viste desplegado es exactamente tu código corregido.

> **📄 Entregable:** captura de la salida inicial (FCFS = SJF) y de la salida tras tu corrección (SJF mejor que FCFS) + el hash `md5sum` de ambos lados coincidiendo. *La práctica de "desplegar y verificar" es exactamente lo que hace un equipo de operaciones con CI/CD.*

---

## Paso 5 — Handlers: solo actuar cuando algo cambió

Los **handlers** son tareas que se ejecutan únicamente si otra tarea las "notificó" (porque cambió algo).

```bash
ansible-playbook -i inventario.ini playbooks/balanceo.yml
```

Ejecútalo dos veces. La primera vez la tarea `cron` cambia la configuración → `notify` dispara `Reiniciar cron`. La segunda vez no hay cambios → cron **no** se reinicia.

> **📄 Entregable:** captura mostrando que el handler corre la 1ª vez y NO la 2ª.

---

## 🤖 ¿Por qué Ansible y Terraform siguen siendo relevantes en la era de la IA?

Pareciera que "la IA lo configura todo solo y ya no hace falta aprender herramientas". La realidad es la contraria:

### 1. La IA se ejecuta sobre infraestructura
Entrenar un modelo es un *clúster* de GPUs: miles de servidores que nadie configura a mano. **Terraform crea el parque de máquinas** (las "hace existir") y **Ansible las configura** (instala drivers, dependencias, servicios). Sin automatización no hay IA funcionando a escala.

### 2. Código declarativo = memoria del estado
Que la infraestructura viva en un repositorio la hace **versionada, auditable y reproducible**: puedes reconstruir el clúster de ayer exactamente igual hoy, y el historial de git dice *quién cambió qué y cuándo*. Es condición para cualquier sistema confiable, IA incluida.

### 3. La IA escribe la infraestructura; tú dictas la calidad
Copilot o los LLMs hoy *escriben* Ansible/Terraform con facilidad. Pero si no entiendes **idempotencia, drift, secretos y seguridad**, no puedes revisar ese código generado → y delegar sin revisar produce caídas y agujeros de seguridad. **Dominar IaC te convierte en la persona que dirige a la IA, no en la que es dirigida.** La demanda es de quien *audita*, no de quien *teclea*.

### 4. Seguridad y costos como código
Con millonarios clústeres de GPUs, los costos importan: el código permite **dimensionar hacia abajo**, etiquetar recursos y no dejar servidores olvidados pagando. Las políticas de seguridad (RBAC, secretos, compliance) también se versionan. "Compliance as code" es más urgente cuando las máquinas se disparan solas.

### 5. Es la base del stack de MLOps
Kubernetes, pipelines de datos y MLOps heredan la misma filosofía de "estado deseado". Aprender Ansible/Terraform hoy = cimentar el stack completo de la informática moderna, incluida la IA.

> **Conclusión en una línea:** la IA **aumenta** el valor de la automatización: no reemplaza al ingeniero que sabe definir *estado deseado*; lo hace más productivo y necesario.

---

## ❓ Mini-cuestionario opcional

1. ¿Qué diferencia hay entre un script shell y un playbook de Ansible? (piensa en idempotencia y estado deseado)
2. ¿Por qué se dice que Ansible es *agent-less*?
3. ¿Qué papel juega `notify`/`handler` y qué trabajo innecesario evita?
4. *(Lab 3A)* ¿Qué valor de `ni` mostró la tabla `ps` para cada variante de proceso? ¿Dónde se refleja luego el `PRI`?
5. *(Lab 3B)* Tras corregir `sjf()`, ¿por qué SJF mejora el promedio de espera pero NO el de todos los procesos (P1 y P2 no cambian)? ¿Qué le pasaría a un proceso largo con SJF?
6. *(DevOps)* ¿Qué ventaja tiene "editar → desplegar → verificar" con Ansible frente a editar el archivo directamente en el servidor con `nano`? (piensa en versión, reproducibilidad y quién puede rehacer el paso)
7. *(IA)* Si una IA te genera un playbook, ¿qué debes revisar antes de desplegarlo a producción? Da un ejemplo concreto con los conceptos de este módulo.

---

## ✅ Checklist de entrega (si decides hacerlo)

- [ ] `vagrant up` del módulo (VM propia, sin Lab 1)
- [ ] `ansible -m ping` → SUCCESS
- [ ] `herramientas.yml` dos veces (idempotencia)
- [ ] `preparacion_3A.yml` + captura de tabla `ps`
- [ ] Ad-hoc `chrt` o `taskset` consultando la flota
- [ ] `simulacion_3B.yml`: salida inicial (FCFS = SJF) y salida tras corrección (SJF mejor)
- [ ] Hash `md5sum` coincidiendo en control node y servidor
- [ ] `balanceo.yml` dos veces (handler solo la 1ª)
- [ ] Mini-cuestionario respondido (incluye preguntas de 3B, DevOps e IA)
- [ ] Archivo a subir: `Apellido_Nombre_Ansible.pdf`

---

## 🏆 Rúbrica sugerida (bonificación)

| Componente | Puntos |
|------------|--------|
| VM propia + conectividad | 2 |
| Idempotencia demostrada y explicada | 3 |
| Prep Lab 3A: carga + ad-hoc de prioridades | 3 |
| Prep Lab 3B: despliegue, corrección de `sjf()` y verificación | 3 |
| Handlers y configuración | 2 |
| Reflexión sobre automatización + IA | 2 |
| **Total** | **15** |