Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

  config.vm.define :cloud_sim do |cloud_sim|
    cloud_sim.vm.box = "generic/ubuntu2004"
  end
end
