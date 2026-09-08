# 📦 Módulo opcional — Ansible: automatizando a NovaTech

> **Curso:** Sistemas Operativos (0689) · Grupo 1SF134
> **Docente:** Isacio Manuel Tamayo Rodríguez
> **Modalidad:** Opcional · Bonus · Independiente del laboratorio
> **Estimado:** 1h – 1h30

---

## 🤔 ¿De qué va este módulo?

Los laboratorios 1 y 3A te mostraron cómo *provisionar* una máquina (Vagrant/Terraform) y cómo *comprender* la planificación de CPU. Este módulo es **totalmente independiente**: te introduce a **Ansible**, la herramienta de automatización de configuración que usa un equipo de operaciones real para que 500 servidores queden configurados *igual* sin tocar cada uno a mano.

> 🏢 **Contexto NovaTech:** después de la crisis del servidor, el equipo decidió que "ya no vamos a configurar máquinas a mano". Te piden investigar Ansible y dejar un primer playbook que replique la configuración del Lab 1 en cualquier servidor nuevo.

No evalúa el laboratorio 3. Si lo entregas, suma **bonificación** y demuestra dominio de automatización (muy valorado en entrevistas).

---

## 🎯 Objetivos

- Entender el modelo **agente-less** de Ansible (control node → managed nodes por SSH).
- Escribir un **inventario** y probar conectividad con `ansible -m ping`.
- Crear un **playbook** idempotente que instale las herramientas del curso.
- Demostrar **idempotencia**: ejecutar el mismo playbook dos veces y ver que la segunda no "cambia" nada.
- Usar **handlers** y módulos de configuración (`lineinfile`, `cron`, `service`).

---

## 🛠️ Requisitos

| Componente | Herramienta |
|------------|-------------|
| Control node (donde escribes) | Tu máquina anfitriona Linux, o la VM del Lab 1 |
| Managed node (lo que configuras) | La VM del Lab 1 (Ubuntu Bionic) funcionando |
| Conexión | SSH desde el control hacia la VM |
| Herramienta | `ansible-core` + `ansible` (paquetes Python) |

### Instalar Ansible (en el control node)

Recomendado con `pip` en un entorno aislado (Ubuntu 24.04 ya no trae `ansible` en `apt`):

```bash
python3 -m venv ~/ansible-venv
source ~/ansible-venv/bin/activate
pip install --upgrade pip
pip install ansible
ansible --version
```

> Si tu control node es la propia VM del Lab 1, recuerda activar el venv en cada sesión (`source ~/ansible-venv/bin/activate`).

---

## 🧠 Marco conceptual (5 minutos)

| Concepto | Qué es |
|----------|--------|
| **Control node** | La máquina donde instalas Ansible y ejecutas comandos. |
| **Managed node** | La máquina que Ansible configura... ¡a través de SSH! Sin agente instalado en ella. |
| **Inventario** | Lista de los managed nodes (hosts) y sus datos de conexión. |
| **Módulo** | Pieza de acción atómica (`apt`, `cron`, `lineinfile`, `service`...). |
| **Playbook** | Archivo YAML con la lista de tareas (módulos) a ejecutar sobre los hosts. |
| **Idempotencia** | Ejecutar la misma configuración N veces produce el mismo estado final; solo cambia lo que hizo falta. |

```text
 [ Tu laptop / control ] --SSH--> [ VM del Lab 1 / managed ]
   ansible -m ping                    (solo necesita Python y SSH)
```

> 💡 **La clave:** Ansible describe el **estado deseado**, no los pasos. "Me aseguro de que `htop` esté instalado" → si ya está, no hace nada.

---

## Paso 1 — Levanta la VM del Lab 1

```bash
cd lab1-preparacion-entorno
vagrant up
```

Ansible se conectará a ella por SSH. Para probar la conexión manualmente:

```bash
vagrant ssh -c "echo conectado"
```

---

## Paso 2 — Inventario

Crea el archivo `inventario.ini` (ya está preparado en `lab_opcional_ansible/`):

```ini
[novatech]
vm-novatech ansible_host=127.0.0.1 ansible_port=2222 ansible_user=vagrant
```

> ⚠️ El puerto puede variar si tienes varias VMs. Averigua el tuyo con `vagrant ssh-config | grep Port`.

### Probar conectividad

```bash
ansible -i inventario.ini -m ping novatech
```

Resultado esperado (primera vez pedirá aceptar la huella SSH o fallará por clave):

```text
vm-novatech | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

> 🔧 *Tip:* si pide contraseña o falla la autenticación, añade la clave de Vagrant al agente:
> `ssh-add ~/.vagrant.d/insecure_private_key`

---

## Paso 3 — Primer playbook: las herramientas del curso

Este playbook replica exactamente lo que hacía `scripts/setup_env.sh` del Lab 1… pero **declarativamente**.

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

Ejecuta:

```bash
ansible-playbook -i inventario.ini playbooks/herramientas.yml
```

### 🧪 Experimento de idempotencia

**Ejecútalo una segunda vez.** Observa las columnas:

```text
PLAY RECAP
vm-novatech : ok=3    changed=0    ...   ← la segunda vez NO cambia nada
```

- Primera ejecución: `changed=2` (actualizó índices + instaló paquetes).
- Segunda ejecución: `changed=0` — todo "ok" porque el estado deseado ya se cumple.

> **📄 Entregable:** captura de las DOS ejecuciones y una frase explicando por qué la segunda no cambia nada.

---

## Paso 4 — Configuración idempotente + handlers

Ahora configura herramientas de gestión usando módulos finos (`cron`, `service`) y un **handler** (tarea que solo corre si un cambio la dispara).

```yaml
# playbooks/balanceo.yml
---
- name: Programar balanceo nocturno del servicio de recomendaciones
  hosts: novatech
  become: true

  tasks:
    - name: Crear script de balanceo de carga
      ansible.builtin.copy:
        content: |
          #!/bin/bash
          echo "Balanceando carga de recomendaciones (simulación)…"
        dest: /usr/local/bin/balancear.sh
        mode: "0755"

    - name: Añadir tarea nocturna a cron
      ansible.builtin.cron:
        name: "Balanceo nocturno recomendaciones"
        minute: "30"
        hour: "2"
        job: "/usr/local/bin/balancear.sh"
      notify: Reiniciar cron

  handlers:
    - name: Reiniciar cron
      ansible.builtin.service:
        name: cron
        state: restarted
```

Ejecuta dos veces:

```bash
ansible-playbook -i inventario.ini playbooks/balanceo.yml
```

Observa:
1. Con `notify`/handler: el `service` solo se reinicia **cuando la tarea de cron cambió algo**. En la segunda ejecución no hay cambios → cron **no** se reinicia.
2. Tarea con `content:` → idempotente: aunque la reescribas, no informa "changed" si el contenido es idéntico.

> **📄 Entregable:** captura mostrando que el handler NO se ejecuta en la segunda corrida, y explica por qué.

---

## Paso 5 — Un ad-hoc que conecta con el Lab 3A

Ansible también sirve para operaciones puntuales. Vuelve al caso del servidor lento:

```bash
ansible -i inventario.ini novatech -m shell -a "ps -eo pid,ni,pri,comm --sort=-ni | head"
```

Esto consulta las prioridades de todos los "servidores" desde tu control node. Nota cómo un solo comando permite inspeccionar **un parque completo** de máquinas, no solo una.

> **📄 Entregable:** captura de la salida y una frase sobre qué ventaja tiene esto frente a conectarse con `ssh` a cada máquina.

---

## ❓ Mini-cuestionario opcional

1. ¿Qué diferencia hay entre Ansible y un script shell como `setup_env.sh`? Piensa en idempotencia y en el "estado deseado".
2. ¿Por qué se dice que Ansible es *agent-less*? ¿Qué necesita instalado el managed node?
3. ¿Qué papel juega el `notify`/`handler` y por qué evita trabajo innecesario?
4. Ansible, Vagrant y Terraform pueden parecer "lo mismo". ¿Cuándo usarías cada uno en la vida de un servidor?

---

## ✅ Checklist de entrega (si decides hacerlo)

- [ ] Inventario funcionando (`ansible -m ping` → SUCCESS)
- [ ] Captura de `herramientas.yml` ejecutado dos veces (idempotencia)
- [ ] Captura de `balanceo.yml` con handler ejecutado solo la primera vez
- [ ] Captura del ad-hoc del Paso 5
- [ ] Mini-cuestionario respondido

---

## 🏆 Rúbrica sugerida (bonificación)

| Componente | Puntos |
|------------|--------|
| Inventario y conexión | 2 |
| Idempotencia demostrada y explicada | 3 |
| Handlers y módulos de configuración | 3 |
| Ad-hoc + reflexión sobre automatización | 2 |
| **Total** | **10** |