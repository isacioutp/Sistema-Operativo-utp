# Laboratorio 1: Preparación del Entorno Linux para Sistemas Operativos

## 📌 Objetivo
Desplegar y verificar la máquina virtual de trabajo que se utilizará a lo largo del semestre para la ejecución de prácticas de C, kernel, gestión de memoria y llamadas al sistema.

---

## 🛠️ Requisitos Previos
Tener instalados en el sistema anfitrión:
* **VirtualBox** (v6.1 o superior)
* **Vagrant** o **Terraform**

---

## 🚀 OPCIÓN A: Despliegue con Terraform (Recomendado)

1. Abre la terminal en esta carpeta e inicializa Terraform:
   ```bash
   terraform init



1. Despliega la máquina virtual:

   Bash

   ```
   terraform apply -auto-approve
   ```

2. Para acceder a la VM o destruirla cuando termines:

   Bash

   ```
   # Destruir cuando finalices la práctica:
   terraform destroy -auto-approve
   ```

## 🚀 OPCIÓN B: Despliegue directo con Vagrant

Si prefieres usar Vagrant directamente:

1. Inicia y aprovisiona la VM:

   Bash

   ```
   vagrant up
   ```

2. Accede a la máquina virtual vía SSH:

   Bash

   ```
   vagrant ssh
   ```

3. Para apagar o eliminar la VM:

   Bash

   ```
   vagrant halt    # Apagar
   vagrant destroy # Eliminar
   ```

## 🔬 Verificación del Entorno en la VM

Una vez dentro de la Máquina Virtual (vía SSH):

1. Dirígete a la carpeta de trabajo del curso:

   Bash

   ```
   cd ~/laboratorios/unidad1
   ```

2. Ejecuta el binario de prueba compilado durante el aprovisionamiento:

   Bash

   ```
   ./test_proc
   ```

3. Confirma la instalación de las herramientas de inspección ejecutando:

   Bash

   ```
   gcc --version
   make --version
   strace -V
   htop --version
   ```

## 
