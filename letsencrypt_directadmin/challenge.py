"""DirectAdminHTTP01Challenge"""
import logging
import os

from letsencrypt import errors

logger = logging.getLogger(__name__)


class DirectAdminHTTP01Challenge(object):
    """Class performs HTTP01 challenge within the DirectAdmin configurator."""

    def __init__(self, da_api_client):
        self.da_api_client = da_api_client

    def perform(self, achall):
        """Perform a challenge on DirectAdmin."""
        response, validation = achall.response_and_validation()
        self._put_validation_file(
            domain=achall.domain,
            path=achall.URI_ROOT_PATH,
            filename=achall.chall.encode("token"),
            content=validation.encode())
        return response

    def _put_validation_file(self, domain, path, filename, content):
        """Put file to the domain with validation content"""
        path = self.da_api_client.get_public_html_path(domain) + path
        response = self.da_api_client.create_file(
            path=path,
            filename=filename,
            contents=content)

    def cleanup(self, achall):
        """Remove validation file and directories."""
        path = self.da_api_client.get_public_html_path(achall.domain)
        dirname = os.path.dirname(achall.URI_ROOT_PATH)
        self.da_api_client.remove_folder(os.path.join(path, dirname))
