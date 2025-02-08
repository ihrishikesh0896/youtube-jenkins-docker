    # fix_secrets/secrets_remediation.py
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name, key_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        endpoint_url='http://localhost:4566',
        service_name='secretsmanager',
        region_name='ap-south-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

    try:
        # Fetch the secret value from AWS Secrets Manager
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle errors (e.g., secret not found, permission issues)
        print(f"Error fetching secret: {e}")
        raise e

    # Retrieve the secret string from the response
    secret = get_secret_value_response['SecretString']

    # Convert the secret from JSON string to a dictionary
    secret_dict = json.loads(secret)  # or json.loads(secret) if it's a proper JSON string

    # Return the value of the specified key
    if key_name in secret_dict:
        return secret_dict[key_name]
    else:
        raise KeyError(f"Key {key_name} not found in the secret.")

        