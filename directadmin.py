"""DirectAdmin API plugin."""
import errno
import logging
import os

import zope.interface

from acme import challenges

from letsencrypt import errors
from letsencrypt import interfaces
from letsencrypt.plugins import common


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
            # TODO: ssl support
            help="DirectAdmin Server (can include port, standard 2222)")
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
        pass  # pragma: no cover

    def get_chall_pref(self, domain):
        #TODO: implement other challenges?
        #               challenges.TLSSNI01
        #        and/or challenges.RecoveryContact
        #        and/or challenges.ProofOfPossession
        #        and/or challenges.DNS
        return [challenges.HTTP01]

    def get_all_names(self):
        # TODO: DA API: CMD_API_ADDITIONAL_DOMAINS
        # TODO: Include subdomains..
        return []

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
