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
import directadmin
from letsencrypt_directadmin import challenge, deployer
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
            # TODO: Allow the user to specify the server as https://user:loginkey@localhost:2222/
            if self.conf('server') is None:
                # TODO: check if there is a local server at https://localhost:2222 (with non-ssl fallback?)
                raise PluginError('User did not supply a DirectAdmin Server url.')
            parsed_url = urlsplit(self.conf('server'))
            self.da_api_client = directadmin.Api(
                https=(False if parsed_url.scheme == 'http' else True),
                hostname=(parsed_url.hostname if parsed_url.hostname else 'localhost'),
                port=(parsed_url.port if parsed_url.port else 2222),
                username=self.conf('username'),
                password=self.conf('login-key'))
        # TODO: check if da server exists, credentials are correct, permissions are okay and ssl certificates are supported
        self.da_api_client.test_login()

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
            da_challenge = challenge.DirectAdminHTTP01Challenge(self.da_api_client)
            responses.append(da_challenge.perform(x))
            self.da_challenges[x.domain] = da_challenge
        return responses

    def cleanup(self, achalls):
        """Revert all challenges."""
        for x in achalls:
            if x.domain in self.da_challenges:
                self.da_challenges[x.domain].cleanup(x)

    def get_all_names(self):
        """Returns all names that may be authenticated."""
        alldomains = []
        domains = self.da_api_client.list_domains()
        for domain in domains:
            # make a list of prefixes (including www. and all subdomains)
            subdomains = self.da_api_client.list_subdomains(domain)
            prefixes = ['www.', '']
            prefixes += [p + s + '.' for s in subdomains for p in prefixes]

            # add the main domain to the list of names
            alldomains += [p + domain for p in prefixes]

            # add the pointers to the list of names
            pointers = self.da_api_client.list_domain_pointers(domain)
            alldomains += [p + d for d in pointers for p in prefixes]
        return alldomains

    def deploy_cert(self, domain, cert_path, key_path,
                    chain_path=None, fullchain_path=None):
        """Initialize deploy certificate in DirectAdmin via API."""
        (base, subdomain) = self.da_api_client.get_base_domain(domain)
        if base is None:
            raise PluginError('Unknown domain {} got authorized'.format(domain))
        if base in self.da_deployers:
            self.da_deployers[base].add_domain(domain)
        else:
            da_deployer = deployer.DirectAdminDeployer(self.da_api_client, base)
            da_deployer.add_domain(domain)
            with open(cert_path) as cert_file:
                cert_data = cert_file.read()
            with open(key_path) as key_file:
                key_data = key_file.read()
            if fullchain_path:
                with open(fullchain_path) as chain_file:
                    chain_data = chain_file.read()
            elif chain_path:
                with open(chain_path) as chain_file:
                    chain_data = chain_file.read()
            else:
                chain_data = None

            da_deployer.init_cert(cert_data, key_data, chain_data)
            self.da_deployers[base] = da_deployer

    def enhance(self, domain, enhancement, options=None):
        print 'enhance called', domain, enhancement, options
        pass  # pragma: no cover

    def supported_enhancements(self):
        print 'supported_enhancements called'
        return []

    def get_all_certs_keys(self):
        print 'get_all_certs_keys called'
        return []

    def save(self, title=None, temporary=False):
        """Push DirectAdmin to deploy certificate(s)."""
        for domain in self.da_deployers:
            da_deployer = self.da_deployers[domain]
            if not da_deployer.cert_installed:
                da_deployer.install_cert()

    def rollback_checkpoints(self, rollback=1):
        print 'rollback_checkpoints called'
        pass  # pragma: no cover

    def recovery_routine(self):
        """Revert deployer changes."""
        for domain in self.da_deployers:
            self.da_deployers[domain].revert()

    def view_config_changes(self):
        print 'view_config_changes called'
        pass  # pragma: no cover

    def config_test(self):
        print 'config_test called'
        pass  # pragma: no cover

    def restart(self):
        print 'restart called'
        # TODO: cleanup
        pass  # pragma: no cover
