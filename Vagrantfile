# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|

  config.vm.box = "precise64"

  config.vm.customize [
    "modifyvm",
    :id,
    "--memory",
     2048,
    "--cpus",
    2
  ]

end
