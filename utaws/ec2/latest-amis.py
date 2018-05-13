#!/usr/bin/env python3

import argparse
import os
import sys
import json
import inspect
import boto3
from botocore.exceptions import ClientError
from utaws.common.session import authenticated, boto3_session
from utaws.common.script_utils import stdout_message
from utaws import loggers

try:
    from utaws.common.oscodes_unix import exit_codes
except Exception:
    from utaws.common.oscodes_win import exit_codes    # non-specific os-safe codes

# globals
logger = loggers.getLogger()


def get_regions():
    """ Return list of all regions """

    client = session.client('ec2')
    return [x['RegionName'] for x in client.describe_regions()['Regions']]


def amazonlinux(profile=None):
    """
    Return latest current amazonlinux v1 AMI for each region
    """
    latest = {}
    for region in regions:
        try:
            client = session.client('ec2', region_name=region)
            r = client.describe_images(
                Owners=['amazon'],
                Filters=[
                    {
                        'Name': 'name',
                        'Values': [
                            'amzn-ami-hvm-2018.??.?.2018????-x86_64-gp2'
                        ]
                    }
                ])
            latest[region] = r['Images']
        except ClientError as e:
            logger.exception(
                '%s: Boto error while retrieving AMI data (%s)' %
                (inspect.stack()[0][3], str(e)))
            continue
        except Exception as e:
            logger.exception(
                '%s: Unknown Exception occured while retrieving AMI data (%s)' %
                (inspect.stack()[0][3], str(e)))
            raise e
    return latest


def amazonlinux2(profile=None):
    """
    Return latest current amazonlinux v1 AMI for each region
    """
    latest = {}
    for region in regions:
        try:
            client = boto3_session(service='ec2', profile=profile)
            client = session.client('ec2', region_name=region)
            r = client.describe_images(
                Owners=['amazon'],
                Filters=[
                    {
                        'Name': 'name',
                        'Values': [
                            'amzn2-ami-hvm-????.??.?.2018????.?-x86_64-gp2',
                            'amzn2-ami-hvm-????.??.?.2018????-x86_64-gp2'
                        ]
                    }
                ])
            latest[region] = r['Images']
        except ClientError as e:
            logger.exception(
                '%s: Boto error while retrieving AMI data (%s)' %
                (inspect.stack()[0][3], str(e)))
            continue
        except Exception as e:
            logger.exception(
                '%s: Unknown Exception occured while retrieving AMI data (%s)' %
                (inspect.stack()[0][3], str(e)))
            raise e
    return latest


def options(parser, help_menu=True):
    """
    Summary:
        parse cli parameter options
    Returns:
        TYPE: argparse object, parser argument set
    """
    parser.add_argument("-p", "--profile", nargs='?', default="default",
    parser.add_argument("-V", "--version", dest='version', action='store_true', required=False)
    #parser.add_argument("-h", "--help", dest='help', action='store_true', required=False)
    return parser.parse_args()


def init_cli():
    # parser = argparse.ArgumentParser(add_help=False, usage=help_menu())
    parser = argparse.ArgumentParser(add_help=True)

    try:
        args = options(parser)
    except Exception as e:
        #help_menu()
        stdout_message(str(e), 'ERROR')
        sys.exit(exit_codes['EX_OK']['Code'])

    if len(sys.argv) == 1:
        #help_menu()
        sys.exit(exit_codes['EX_OK']['Code'])

    elif authenticated(profile=args.profile):
        # execute keyset operation
        success = main(
                    operation=args.operation,
                    profile=args.profile,
                    user_name=args.username,
                    auto=args.auto,
                    debug=args.debug
                    )
        if success:
            logger.info('Job complete')
            sys.exit(exit_codes['EX_OK']['Code'])
    else:
        stdout_message(
            'Authenication Failed to AWS Account for user %s' % args.profile,
            prefix='AUTH',
            severity='WARNING'
            )
        sys.exit(exit_codes['E_AUTHFAIL']['Code'])

    failure = """ : Check of runtime parameters failed for unknown reason.
    Please ensure local awscli is configured. Then run keyconfig to
    configure keyup runtime parameters.   Exiting. Code: """
    logger.warning(failure + 'Exit. Code: %s' % sys.exit(exit_codes['E_MISC']['Code']))
    print(failure)


if __name__ == '__main__':
    init_cli()
