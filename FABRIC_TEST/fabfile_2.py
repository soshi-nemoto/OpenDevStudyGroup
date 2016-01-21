# add include path
import sys

# import ansible.inventory and fabric.api
sys.path.append('/usr/local/Cellar/ansible/1.9.4/libexec/lib/python2.7/site-packages')
sys.path.append('/usr/local/Cellar/ansible/1.9.4/libexec/vendor/lib/python2.7/site-packages')
from ansible import inventory
from fabric.api import env, run

# import fabric libraries
inventory = inventory.Inventory('./hosts')
env.roledefs = inventory.groups_list()
env.use_ssh_config = True

# command
def remotetest():
      run('ls -al')

# How to call
# $ fab -R {ROLE} -f fabfie_2.py remotetest
# -> {ROLE} should be defined in 'hosts' file.
      
## Note
#  Please change library path for your environment.
