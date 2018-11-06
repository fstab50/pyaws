"""
Summary.

    S3 put object Class

"""

import boto3
from botocore.exceptions import ClientError
from pyaws.session import boto3_session
from pyaws import logger


class ObjectS3Operations():
    """
    Summary.

        put, delete, put-acl object operations in Amazon S3
    """
    def __init__(self, bucket, profile=None):
        self.client = boto3_session(service='s3', profile_name=profile)
        self.bucket = bucket

    def put_object(self, key, body, bucket=self.bucket):
        r = self.client.put_object(
                Bucket=bucket, Key=key, Body=body
            )
        return r

    def put_object_acl(self, key, acl, bucket=self.bucket):
        r = client.put_object_acl(
                Bucket=bucket,
                Key=,
                ACL='public-read'
            )
        return r
