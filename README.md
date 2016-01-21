## Fabric workshop 

### fabfile.py
* Usage: 
    * $ fab help
      * $ fab -R {ROLE} [deploy|tags|change|remove}
* How to use.

    * Preparation (see. Preparation_for_Fabric2.pdf)
        1. edit "Vagrantfile" and fix IP address of your vagrant machine.
        1. edit "hosts" file to set IP address of the vagrant machine.
put ssh private key for github access to "fabric_files/resources/".
        1. — create Vagrant machine —
        1. edit "fabric_files/resources/ssh_config".
        1. edit "fabric_files/resource.py".
        1. edit your ssh condig file (~/.ssh/config : on local)
                
    * Deploy
        1. test this deploy tool
            * $ fab help
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
