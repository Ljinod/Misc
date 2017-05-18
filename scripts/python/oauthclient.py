#!/usr/bin/python3

"""
OAuth client class
"""

import subprocess
import logging
import sys
from urllib.parse import urlparse


class OAuthClient:
    """
    OAuth client class. Its fields are:

    * instance: the instance to which the oauth client is linked.
    * doctypes: the doctypes the oauth client can access.
    * client_id: the id of the OAuth client.
    * token: the token associated with the OAuth client.
    """

    def __init__(self, instance, doctypes, domain=None):
        self.instance = instance
        self.doctypes = doctypes
        self.client_id = ""
        self.token = ""

        if not domain:
            if instance.startswith("http://") or \
                    instance.startswith("https://"):
                self.domain = instance
            else:
                self.domain = "http://{}".format(instance)
        else:
            self.domain = domain

    def create_oauth_client(self):
        """Create an OAuth client for the given instance."""

        # The redirect_uri cannot contain a port.
        parsed_domain = urlparse(self.domain)
        port = str(parsed_domain.port)
        pos = self.domain.find(port)
        if pos is not -1:
            # pos will give us this position: http://cozy1.local:8080
            #                                                    ^
            # we need to remove the colon as well.
            start = pos - 1
            end = pos + len(port)
            redirect_uri = self.domain[0:start] + \
                self.domain[end:len(self.domain)]
        else:
            redirect_uri = self.domain

        cmd = "cozy-stack instances client-oauth {} {} cli-test test".format(
            self.instance, redirect_uri)
        logging.debug(cmd)

        try:
            # As I'm passing a string for the command to execute shell must be
            # set to True otherwise an error "No such file or directory" will
            # be raised.
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, check=True,
                                 encoding="utf-8")

        except subprocess.CalledProcessError as cpe:
            logging.error('Could not create OAuth client for %s',
                          self.instance)
            logging.error('The following error occurred: %s', cpe.stderr)
            sys.exit()
        except subprocess.SubprocessError as spe:
            logging.error('An unexpected error occurred: %s', spe)
            sys.exit()

        # Remove newline characters through `rstrip`.
        self.client_id = res.stdout.rstrip()

    def create_token(self):
        """Create on OAuth token that gives all rights on the provided
        doctypes."""

        doctypes_str = ' '.join(self.doctypes)
        doctypes_str.rstrip()

        cmd = "cozy-stack instances token-oauth {} {} {}".format(
            self.instance, self.client_id, doctypes_str)
        logging.debug(cmd)

        try:
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, check=True,
                                 encoding="utf-8")

        except subprocess.CalledProcessError as cpe:
            logging.error('Could not create OAuth token for %s',
                          self.client_id)
            logging.error('The following error occurred: %s', cpe.stderr)
            sys.exit()
        except subprocess.SubprocessError as spe:
            logging.error('An unexpected error occurred: %s', spe)
            sys.exit()

        self.token = res.stdout.rstrip()
