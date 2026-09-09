# Sistemas Operativos (0689)

> **Grupo 1SF134 · II Semestre 2026 · Prof. Isacio Manuel Tamayo Rodríguez**
> **Horario:** Miércoles (teoría) · Viernes (teoría + laboratorio)

Repositorio del curso de Sistemas Operativos — 100% Linux, con laboratorios semanales, proyecto semestral de IaC y el parcial único basado en Bandit.

---

## Estructura del repositorio

```
Sistema-Operativo-utp/
├── lab1-preparacion-entorno/        # VM, Terraform/Vagrant, verificación
├── lab2_proceso_senales/            # Procesos, señales, /proc
├── lab3_planificacion_CPU/          # Planificación real (3A) + simulación (3B)
│   └── opcional_ansible/            # Bonus: Ansible (prep 3A/3B)
├── lab4_hilos_hebras/               # Procesos ligeros, pthreads
├── lab5_gestion_memoria/            # Memoria, valgrind, swap
├── lab6_sistema_archivos/           # Inodos, permisos, montaje
├── lab7_entrada_salida/             # Drivers, E/S, disco
├── semestral/                       # Proyecto: 10 variaciones IaC
├── herramientas/                    # Scripts utilitarios
├── PLAN_SEMESTRE.md                 # Calendario completo (17 semanas)
└── README.md                        # Este archivo
```

---

## Laboratorios

| Lab | Tema | Módulo | Pts | Estado |
|-----|------|--------|-----|--------|
| Lab 1 | Preparación del entorno Linux | I | — | Completado |
| Lab 2 | Procesos, señales y `/proc` | I | — | Completado |
| Lab 3A | Planificación real en Linux | I | 25 | Completado |
| Lab 3B | Simulación de algoritmos de planificación | I | 40 | Completado |
| Opcional | Ansible (bonus) | I–III | 15 | Completado |
| Lab 4 | Procesos ligeros / Hebras | I | 25 | Creado |
| Lab 5 | Gestión de Memoria | II | 35 | Creado |
| Lab 6 | Sistema de Archivos | III | 35 | Creado |
| Lab 7 | Entrada/Salida y Almacenamiento | III | 30 | Creado |
| **Total laboratorios** | | | **190 + 15 bonus** | |

---

## Evaluaciones

| Evaluación | Descripción | Puntos |
|------------|-------------|--------|
| Laboratorios semanales | Labs 3A, 3B, 4, 5, 6, 7 | 190 |
| Proyecto Semestral | 10 variaciones de IaC (Terraform/Vagrant/Ansible/Bash) | 100 |
| Bandit | Parcial único — niveles 1–20 (todo el semestre para entregar) | Único parcial |
| Opcional Ansible | Bonus | 15 |

---

## Metodología

Cada laboratorio sigue el ciclo **AE-CI**:

```
ANTICIPA → EJECUTA → COMPARA → INTERPRETA
```

- **Parte A (Miércoles):** teoría + diagnóstico
- **Parte B (Viernes):** práctica aplicada (caso NovaTech)

---

## Requisitos del entorno

- VirtualBox 6.1+
- Terraform o Vagrant
- Ubuntu/Debian (recomendado)
- Herramientas: `gcc`, `make`, `strace`, `htop` (se verifican en Lab 1)

---

## Referencia rápida

- [Plan completo del semestre](PLAN_SEMESTRE.md)
- [Proyecto Semestral (10 variaciones IaC)](semestral/SEMESTRAL.md)
- [Guía oficial del proyecto (PDF)](Proyecto%20Semestral%2010%20Variaciones%20de%20Implementaci%C3%B3n%20con%20Infraestructura%20como%20C%C3%B3digo%20(IaC).pdf)

---

## Formato de entrega

- **Laboratorios:** `Apellido_Nombre_LabN.pdf` (+ `.c`/`.py` si aplica)
- **Proyecto:** `Apellido_Nombre_Proyecto.pdf` + carpeta con código IaC
- **Evidencias:** capturas legibles con `PS1` personalizado

---

## Calendario resumido

| Sem | Lab | Bandit sugerido |
|-----|-----|-----------------|
| 1–3 | Labs 1, 2, 3 | — |
| 4 | Lab 4 — Hilos | N1–5 |
| 5–6 | Lab 5 — Memoria | N6–10 |
| 7–8 | Lab 6 — Archivos | N11–14 |
| 9–10 | Lab 7 — E/S | N15–18 |
| 11 | Presentación proyecto | N19 |
| 12–13 | Tutoría (feriados) | N20 |
| 14 | Tutoría proyecto | N20 |
| 15 | **Entrega Bandit** | ✅ |
| 16 | **Entrega Proyecto + Sustentación** | — |
| 17 | Cierre y notas | — |
