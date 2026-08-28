#!/bin/bash
# Aprovisionamiento del entorno de desarrollo para Sistemas Operativos

export DEBIAN_FRONTEND=noninteractive

echo "===> 1. Actualizando repositorios e instalando herramientas base..."
apt-get update -y
apt-get install -y \
    build-essential \
    gcc \
    make \
    gdb \
    procps \
    htop \
    tree \
    lsof \
    strace \
    curl \
    git \
    vim

echo "===> 2. Creando estructura de directorios del curso..."
mkdir -p /home/vagrant/laboratorios/unidad1
cd /home/vagrant/laboratorios/unidad1

echo "===> 3. Creando programa de prueba de entorno (demo_proc)..."
cat << 'C_CODE' > test_env.c
#include <stdio.h>
#include <unistd.h>

int main() {
    printf("=========================================\n");
    printf(" ¡ENTORNO DE SISTEMAS OPERATIVOS LISTO!  \n");
    printf(" PID del proceso: %d                     \n", getpid());
    printf("=========================================\n");
    return 0;
}
C_CODE

echo "===> 4. Compilando programa de prueba..."
gcc test_env.c -o test_proc

echo "===> 5. Ajustando permisos de usuario..."
chown -R vagrant:vagrant /home/vagrant/laboratorios

echo "===> ¡Aprovisionamiento completado con éxito!"
