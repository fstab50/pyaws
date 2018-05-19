"""
utaws.tags:  Tag Utilities
"""
import os
import sys
import json
import inspect
import boto3
from botocore.exceptions import ClientError
from utaws.common import loggers
from utaws import __version__

logger = loggers.getLogger(__version__)


def filter_tags(tag_list, *args):
    """
        - Filters a tag set by exclusion
        - variable tag keys given as parameters, tag keys corresponding to args
          are excluded

    RETURNS
        TYPE: list
    """
    clean = tag_list.copy()

    for tag in tag_list:
        for arg in args:
            if arg in tag['Key']:
                clean.remove(tag)
    return clean


def print_tags(resource_list, tag_list, mode=''):
    """
        - Prints tag keys, values applied to resources
        - output: cloudwatch logs
        - mode:  INFO, DBUG, or UNKN (unknown or not provided)
    """
    if mode == 0:
        mode_text = 'DBUG'
    else:
        mode_text = 'INFO'

    try:
        for resource in resource_list:
            logger.info('Tags successfully applied to resource: ' + str(resource))
            ct = 0
            for t in tag_list:
                logger.info('tag' + str(ct) + ': ' + str(t['Key']) + ' : ' + str(t['Value']))
                ct += 1
        if mode == 0:
            logger.debug('DBUGMODE = True, No tags applied')

    except Exception as e:
        logger.critical(
            "%s: problem printing tag keys or values to cw logs: %s" %
            (inspect.stack()[0][3], str(e)))
        return 1
    return 0


def json_tags(resource_list, tag_list, mode=''):
    """
        - Prints tag keys, values applied to resources
        - output: cloudwatch logs
        - mode:  INFO, DBUG, or UNKN (unknown or not provided)
    """
    if mode == 0:
        mode_text = 'DBUG'
    else:
        mode_text = 'INFO'

    try:
        for resource in resource_list:
            if mode == 0:
                logger.debug('DBUGMODE enabled - Print tags found on resource %s:' % str(resource))
            else:
                logger.info('Tags found resource %s:' % str(resource))
            print(json.dumps(tag_list, indent=4, sort_keys=True))
    except Exception as e:
        logger.critical(
            "%s: problem printing tag keys or values to cw logs: %s" %
            (inspect.stack()[0][3], str(e)))
        return False
    return True


def create_taglist(dict):
    """
    Summary:
        Transforms tag dictionary back into a properly formatted tag list
    Returns:
        tags, TYPE: list
    """
    tags, temp = [], {}
    for k, v in dict:
        temp['Key'] = k
        temp['Value'] = v
        tags.append(temp)
    return tags
