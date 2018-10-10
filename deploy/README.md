# Steps to deploy

- ubuntu 18.04 (x64)
- python 3.7

## Preview

### add user(example : www)

- sudo adduser www && sudo usermod -G sudo www
- sudo chown -r www:www /opt/ && su www 
- cd ~

### zsh (recommend!!)

- sudo apt install zsh
- sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
- chsh -s /bin/zsh

### conda environment

- wget "https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh"
- sudo chmod +x ./Anaconda3-5.3.0-Linux-x86_64.sh && ./Anaconda3-5.3.0-Linux-x86_64.sh

- conda create -n deploy python=3.7
- echo "alias deploy='conda activate deploy'" >> ~/.zshrc && source ~/.zshrc && deploy
- conda install -c conda-forge uwsgi
- conda install -c conda-forge gevent
- conda install --yes --file requirements.txt

### Nginx

- sudo apt install nginx
- nginx -t
- nginx -s reload


