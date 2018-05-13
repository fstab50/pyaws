#!/usr/bin/env python3

import argparse
import os
import sys
import json
import inspect
from pygments import highlight, lexers, formatters
import boto3
from botocore.exceptions import ClientError
from utaws.common.session import authenticated, boto3_session
from utaws.common.script_utils import stdout_message, export_json_object
from utaws import loggers

try:
    from utaws.common.oscodes_unix import exit_codes
except Exception:
    from utaws.common.oscodes_win import exit_codes    # non-specific os-safe codes

# globals
logger = loggers.getLogger()
VALID_AMIS = ('amazonlinux1', 'amazonlinux2', 'aml1', 'aml2', 'redhat', 'kali')
VALID_FORMATS = ('stdout', 'file', 'list')


def get_regions(profile):
    """ Return list of all regions """
    try:
        if not profile:
            profile = 'default'
        client = boto3_session(service='ec2', profile=profile)

    except ClientError as e:
        logger.exception('%s: Boto error while retrieving regions (%s)' %
            (inspect.stack()[0][3], str(e)))
        raise e
    return [x['RegionName'] for x in client.describe_regions()['Regions']]


def amazonlinux1(profile, debug=False):
    """
    Return latest current amazonlinux v1 AMI for each region
    """
    latest = {}
    for region in regions:
        try:
            client = boto3_session(service='ec2', profile=profile)
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


def amazonlinux2(profile, debug=False):
    """
    Return latest current amazonlinux v1 AMI for each region
    """
    latest = {}
    for region in regions:
        try:
            if not profile:
                profile = 'default'
            client = boto3_session(service='ec2', profile=profile)

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
    parser.add_argument("-p", "--profile", nargs='?', default="default", required=False, help="type (default: %(default)s)")
    parser.add_argument("-i", "--image", nargs='?', default='list', type=str, choices=VALID_AMIS, required=False)
    parser.add_argument("-f", "--format", nargs='?', default='list', type=str, choices=VALID_FORMATS, required=False)
    parser.add_argument("-d", "--debug", dest='debug', action='store_true', required=False)
    parser.add_argument("-V", "--version", dest='version', action='store_true', required=False)
    #parser.add_argument("-h", "--help", dest='help', action='store_true', required=False)
    return parser.parse_args()


def init_cli():
    # parser = argparse.ArgumentParser(add_help=False, usage=help_menu())
    parser = argparse.ArgumentParser(add_help=True)
    print('debug is: ' + args.debug)
    exit(0)
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
        # execute ami operation
        if args.image in ('amazonlinux1', 'aml1'):
            latest = amazonlinux1(profile=args.profile, debug=args.debug)
        elif args.image in ('amazonlinux2', 'aml2'):
            latest = amazonlinux2(profile=args.profile, debug=args.debug)

        # return appropriate response format
        if RETURN_FORMAT == 'stdout':
            export_json_object(dict_obj=latest)
            sys.exit(exit_codes['EX_OK']['Code'])

        elif RETURN_FORMAT == 'file' and args.filename:
            export_json_object(dict_obj=latest, filename=args.filename)
            sys.exit(exit_codes['EX_OK']['Code'])

        elif RETURN_FORMAT == 'list':
            return latest
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
    RETURN_FORMAT = 'print'
    init_cli()
    sys.exit(exit_codes['EX_OK']['Code'])
