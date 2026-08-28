# Laboratorio 1: Preparación del Entorno Linux para Sistemas Operativos

## 📌 Objetivo

Desplegar y verificar la máquina virtual de trabajo que se utilizará durante el semestre.

Al finalizar este laboratorio, el estudiante deberá ser capaz de:

* Desplegar una máquina virtual Linux.
* Verificar que el entorno funciona correctamente.
* Acceder a la máquina virtual mediante SSH.
* Comprobar las herramientas necesarias para los laboratorios.
* Ejecutar un programa de prueba.
* Documentar la evidencia de la preparación del entorno.

---

## 🛠️ Requisitos previos

El sistema anfitrión debe tener instalados:

* **VirtualBox 6.1 o superior**
* **Terraform**
* **Vagrant**

> El estudiante puede utilizar **Terraform** o **Vagrant**, según la opción indicada por el docente.

---

# 🚀 Opción A: Despliegue con Terraform

## 1. Abrir la carpeta del laboratorio

Abre una terminal y dirígete a la carpeta donde descargaste el laboratorio:

```bash
cd laboratorio-1
```

Comprueba su contenido:

```bash
ls -la
```

---

## 2. Inicializar Terraform

Ejecuta:

```bash
terraform init
```

---

## 3. Revisar el plan

> ⚠️ **Paso obligatorio**

Antes de crear la máquina virtual, ejecuta:

```bash
terraform plan
```

Revisa los recursos que Terraform indica que serán creados.

---

## 4. Crear la máquina virtual

Si el laboratorio utiliza la imagen configurada por defecto:

```bash
terraform apply -auto-approve
```

Espera hasta que Terraform finalice correctamente.

---

# 📦 Uso de una imagen `.box` local

Si el docente te proporciona el archivo:

```text
ubuntu-bionic.box
```

colócalo **en la carpeta principal del laboratorio**, junto con los archivos de configuración.

Ejemplo:

```text
laboratorio-1/
├── main.tf
├── variables.tf
├── outputs.tf
├── Vagrantfile
├── ubuntu-bionic.box
└── plantilla_entrega.md
```

### Si utilizas Terraform

Si la configuración del laboratorio permite seleccionar la imagen mediante `box_source`, utiliza:

```bash
terraform plan -var="box_source=./ubuntu-bionic.box"
```

Si el plan es correcto:

```bash
terraform apply -var="box_source=./ubuntu-bionic.box" -auto-approve
```

> 📌 **Importante:** El archivo debe llamarse exactamente `ubuntu-bionic.box` y estar en la ubicación indicada.

---

# 🚀 Opción B: Despliegue con Vagrant

Si utilizas Vagrant, coloca igualmente el archivo:

```text
ubuntu-bionic.box
```

en la carpeta del laboratorio.

La estructura será:

```text
laboratorio-1/
├── Vagrantfile
├── ubuntu-bionic.box
├── plantilla_entrega.md
└── ...
```

El `Vagrantfile` proporcionado por el docente está preparado para utilizar la imagen local.

Inicia la máquina virtual con:

```bash
vagrant up
```

Espera hasta que finalice el proceso de aprovisionamiento.

---

## 🔑 Acceder a la máquina virtual

Una vez creada la VM, ejecuta:

```bash
vagrant ssh
```

A partir de este momento, los siguientes comandos deben ejecutarse **dentro de la máquina virtual**.

---

# 🔬 Verificación del entorno

## 1. Ir a la carpeta del curso

Dentro de la máquina virtual:

```bash
cd ~/laboratorios/unidad1
```

Comprueba que estás en la ubicación correcta:

```bash
pwd
```

---

## 2. Ejecutar el programa de prueba

Ejecuta:

```bash
./test_proc
```

El programa debe ejecutarse correctamente.

📸 **Toma una captura de pantalla de este resultado.**

---

## 3. Verificar GCC

```bash
gcc --version
```

---

## 4. Verificar Make

```bash
make --version
```

---

## 5. Verificar Strace

```bash
strace -V
```

---

## 6. Verificar Htop

```bash
htop --version
```

---

# ✅ Lista de comprobación

| Elemento           | Comando                          | Verificado |
| ------------------ | -------------------------------- | :--------: |
| Máquina virtual    | `vagrant up` / `terraform apply` |      ☐     |
| Acceso a la VM     | `vagrant ssh`                    |      ☐     |
| GCC                | `gcc --version`                  |      ☐     |
| Make               | `make --version`                 |      ☐     |
| Strace             | `strace -V`                      |      ☐     |
| Htop               | `htop --version`                 |      ☐     |
| Programa de prueba | `./test_proc`                    |      ☐     |

---

# 📸 Evidencias

El estudiante debe presentar las siguientes capturas:

1. **Despliegue de la máquina virtual**

   * `terraform apply` o `vagrant up`.

2. **Plan de Terraform**

   * `terraform plan`, si utiliza Terraform.

3. **Acceso a la máquina virtual**

   * `vagrant ssh`.

4. **Ejecución del programa:**

```bash
./test_proc
```

5. **Verificación de las herramientas:**

```bash
gcc --version
make --version
strace -V
htop --version
```

---

# 📤 Entrega

Completa el archivo:

```text
plantilla_entrega.md
```

Incluye las capturas de pantalla solicitadas y responde las preguntas de la plantilla.

La entrega se realizará **según el mecanismo indicado por el docente**.

> **No es necesario realizar `git push`, `git commit` ni ninguna otra operación de Git para completar este laboratorio.**

---

# 🎯 Resultado esperado

Al finalizar el laboratorio, debes tener una **máquina virtual Linux funcionando correctamente**, con las herramientas necesarias para los próximos laboratorios de Sistemas Operativos:

* `gcc`
* `make`
* `strace`
* `htop`
* `test_proc`

La máquina virtual preparada será utilizada en los siguientes laboratorios del curso.
