"""
Summary:
    ec2_utils (python3) | Common EC2 functionality implemented by boto3 SDK

Author:
    Blake Huber
    Copyright Blake Huber, All Rights Reserved.

License:
    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose and without fee is hereby granted,
    provided that the above copyright notice appear in all copies and that
    both the copyright notice and this permission notice appear in
    supporting documentation

    Additional terms may be found in the complete license agreement located at:
    https://bitbucket.org/blakeca00/lambda-library-python/src/master/LICENSE.md

"""
import os
import subprocess
import inspect
import boto3
from botocore.exceptions import ClientError
from pyaws.session import boto3_session
from pyaws import logger


# global objects
REGION = os.environ['AWS_DEFAULT_REGION']


# -- declarations -------------------------------------------------------------


def running_instances(region, profile=None, debug=False):
    """
    Summary.

        Determines state of all ec2 machines in a region

    Returns:
        :list of running ec2 instance ids, TYPE: list

    """
    if profile and profile != 'default':
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource('ec2', region_name=region)
    else:
        ec2 = boto3.resource('ec2', region_name=region)

    instances = ec2.instances.all()

    try:

        return [x for x in instances if x.state['Name'] == 'running']

    except Exception as e:
        logger.exception('Unknown error: {}'.format(e))


def stopped_instances(region, profile=None, debug=False):
    """
    Summary.

        Determines state of all ec2 machines in a region

    Returns:
        :list of stopped ec2 instance ids, TYPE: list

    """
    if profile and profile != 'default':
        session = boto3.Session(profile_name=profile)
        ec2 = session.resource('ec2', region_name=region)
    else:
        ec2 = boto3.resource('ec2', region_name=region)

    instances = ec2.instances.all()

    try:

        return [x for x in instances if x.state['Name'] == 'stopped']

    except Exception as e:
        logger.exception('Unknown error: {}'.format(e))
