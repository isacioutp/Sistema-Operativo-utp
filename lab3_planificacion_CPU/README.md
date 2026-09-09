# 📚 Laboratorio 3 — Planificación de CPU

> **Curso:** Sistemas Operativos (0689) · Grupo 1SF134
> **Unidad:** 2 — Gestión de Procesos y Procesador (2.4 Planificación de Procesos)
> **Enfoque:** cada guía está diseñada para que resuelvas el laboratorio **aprendiendo en el proceso** (anticipa → ejecuta → compara → interpreta).

---

## 📖 Estructura y recorrido sugerido

| # | Recurso | Contenido | ¿Cuándo? |
|---|---------|-----------|----------|
| 0 | `opcional_ansible/` | Módulo **opcional**: ensaya el 3A por control remoto y el 3B como mini-pipeline "edita → despliega → verifica" | **Antes** del 3A (bonus)
| 1 | `Teoria_Lab3A_Linux.pptx` | Teoría previa: nice, renice, chrt, taskset, políticas, CFS | Antes del 3A |
| 2 | `Laboratorio3A_Planificacion_Linux.md` | Gestión de prioridades y planificación **real** en Linux (caso NovaTech) | Laboratorio 3A |
| 3 | `Teoria_Lab3B_Algoritmos.pptx` | Teoría previa: FCFS, SJF, Round Robin, métricas | Antes del 3B |
| 4 | `Laboratorio3B_Simulacion_Algoritmos.md` | Simulación y comparación de algoritmos (caso NovaTech) | Laboratorio 3B |

> **Flujo pedagógico:** primero **ensayas sin manos** (opcional Ansible: carga del 3A y pipeline de despliegue del 3B) → luego **manipulas el kernel real** (3A) → por último **compruebas algebraicamente** cuál algoritmo conviene (3B). No es casual: cada parte justifica la siguiente.

---

## 🧩 Resumen de los laboratorios

### Laboratorio 3A — Planificación real en Linux
Caso *"El servidor de NovaTech se está incendiando"*: aprendes a diagnosticar (`ni`/`pri`), degradar (`nice`/`renice`), consultar políticas (`chrt`) y anclar procesos (`taskset`) como haría un sysadmin ante un servidor saturado.
- **Aprenderás:** por qué `NI` y `PRI` son distintos, la regla de permisos (y su motivo de seguridad), y cómo CFS decide de verdad.
- **Entregas:** evidencias por fase + cuestionario técnico. **25 pts.**

### Laboratorio 3B — Simulación de algoritmos
Caso *"NovaTech necesita elegir un planificador"*: simulas FCFS, SJF y Round Robin sobre una carga de 4 reportes y produces una **recomendación con datos** para la gerencia.
- **Aprenderás:** a calcular espera/retorno, a corregir un `sjf()` con un bug intencional, el efecto del quantum y por qué CFS no es "de libro".
- **Entregas:** `scheduler_sim.py` corregido + informe + cuestionario. **40 pts.**

### Módulo opcional — Ansible (bonus)
Prepara los **dos** laboratorios: despliega la carga sintética del 3A (`sha256sum`, `nice -n 10`, `taskset -c 0`) en un "servidor" propio (VM incluida, sin depender del Lab 1), y despliega/ejecuta la simulación del 3B en el servidor (`scheduler_sim.py`), mostrando el bug de `sjf()` y funcionando como mini-pipeline de *edita → despliega → verifica*. Además aborda la pregunta: *¿por qué Ansible/Terraform siguen siendo relevantes en la era de la IA?*
- **Bonus:** hasta 15 pts.

---

## 🔗 Conexión con los otros laboratorios

- **Lab 1** te dio la VM y el entorno (gcc, make, strace, htop).
- **Lab 2** te enseñó procesos, señales y `/proc`.
- **Lab 3A** usa esa VM para manipular la planificación real.
- **Lab 3B** cierra con la teoría matemática de los algoritmos.
- **Opcional Ansible** refuerza automatización y te prepara para 3A.

---

## ✅ Checklist por laboratorio

### Lab 3A
- [ ] VM del Lab 1 operativa
- [ ] `util-linux` instalado
- [ ] Autocomprobación (sección "¿Cómo sé que lo hice bien?") cumplida
- [ ] Evidencias de las 5 fases
- [ ] Cuestionario respondido
- [ ] Nombre: `Apellido_Nombre_Lab3A.pdf`

### Lab 3B
- [ ] Python 3.8+
- [ ] Timeline verificado a mano en papel
- [ ] `sjf()` corregido y autocomprobación cumplida
- [ ] Tabla comparativa + informe a la gerencia
- [ ] Cuestionario respondido
- [ ] Nombre: `Apellido_Nombre_Lab3B.pdf` + `.py`

### Opcional Ansible
- [ ] `vagrant up` en `opcional_ansible/` (VM propia)
- [ ] `ansible -m ping` → SUCCESS
- [ ] Idempotencia (herramientas 2 veces) y handlers (balanceo 2 veces)
- [ ] Prep 3A: carga + tabla `ps` + ad-hoc `chrt`/`taskset`
- [ ] Prep 3B: `simulacion_3B.yml` antes y después de corregir `sjf()` (+ `md5sum` en ambos lados)
- [ ] Mini-cuestionario (incluye preguntas de 3B, DevOps e IA)
- [ ] Nombre: `Apellido_Nombre_Ansible.pdf`