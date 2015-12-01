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
        self.cert_installed = self.cacert_installed = False

    def add_domain(self, domain):
        """Add domain to the list of domains this certificate is deployed to"""
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
        cacert_response = None
        certificate = self.key_data + '\n' + self.cert_data
        cert_response = self.da_api_client.set_ssl_certificate(self.basedomain, certificate)
        if self.chain_data is not None:
            cacert_response = self.da_api_client.set_ca_root_ssl_certificate(
                self.basedomain, self.chain_data)

        if not cert_response is True:
            raise errors.PluginError('Install certificate failure: %s' % cert_response)
        self.cert_installed = True

        if not cacert_response is True:
            raise errors.PluginError('Install CA root certificate failure: %s' % cacert_response)
        self.cacert_installed = True

        return self.cert_installed and self.cacert_installed

    def remove_cert(self):
        """Remove certificate in DirectAdmin."""
        # TODO: should set back old certificate?
        cert_response = self.da_api_client.remove_ssl_certificate(self.basedomain)
        cacert_response = self.da_api_client.remove_ca_root_ssl_certificate(self.basedomain)
        if cert_response is True:
            self.cert_installed = False
        else:
            raise PluginError('Could not uninstall certificate for domain {}'.format(self.basedomain))
        if cacert_response is True:
            self.cacert_installed = False
        else:
            raise PluginError('Could not uninstall chain for domain {}'.format(self.basedomain))

    def revert(self):
        """Revert changes in DirectAdmin."""
        if self.cert_installed:
            self.remove_cert()
