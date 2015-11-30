# letsencrypt-directadmin

# Installation?
* download the letsencrypt client at https://github.com/letsencrypt/letsencrypt and set it up
* clone this repository in the same directory using `git --git-dir=.gittwo clone git@github.com:sjerdo/letsencrypt-directadmin.git tmp && mv tmp/.gittwo && rm -rf tmp && git --git-dir=.gittwo reset --hard .`
* update git submodules using `git --git-dir=.gittwo submodule init && git --git-dir=.gittwo submodule update`
* Run `./venv/bin/python setup-directadmin.py develop`

# Run
You can simply run the client by executing the command
```letsencrypt --configurator letsencrypt-directadmin:directadmin```

# TODO: instructions about config file
