variable "box_source" {
  type        = string
  default     = "./focal-server-cloudimg-amd64-vagrant.box"
  description = "Ruta local o URL remota del archivo .box para la imagen de VirtualBox"
}

variable "vm_cpus" {
  type        = number
  default     = 2
  description = "Número de núcleos de CPU para la VM"
}

variable "vm_memory" {
  type        = string
  default     = "2048 mib"
  description = "Cantidad de memoria RAM asignada a la VM"
}
