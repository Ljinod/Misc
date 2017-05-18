#!/usr/bin/python3

"""
Request the route /permissions/doctype/:doctype/sharedWithOthers to get all the
permissions that apply to the documents of the provided doctype that were
shared to the user.
"""

import logging
import subprocess
import sys
import createoauthclientandtoken

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_shared_with_others_perms():
    """
    Request the route /permissions/doctype/:doctype/sharedWithOthers to get
    all the permissions that apply to the documents of the provided doctype
    that were shared to the user.
    """

    client = createoauthclientandtoken.create_oauth_client_and_token()

    for doctype in client.doctypes:
        cmd = 'curl -s -X GET -H "Authorization: Bearer {}" \
            -H "Host: {}" -H "Accept: application/json" \
            {}/permissions/doctype/{}/sharedWithOthers'.format(client.token,
                                                               client.instance,
                                                               client.domain,
                                                               doctype)
        logging.debug(cmd)

        logging.info("Requesting for doctype: %s", doctype)
        try:
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, check=True,
                                 encoding="utf-8")
        except subprocess.CalledProcessError as cpe:
            logging.error("Request failed with error: %s", cpe.stderr)
            sys.exit()
        except subprocess.SubprocessError as spe:
            logging.error('An unexpected error occurred: %s', spe)
            sys.exit()

        print("List of permissions for {}: {}".format(
            doctype, res.stdout.rstrip()))


if __name__ == "__main__":
    get_shared_with_others_perms()
