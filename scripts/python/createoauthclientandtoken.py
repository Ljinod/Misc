#!/usr/bin/python3

"""
This module deals with the creation of an OAuth client and a token for a
specific domain and the provided document types.
"""

import argparse
import logging
import oauthclient

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def create_oauth_client_and_token():
    """Create an OAuth client and a token with all rights access for the given
       domain and doctypes."""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
Create an OAuth client and a token with all rights access for the given
doctypes.

Examples:
$ ./script.py cozy1.local:8080 io.cozy.photos io.cozy.albums
 Will try to create an OAuth client for the instance "cozy1.local:8080" and the
 domain is presumed to be "http://cozy1.local:8080".

$ ./script.py cozy1 io.cozy.photos -d http://cozy1.local:8080
 Will try to create an OAuth client for the instance "cozy1" and the requests
 will be send to the domain "http://cozy1.local:8080".
''')

    parser.add_argument("instance", action="store",
                        help="""Instance for which the OAuth client and token
                        will be created.""")
    # `nargs="+"` means: take the remaining arguments and at least one.
    parser.add_argument("doctypes", nargs="+", action="store",
                        help="""Doctypes the client will have access to.
                        A space separated list can be provided.""")
    parser.add_argument("--domain", "-d", action="store",
                        help="""The domain corresponding to the instance. By
                        default this value is 'http://instance'. """)
    args = parser.parse_args()

    client = oauthclient.OAuthClient(args.instance, args.doctypes,
                                     domain=args.domain)

    logging.info('Creating OAuth client for instance: %s', args.instance)
    client.create_oauth_client()
    logging.info('OAuth client created, id: %s', client.client_id)

    logging.info('Generating token for OAuth client: %s', client.client_id)
    client.create_token()
    logging.info('OAuth token created: %s', client.token)

    return client


if __name__ == "__main__":
    create_oauth_client_and_token()
