import boto3


def get_s3_object_last_modified(bucket_name, prefix):
    """
    Get last modified S3 object in specified bucket_name with prefix

    :param str bucket_name: Name of bucket to chewck for last modified object
    :param str prefix: Prefix of object key
    :return Object: AWS S3 Object
    """
    # Based on https://stackoverflow.com/a/62864288
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    last_modified = None
    for page in page_iterator:
        if "Contents" in page:
            last_modified2 = max(page["Contents"], key=lambda x: x["LastModified"])
            if last_modified is None or last_modified2["LastModified"] > last_modified["LastModified"]:
                last_modified = last_modified2
    return last_modified
