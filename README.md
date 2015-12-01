# letsencrypt-directadmin

# Installation
* download the letsencrypt client at https://github.com/letsencrypt/letsencrypt and set it up
* clone this repository in the same directory using `git --git-dir=.gittwo clone git@github.com:sjerdo/letsencrypt-directadmin.git tmp && mv tmp/.gittwo && rm -rf tmp && git --git-dir=.gittwo reset --hard .`
* update git submodules using `git --git-dir=.gittwo submodule init && git --git-dir=.gittwo submodule update`
* Run `./venv/bin/python setup-directadmin.py develop`

# Run
You can run the client by executing the command
```letsencrypt --configurator letsencrypt-directadmin:directadmin --letsencrypt-directadmin:directadmin-server https://www.example.com:2222/ --letsencrypt-directadmin:directadmin-username USERNAME --letsencrypt-directadmin:directadmin-login-key LOGINKEY```
You can also use your DirectAdmin password instead of a Login Key, but this is not recommended.

# TODO: Run with configuration file

# DirectAdmin Login Keys
If you would like to use DirectAdmin Login Keys (which is recommended) instead of your password, the login key should be allowed to use the following commands:
* CMD_API_LOGIN_TEST
* CMD_API_SHOW_DOMAINS
* CMD_API_DOMAIN_POINTER
* CMD_API_SUBDOMAINS
* CMD_API_FILE_MANAGER
* CMD_API_SSL

# TODO's
* subdomains are not yet supported
* subdomains of domain pointers are not yet supported
