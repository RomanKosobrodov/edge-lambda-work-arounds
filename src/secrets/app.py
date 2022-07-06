import boto3
import json
import yaml


error = None                      
try:
    client = boto3.client(service_name="secretsmanager",
                          region_name="us-east-1")
    response = client.get_secret_value(SecretId="edge-lambda-resources")
    resources = json.loads(response["SecretString"])
    bucket_name = resources["bucket"]
    
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)   
    bucket.objects.all()  # check that listing objects is allowed
except Exception as e:
    error = e


def handler(event, context): 
    if error is not None:
        return {
                "status": "200",
                "statusDescription": "OK",
                "body": str(error)                
                }
        
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

    return {
            "status": "200",
            "statusDescription": "OK",
            "body": yaml.dump(data)                
            }
