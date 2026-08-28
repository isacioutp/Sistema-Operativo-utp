terraform {
  required_providers {
    virtualbox = {
      source  = "terra-farm/virtualbox"
      version = "0.2.2-alpha.1"
    }
  }
}

resource "virtualbox_vm" "so_node" {
  name   = "vm-sistemas-operativos"
  image  = "https://app.vagrantup.com/ubuntu/boxes/bionic64/versions/20230607.0.1/providers/virtualbox.box"
  cpus   = 2
  memory = "2048 mib"

  user_data = file("${path.module}/scripts/setup_env.sh")

  network_adapter {
    type           = "hostonly"
    host_interface = "VirtualBox Host-Only Ethernet Adapter"
  }
}

output "vm_name" {
  value       = virtualbox_vm.so_node.name
  description = "Nombre de la Máquina Virtual creada"
}
