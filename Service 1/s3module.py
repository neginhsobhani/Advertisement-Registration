import boto3
import logging
from botocore.exceptions import ClientError

ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.com'
AWS_ACCESS_KEY_ID = 'your_access_key_ID'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'
ARVAN_ENDPOINT = 'https://imagebucket.s3.ir-thr-at1.arvanstorage.com'


def get_url(object_name):
    url = f'{ARVAN_ENDPOINT}/{object_name}'
    return url


def upload_to_s3(input_file_path, input_object):
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        s3_resource = boto3.resource(
            's3',
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    except Exception as exc:
        logging.error(exc)
    else:
        try:
            bucket = s3_resource.Bucket('imagebucket')
            file_path = input_file_path
            object_name = input_object

            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='public-read',
                    Body=file,
                    Key=object_name
                )
                url = get_url(input_object)
        except ClientError as e:
            logging.error(e)
            return None
        return url


