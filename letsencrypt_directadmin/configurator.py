"""DirectAdmin API plugin."""
import errno
import logging
import os

import zope.interface

from acme import challenges

from letsencrypt import errors
from letsencrypt import interfaces
from letsencrypt.plugins import common
from letsencrypt.errors import PluginError

# Hacky fix to include the git submodule (python-directadmin should be in PyPI?)
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../python-directadmin/'))
print sys.path

import directadmin
from urlparse import urlsplit


class Configurator(common.Plugin):
    """DirectAdmin API Configurator."""
    zope.interface.implements(interfaces.IAuthenticator, interfaces.IInstaller)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "DirectAdminAPI Configurator"

    MORE_INFO = """\
Configurator plugin that performs http-01 challenge by saving
necessary validation resources to appropriate paths on a server
using the DirectAdmin API. It expects that correct API credentials
are given in commandline or in GUI. Certificates will be installed
automatically. """

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return self.MORE_INFO

    @classmethod
    def add_parser_arguments(cls, add):
        add("server", default=os.getenv('DA_SERVER'),
            help="DirectAdmin Server (can include port, standard 2222, include http:// if the DA server does not support SSL)")
        add("username", default=os.getenv('DA_USERNAME'),
            help="DirectAdmin Username")
        add("login-key", default=os.getenv('DA_LOGIN_KEY'),
            help="DirectAdmin Login Key")

    def __init__(self, *args, **kwargs):
        """Initialize DirectAdmin Configurator."""
        super(Configurator, self).__init__(*args, **kwargs)

        self.da_challenges = {}
        self.da_deployers = {}
        # This will be set in the prepare function
        self.da_api_client = None

    def prepare(self):
        if self.da_api_client is None:
            if self.conf('server') is None:
                # TODO: check if there is a local server at https://localhost:2222 (with non-ssl fallback?)
                # TODO: Allow the user to specify the server as https://user:loginkey@localhost:2222/
                raise PluginError('User did not supply a DirectAdmin Server url.')
            parsed_url = urlsplit(self.conf('server'))
            print directadmin
            self.da_api_client = directadmin.Api(
                https=(False if parsed_url.scheme == 'http' else True),
                hostname=(parsed_url.hostname if parsed_url.hostname else 'localhost'),
                port=(parsed_url.port if parsed_url.port else 2222),
                username=self.conf('username'),
                password=self.conf('login-key'))
        # TODO: check if da server exists, credentials are correct, permissions are okay and ssl certificates are supported
        self.da_api_client.test_login()
        pass  # pragma: no cover

    def get_chall_pref(self, domain):
        """Return list of challenge preferences."""
        # TODO: implement other challenges?
        #               challenges.TLSSNI01
        #        and/or challenges.RecoveryContact
        #        and/or challenges.ProofOfPossession
        #        and/or challenges.DNS
        return [challenges.HTTP01]

    def perform(self, achalls):
        """Perform the configuration related challenge."""
        responses = []
        for x in achalls:
            raise PluginError('Challenges not yet implemented for plugin DirectAdmin')
            pass
            #plesk_challenge = challenge.PleskChallenge(self.plesk_api_client)
            #responses.append(plesk_challenge.perform(x))
            #self.plesk_challenges[x.domain] = plesk_challenge
        return responses

    def cleanup(self, achalls):
        """Revert all challenges."""
        # TODO: revert all challenges
        for x in achalls:
            pass
            #if x.domain in self.plesk_challenges:
            #    self.plesk_challenges[x.domain].cleanup(x)

    def get_all_names(self):
        """Returns all names that may be authenticated."""
        alldomains = []
        domains = self.da_api_client.list_domains()
        for domain in domains:
            # prepend www. to all (sub-)domains and (sub-)pointers..
            subdomains = self.da_api_client.list_subdomains(domain)
            prefixes = ['www.', '']
            prefixes += [p + s + '.' for s in subdomains for p in prefixes]
            alldomains += [p + domain for p in prefixes]

            # add the pointers
            pointers = self.da_api_client.list_domain_pointers(domain)
            alldomains += [p + d for d in pointers for p in prefixes]
        return alldomains

    def deploy_cert(self, domain, cert_path, key_path,
                    chain_path=None, fullchain_path=None):
        pass  # pragma: no cover

    def enhance(self, domain, enhancement, options=None):
        pass  # pragma: no cover

    def supported_enhancements(self):
        return []

    def get_all_certs_keys(self):
        return []

    def save(self, title=None, temporary=False):
        pass  # pragma: no cover

    def rollback_checkpoints(self, rollback=1):
        pass  # pragma: no cover

    def recovery_routine(self):
        pass  # pragma: no cover

    def view_config_changes(self):
        pass  # pragma: no cover

    def config_test(self):
        pass  # pragma: no cover

    def restart(self):
        pass  # pragma: no cover
