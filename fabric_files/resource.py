from fabric.api import env

env.hoge = 'nemo'

# program name
env.prog_name = 'Fabric.study'

# deploy mode
env.deploy_mode = ['production','staging','development']

# Ansible inventory location
env.inventory = './hosts'

# current release_tag
env.current_tag = None

# github clone base dir
env.source_base = {}
env.source_base['base_path'] = '/home/vagrant/deploy'

# symbolic link target
env.dest_base = '/var/deploy'
env.dest_name = 'STUDY_TEST'
env.dest_path = ('%s/%s' % (env.dest_base, env.dest_name))

# ssh pathes
env.ssh = {}
env.ssh['base_path'] = '/home/vagrant/.ssh'
env.ssh['config_name'] = 'config'
env.ssh['sshkey_name'] = '{PRIVATE_KEY_FILE_FOR_GITHUB}'
#env.ssh['sshkey_name'] = 'id_rsa_FOO_BAR'  <- set in "resources/"


# git repogitries
env.git = {}
env.git['repository'] = 'git@github.com:nemo-soshi-mulodo/OpenDevStudyGroup.git'


# resource files
env.resources = {}
env.resources['ssh_key'] = './fabric_files/resources/id_rsa_github_mulodo'
env.resources['ssh_config'] = './fabric_files/resources/ssh_config'
