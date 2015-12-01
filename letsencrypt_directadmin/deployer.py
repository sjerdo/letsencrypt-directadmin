"""DirectAdmin deployer"""
import logging

from letsencrypt import errors

logger = logging.getLogger(__name__)


class DirectAdminDeployer(object):
    """Class performs deploy operations within the DirectAdmin configurator"""

    def __init__(self, da_api_client, basedomain):
        """Initialize DirectAdmin Certificate Deployer"""
        self.da_api_client = da_api_client
        self.basedomain = basedomain
        self.domains = []
        self.cert_data = self.key_data = self.chain_data = None
        self.cert_installed = False

    def add_domain(self, domain):
        self.domains.append(domain)

    def cert_name(self):
        """Return name of the domain certificate in DirectAdmin."""
        return "Lets Encrypt %s" % self.basedomain

    def init_cert(self, cert_data, key_data, chain_data=None):
        """Initialize certificate data."""
        self.cert_data = cert_data
        self.key_data = key_data
        self.chain_data = chain_data if chain_data else {}

    def install_cert(self):
        """Install certificate to the domain repository in DirectAdmin."""
        certificate = self.key_data + '\n' + self.cert_data
        print self.da_api_client.set_ssl_certificate(self.basedomain, certificate)
        if self.chain_data is not None:
            print self.da_api_client.set_ca_root_ssl_certificate(
                self.basedomain, self.chain_data)

        # raise errors.PluginError(
        #     'Install certificate failure: %s' % error_text)
        self.cert_installed = True
