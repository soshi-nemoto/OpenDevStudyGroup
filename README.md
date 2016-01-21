## Fabric workshop 

### fabfile.py
* Usage: 
    * $ fab help
      * $ fab -R {ROLE} [deploy|tags|change|remove}
* How to use.

    * Preparation (setup files)
        1. edit "Vagrantfile" and fix IP address of your vagrant machine.
            * {IP_ADDRESS_OF_YOUR_VAGRANT_MACHINE}
        1. edit "hosts" file to set IP address of the vagrant machine.
            * {IP_ADDRESS_OF_YOUR_VAGRANT_MACHINE}
        1. put ssh private key for github access to "fabric_files/resources/".
            * {IP_ADDRESS_OF_YOUR_VAGRANT_MACHINE}
            * {PRIVATE_KEY_FILE_FOR_GITHUB}
            * {PRIVATE_KEY_FILE_FOR_VAGRANT_MACHINE}
                * If you cannot find vagrant's key, please use 'vagrant ssh-config' after creating vagrant machine.
        1. edit "fabric_files/resources/ssh_config".
            * {PRIVATE_KEY_FILE_FOR_GITHUB}
        1. edit "fabric_files/resource.py".
            * {PRIVATE_KEY_FILE_FOR_GITHUB}
            * If you want to deploy your own source on github, please fix the value of "env.git['repository']"
        1. edit your ssh condig file (~/.ssh/config)
            * {IP_ADDRESS_OF_YOUR_VAGRANT_MACHINE}
            * {PRIVATE_KEY_FILE_FOR_VAGRANT_MACHINE}

```config:~/.ssh/config
Host *
    StrictHostKeyChecking no

Host {IP_ADDRESS_OF_YOUR_VAGRANT_MACHINE}
  User vagrant
  TCPKeepAlive yes
  IdentityFile {PRIVATE_KEY_FILE_FOR_VAGRANT_MACHINE}
  IdentitiesOnly yes
  ControlPersist 2h
```

    * Preparation (create vagrant machine)
        1. create vagrant machine
            * $ vagrant up
        1. do all provisions.(Ansible)
            * $ vagrant provision
                * If errors appear, repeat this step after fixing vagrat/ansible files.
                
    * Deploy
        1. deploy code to the machine from github.
            * $ fab -R {ROLE} deploy
                * Default ROLE name of this script is 'httpd-server' defined in 'hosts'.
            * ie "fab -R httpd-server deploy:branch=Ansible"

    
### Related files
* Fabric related files.
    * fabric_files/
      * resource.py : settings for the fabfile.py
      * resources/* : resource files
* Other files.
    * hosts : Ansible inventory file which used in fabric also.
    * Vagrantfile : Vagrant setting file
    * setup.yml   : Ansible file which are loaded in Vagrantfile.
    * playbooks/* : Ansible playbooks.
* for test
    * FABRIC_TEST/* : fabfiles for just testing in workshop.


### Note
* These python files are NOT so pythonic, to learn basic usage of Fabric for non-pythonist. If you can, please modify them for more pythonic codes. (decorator, contexts..)
