from fabric import api

def localtest():
      print "local test"
      api.local('ls -al')


# How to call
# $ fab -f fabfie_1.py localtest
