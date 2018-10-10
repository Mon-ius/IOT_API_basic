import getpass
import os
import re

## Configuration file
uWSGI = "uWSGI.ini"
NGINX = "NGINX.conf"

### Need to change
DOMAIN = "monius.top"


def get_env():
    cu = getpass.getuser()
    cwd = os.getcwd()
    return cu,cwd
# uid = {{w}}
# gid = {{w}}
# master = true
# vhost = true
# work=4
# reload-mercy = 10
# vacuum = true
# max-requests = 1000
# limit-as = 6048
# callable = app
# socket = ./uwsgi.sock
# chmod-socket = 666
# gevent =100
# wsgi-file = ../run.py
# chdir = ${{current_dir}}/..

def gen_ini(usr,loc):
    env = os.path.dirname(loc)
   
    with open(uWSGI, 'r') as fh:
        fds = fh.read()

        fce = re.sub(r'{{env}}',env,fds)
        fcu = re.sub(r'{{usr}}',usr,fce)
        res = re.sub(r'{{loc}}',loc,fcu)

        with open(DOMAIN+'.ini', 'w') as confuwsgi:
            confuwsgi.write(res)
            confuwsgi.close()
    
        fh.close()




def gen_nginx(loc):
    with open(NGINX, "r") as fh:
        fds = fh.read()
    
        fcd = re.sub(r'{{domain}}', DOMAIN, fds)
        res = re.sub(r'{{loc}}', loc, fcd)

        with open(DOMAIN+'.conf', 'w') as confnginx:
            confnginx.write(res)
            confnginx.close()
    
        fh.close()
    

if __name__ == '__main__':
    domain = input("Input domain name : ")
    if domain and len(domain)>3:
        DOMAIN = domain
    usr,loc = get_env()
    gen_ini(usr,loc)
    gen_nginx(loc)
