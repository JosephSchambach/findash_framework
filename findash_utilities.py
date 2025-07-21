import boto3
import boto3.session
import json


def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-2'
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
    else:
        return json.loads(get_secret_value_response['SecretString'])
