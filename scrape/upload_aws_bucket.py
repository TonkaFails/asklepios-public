import boto3
from botocore.exceptions import NoCredentialsError

# Define S3 client
s3 = boto3.client('s3')

# Function to upload file
def upload_to_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket.

    :param file_name: File to upload
    :param bucket_name: S3 bucket name
    :param object_name: S3 object name. If not specified, file_name is used.
    :return: True if file was uploaded, else False
    """
    # If no object_name provided, use the file_name
    if object_name is None:
        object_name = file_name

    try:
        # Upload the file
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Usage example
file_to_upload = 'alle_Leitlinien.zip'
bucket_name = "asklepios-guidelines"
upload_to_s3(file_to_upload, bucket_name)
