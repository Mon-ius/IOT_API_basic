import getpass
import os
import re
import shutil

## Configuration file
uWSGI = "uWSGI.INI"
NGINX = "NGINX.CONF"

SSL = "SSL_AUTO.SH"
SERVICE = "SAMPLE.service"
DOCKER = "DOCKER.run"
### May need to change
DOMAIN = "fff.com"
NGINX_CONF = "/etc/nginx/sites-enabled/"
SYSTEMD_CONF = "/etc/systemd/system/"



def get_env():
    cu = getpass.getuser()
    cwd = os.getcwd()
    return cu,cwd

def add_env(**args):
    env = os.path.dirname(loc)
    with open(env+'.env', 'a') as file:
        for i,j in args.items():
            file.write(i+'='+j)
        file.close()
    return False

def add_uwsgi(usr,loc):
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

def add_nginx(loc):
    with open(NGINX, "r") as fh:
        fds = fh.read()
    
        fcd = re.sub(r'{{domain}}', DOMAIN, fds)
        res = re.sub(r'{{loc}}', loc, fcd)

        with open(DOMAIN+'.conf', 'w') as confnginx:
            confnginx.write(res)
            confnginx.close()
            try:
                shutil.move(DOMAIN+'.conf',NGINX_CONF)
                os.system("nginx -s reload")
            except shutil.Error:
                print("Complete")
        fh.close()

def add_service(usr,loc):
    with open(SERVICE, "r") as fh:
        fds = fh.read()
    
        fcd = re.sub(r'{{domain}}', DOMAIN, fds)
        fcu = re.sub(r'{{usr}}', usr, fcd)
        res = re.sub(r'{{loc}}', loc, fcu)

        with open(DOMAIN+'.service', 'w') as confservice:
            confservice.write(res)
            confservice.close()
    
        #cp
            try:
                shutil.move(DOMAIN+'.service',SYSTEMD_CONF)
            except shutil.Error:
                print("Complete")
        
        os.system("systemctl enable"+DOMAIN)
        os.system("systemctl start"+DOMAIN)
        #reload deamon
        fh.close()

def init_docker(usr):
    
    with open(DOCKER, "r") as fh:
        fds = fh.read()
    
        fcd = re.sub(r'{{domain}}', DOMAIN, fds)
        fcu = re.sub(r'{{usr}}', usr, fcd)
        res = re.sub(r'{{passwd}}', loc+DOMAIN+usr, fcu)

        with open(DOMAIN+'.run', 'w') as confdocker:
            confdocker.write(res)
            confdocker.close()
    
        fh.close()
        
        os.chmod(DOMAIN+'.run',0o700)
        os.system(DOMAIN+'.run')

        conf = "postgres://{}:{}@172.17.0.1:5432/{}".format(usr,loc+DOMAIN+usr,DOMAIN)
        add_env(DATABASE_URL=conf)
        # os.remove(DOMAIN+'.run')

        #add DATABASE_URL into .env



def init_ssl():
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
        if not os.path.exists("/etc/nginx/certs"):
            os.makedirs("/etc/nginx/certs")
        os.chmod(DOMAIN+'.sh',0o700)
        os.system(DOMAIN+'.sh')
        # os.remove(DOMAIN+'.sh')

def accept_warning(s):
    c = ''
    d = {'Y': True, 'y': True, 'N': False, 'n': False}
    while not c in d:
        c = input('Warning: %s Y/N? ' % s)
    return d[c]

if __name__ == '__main__':
    usr,loc = get_env()
    domain = input("Input domain name #Ex: superservice.fff.com :")
    if domain and len(domain)>3:
        DOMAIN = domain
    if not accept_warning("Do you have ssl cert"):
        init_ssl()

    if not accept_warning("Do you have database installed"):
        init_docker(usr)

    
    add_uwsgi(usr,loc)
    add_nginx(loc)
    add_service(usr,loc)
