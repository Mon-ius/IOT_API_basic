import getpass
import os
import re

## Configuration file
uWSGI = "uWSGI.ini"
NGINX = "NGINX.conf"
SSL = "SSL_AUTO.sh"
### Need to change
DOMAIN = "fff.com"


def get_env():
    cu = getpass.getuser()
    cwd = os.getcwd()
    return cu,cwd

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

def accept_warning(s):
    c = ''
    d = {'Y': True, 'y': True, 'N': False, 'n': False}
    while not c in d:
        c = input('Warning: %s Y/N? ' % s)
    return d[c]

def ssl_init():
    key = input("Cloudflare API token #Ex: dah2dsadscangh : ")
    email = input("Cloudflare email #Ex: sexybuddy@fff.com : ")

    with open(SSL, "r") as fh:
        fds = fh.read()

        fcd = re.sub(r'{{domain}}', '.'.join(DOMAIN.split('.')[-2:]), fds)
        fce = re.sub(r'{{EMAIL}}', email, fcd)
        res = re.sub(r'{{KEY}}', key, fce)


        with open(DOMAIN+'.sh', 'w') as confssl:
            confssl.write(res)
            confssl.close()

        fh.close()
        os.remove(DOMAIN+'.sh')
        os.chmod("./sysrun.sh",0o700)
        os.system("./sysrun.sh")

if __name__ == '__main__':
    domain = input("Input domain name #Ex: superservice.fff.com :")
    if domain and len(domain)>3:
        DOMAIN = domain
    if not accept_warning("Do you have ssl cert"):
        ssl_init()

    usr,loc = get_env()
    gen_ini(usr,loc)
    gen_nginx(loc)
