# Laboratorio 1: Preparación del Entorno Linux para Sistemas Operativos

## 📌 Objetivo
Desplegar y verificar la máquina virtual de trabajo que se utilizará a lo largo del semestre mediante Infraestructura como Código (**IaC**).

---

## 🛠️ Requisitos Previos
Tener instalados en el sistema anfitrión:
* **VirtualBox** (v6.1 o superior)
* **Vagrant** o **Terraform**

---

## 🚀 OPCIÓN A: Despliegue con Terraform (Recomendado)

1. Abre la terminal en esta carpeta e inicializa los proveedores:
   ```bash
   terraform init
Auditoría e Inspección del Plan (Paso Obligatorio):
Genera y revisa el plan de ejecución para verificar la infraestructura antes de aplicar cambios:

Bash
terraform plan
Despliega la máquina virtual:

Bash
terraform apply -auto-approve

💡 Nota (Uso de archivo .box local):
Si descargaste previamente la imagen localmente (.box) para evitar consumo de red, puedes pasar el parámetro al plan y al apply:

Bash
terraform plan -var="box_source=./ubuntu-bionic.box"
terraform apply -var="box_source=./ubuntu-bionic.box" -auto-approve
Para destruir la infraestructura al finalizar:

Bash
terraform destroy -auto-approve
🚀 OPCIÓN B: Despliegue directo con Vagrant
Inicia y aprovisiona la VM:

Bash
vagrant up
(Si utilizas un archivo .box local, edita la línea config.vm.box_url dentro del Vagrantfile).

Accede a la máquina virtual vía SSH:

Bash
vagrant ssh
Para apagar o eliminar la VM:

Bash
vagrant halt    # Apagar
vagrant destroy # Eliminar
🔬 Verificación del Entorno en la VM
Una vez dentro de la Máquina Virtual (vía SSH):

Dirígete a la carpeta de trabajo del curso:

Bash
cd ~/laboratorios/unidad1
Ejecuta el binario de prueba compilado durante el aprovisionamiento:

Bash
./test_proc
Confirma la instalación de las herramientas de inspección ejecutando:

Bash
gcc --version
make --version
strace -V
htop --version

📤 Entrega
Completa la información en plantilla_entrega.md, adjunta las capturas requeridas de la verificación del entorno y sube los cambios a tu repositorio personal.
