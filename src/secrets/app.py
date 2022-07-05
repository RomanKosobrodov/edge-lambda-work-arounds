import boto3
import json
import yaml

client = boto3.client(service_name="secretsmanager",
                      region_name="us-east-1")
try:
    response = client.get_secret_value(SecretId="edge-lambda-resources")
    resources = json.loads(response["SecretString"])
    bucket_name = resources["bucket"]
    
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    
    stats = list()
    total_size = 0
    for obj in bucket.objects.all():
        total_size += obj.size
        stats.append({"key": obj.key, "size": obj.size, "modified": str(obj.last_modified)})
    
    data = {
            "function": "secrets",
            "bucket": bucket_name,
            "content" : stats,
            "total_size": total_size
        }
except Exception as e:
    data = {
        "function": "secrets",
        "error": e
    }

body = yaml.dump(data)


def handler(event, context): 
    return {
            "status": "200",
            "statusDescription": "OK",
            "body": body                
            }
    