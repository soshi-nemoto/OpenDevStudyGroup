# -*- coding:utf-8 -*-
"""
Deploy tool
  fab -R {ROLE} help|deploy|tags|change|remove
    * using hosts(inventory file) of Ansible as Fabric Role
  See) $ fab help

  Default settings in fabric_files/resource.py.
  Resource files are in fabric_files/resources/.
"""

__author__ = "Soshi Nemoto <nemo@nemoto.net>"
__status__ = "development"
__version__ = "0.0.1"
__date__    = "05 Janurary 2016"


# add include path
import sys
import time
import datetime
import fabric_files.resource
import contextlib
import syslog

# import ansible.inventory and fabric.api
sys.path.append('/usr/local/Cellar/ansible/1.9.4/libexec/lib/python2.7/site-packages')
sys.path.append('/usr/local/Cellar/ansible/1.9.4/libexec/vendor/lib/python2.7/site-packages')
from ansible import inventory

# import fabric libraries
from fabric import api
from fabric.api import env
from fabric.contrib import files
from fabric.context_managers import hide
from fabric.colors import blue, cyan, green, magenta, red, white, yellow

# set Ansible inventory settings to Fabric role.
inventory = inventory.Inventory(env.inventory)
env.roledefs = inventory.groups_list()
env.use_ssh_config = True



def help():
      """
      Show help of this tool. 'help' is not required role option.
      Usage: $ fab help
      """
      print "Usage:"
      print yellow("<Deploy>")
      print "fab -R [ROLE] deploy"
      print "fab -R [ROLE] deploy:mode=[MODE],tag=[TAG],branch=[BRANCH]force=[True]"
      print "deploy source to servers which are defined as ROLE"
      print "Options"
      print " mode  : 'production', 'staging', 'development'(default)"
      print " tag   : any ASCII tag. (default = Epoch time+microtime)"
      print " branch: target branch name of git. (default = None)"
      print " force : set 'True' cause overwrite. (default = False)"
      print ""
      print yellow("<Show existed tags>")
      print "fab -R [ROLE] tags"
      print "show existed tags"
      print ""
      print yellow("<Change version>")
      print "$ fab -R [ROLE] change:tag=XXXXXX"
      print "change working version to another tagged source"
      print "tag should be exactly same as shown by Tags command"
      print ""
      print yellow("<Remove specified tag>")
      print "$ fab -R [ROLE] remove:tag=XXXXXX"
      print "remove exist tags"
      print "tag should be exactly same as shown by Tags command"

      
def deploy(mode = 'develop' ,tag = None, branch = None, force = False):
      """
      Deploy source from github repository to target host with mode/tag option.
      Options mode  : Deploy mode which used in building tag_name.
                      'development', 'staging', 'production'
              branch: Target branch name of git. default is None(=master)
              tag   : Free strings used in building tag_name.
                      Default is epoch time + micro time.
              force : Bool. True allow to overwrite sources of same tag.
      Usage: $ fab -R {ROLE} deploy
           : $ fab -R {ROLE} deploy:mode=development
           : $ fab -R {ROLE} deploy:tag=PR2349
           : $ fab -R {ROLE} deploy:tag=PR2349,force=True
      Note) 'tag_name' is build as {mode}_YYYYMMDD_{tag} 
      """
      with hide('stdout','stderr','running'):
            print yellow('Processing started')
            # deploying
            _build_new_tag(mode, tag, branch, force)
            _put_github_key()
            _clone_source()
            _check_current_version()
            _create_symlink()
            print yellow('Processing finished')


def tags():
      """
      Show deployed tags and current tag in use.
      Usage: $ fab -R {ROLE} tags
      """
      with hide('stdout','stderr','running'):
            # preparation
            api.run('mkdir -p %s' % env.source_base['base_path'])

            # show current tag
            _check_current_version()
            
            # show tag list
            with hide('stdout','stderr','running'):
                  with api.cd(env.source_base['base_path']):
                        status = api.run('ls -1')
                        print status
      

def change(tag):
      """
      Change used tag to another one
      Options tag : Exsiting tag_name. Tag_names are shown as tags command.
      Usage: $ fab -R {ROLE} change:tag={tag_name}
      """
      with hide('stdout','stderr','running'):
            # check Arg
            if tag == None:
                  print red("Please specify tag. See help (fab help)")
                  api.abort("Version has not changed.")
                
            # preparation
            api.run('mkdir -p %s' % env.source_base['base_path'])
            env.new_path = ('%s/%s' %
                                (env.source_base['base_path'], tag))
            # check tag on remote host
            if not files.exists(env.new_path):
                  print red("No such tag [%s]" % tag)
                  api.abort("Version has not changed.")
    
            # re-link to old version.
            _check_current_version()
            _create_symlink()

            
def remove(tag):
      """
      Remove tag
      Options tag : Exsiting tag_name. Tag_names are shown as tags command.
      Usage: $ fab -R {ROLE} remove:tag={tag_name}
      """
      with hide('stdout','stderr','running'):
            api.run('mkdir -p %s' % env.source_base['base_path'])
            with api.cd(env.source_base['base_path']):
                  if files.exists(tag):
                        _check_current_version()
                        if env.current_tag != ('%s/%s' %
                                               (env.source_base['base_path'],
                                                tag)):
                              status = api.run('rm -fr %s' % tag)
                              print blue("[Remote]: ") + ("remove: %s" % tag)
                        else:
                              print red("The tag(%s) is in use" % tag)
                              api.abort("The tag has not removed.")
                  else:
                        print red("No such tag [%s]" % tag)



            
##########  following functions are priavte ################


def _build_new_tag(mode, tag, branch, force):
      """
      Build new tag_name from arguments given as command option.
      """
      # check deploy mode
      env.mode = 'development'
      if (mode in env.deploy_mode):
            env.mode = mode

      # check branch name
      env.release_branch = branch
      
      # build release tag
      env.tag = tag
      if tag == None:
            tag = str(time.time())
      if env.release_branch == None:
            env.release_tag = ("%s_%s_%s" %
                             (env.mode,
                              datetime.date.today().strftime("%Y%m%d"),
                              str(tag)))
      else:
            env.release_tag = ("%s_%s_%s_%s" %
                             (env.mode,
                              datetime.date.today().strftime("%Y%m%d"),
                              env.release_branch,
                              str(tag)))
      
      # check force mode
      env.force_overwrite = False
      if (force == 'True'):
            env.force_overwrite = True
      
      # check the tag already exists
      env.new_path = ('%s/%s' %
                          (env.source_base['base_path'],
                           env.release_tag))
      if files.exists(env.new_path) and (env.force_overwrite == False):
                  message = ("The tag[%s] is already exists in same day" % tag)
                  print red("[Remote]: ") + message
                  api.abort('Processing aborted')
                  exit
      
      print green("[New tag]: ") +  env.release_tag



def _check_current_version():
      """
      Get used tag_name.
      If None, no source are used in the target host.
      """
      # check current deploy version
      if files.exists(env.dest_path):
            if files.is_link(env.dest_path):
                  env.current_tag = api.run("readlink -f %s" %
                                            env.dest_path)
            else:
                  env.current_tag = None
            
      print green("[current tag]: ") + str(env.current_tag)

      
def _put_github_key():
      """
      Put github private key and a ssh-config file to target hosts.
      """
      # make ssh directry
      api.run('mkdir -p %s' % env.ssh['base_path'])
      print blue("[Remote]: ") + 'create dir: ' +  env.ssh['base_path']
      # put ssh config and key
      api.put(env.resources['ssh_config'],
              ('%s/%s' % (env.ssh['base_path'],
                          env.ssh['config_name'])))
      api.put(env.resources['ssh_key'],
              ('%s/%s' % (env.ssh['base_path'],
                          env.ssh['sshkey_name'])))
      print blue("[Remote]: ") + ('copy files: %s, %s' %
                                  (env.ssh['base_path'],
                                   env.ssh['sshkey_name']))
      # change mode to read only
      api.sudo('chmod 600 %s/%s' %
               (env.ssh['base_path'], env.ssh['config_name']))
      api.sudo('chmod 600 %s/%s' %
               (env.ssh['base_path'], env.ssh['sshkey_name']))
      print blue("[Remote]: ") + ('change mode: %s, %s' %
                                  (env.ssh['base_path'],
                                   env.ssh['sshkey_name']))

      
def _clone_source():
      """
      Clone github repository to env.new_path
        See.  _build_new_tag() about env.new_path
      """
      # remove existed source.
      if env.force_overwrite == True:
            with api.cd(env.source_base['base_path']):
                  api.run('cd %s' % env.source_base['base_path'])
                  api.run('rm -fr %s' % env.release_tag)
                  message = ('FORCE: cd %s' % env.source_base['base_path'])
                  print blue('[Remote]: ') + message
                  message = ('FORCE: rm -fr %s' % env.release_tag)
                  print blue('[Remote]: ') + message
                  
      # clone git source
      api.run('mkdir -p %s' % env.new_path)
      with api.cd(env.new_path):
            if env.release_branch == None:
                  cmd = ('git clone %s' % env.git['repository'])
            else:
                  cmd = ('git clone -b %s %s' % (env.release_branch,
                                                  env.git['repository']))
            api.run(cmd)

      print blue("[Remote]: ") + ('git clonne (%s):\n          %s' %
                                  (env.new_path, cmd))

      
def _create_symlink():
      """
      Make symbolic links from github clone to env.dest_base
        See. resource.py about env.dest_base
      """
      # remove symbolic link
      if env.current_tag != None:
            api.sudo('unlink %s' % env.dest_path)

      # create symbolic link
      api.sudo('mkdir -p %s' % env.dest_base)
      with api.cd(env.dest_base):
            api.sudo('ln -nfs %s %s' % (env.new_path, env.dest_name))
      print blue('[Remote]: ') + ('create link from %s to %s' %
                                  (env.new_path, env.dest_name))

            
def _rollback():
      """
      Not used yet.
      """
      pass

