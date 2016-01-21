# add include path
import sys

# import ansible.inventory and fabric.api
sys.path.append('/usr/local/Cellar/ansible/1.9.4/libexec/lib/python2.7/site-packages')
sys.path.append('/usr/local/Cellar/ansible/1.9.4/libexec/vendor/lib/python2.7/site-packages')
from ansible import inventory

# import fabric libraries
from fabric.api import env, run, put, cd
from fabric.contrib import files

# set Ansible inventory settings to Fabric role.
inventory = inventory.Inventory('./hosts')
env.roledefs = inventory.groups_list()
env.use_ssh_config = True

# command
def mkdir_cd_and_put():
    if not files.exists('TMP'):
        run('mkdir -p TMP')
    with cd('TMP'):
        if not files.exists('hosts'):
            put('hosts','./')
        run('pwd')
        run('ls -al')

# How to call
# $ fab -R {ROLE} -f fabfie_3.py remotetest
# -> {ROLE} should be defined in 'hosts' file.
      
