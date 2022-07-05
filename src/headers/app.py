import boto3
import yaml

def handler(event, context): 
    custom = event["Records"][0]["cf"]["request"]["origin"]["custom"]["customHeaders"]
    if "bucket" in custom.keys():
        if len(custom["bucket"]) > 0:
            if "value" in custom["bucket"][0]:
                bucket_name = custom["bucket"][0]["value"]
                s3 = boto3.resource("s3")
                bucket = s3.Bucket(bucket_name)
                
                stats = list()
                total_size = 0
                for obj in bucket.objects.all():
                    total_size += obj.size
                    stats.append({"key": obj.key, "size": obj.size, "modified": str(obj.last_modified)})
                
                data = {
                        "function": "headers",
                        "bucket": bucket_name,
                        "content" : stats,
                        "total_size": total_size
                    }
                    
                return {
                        "status": "200",
                        "statusDescription": "OK",
                        "body": yaml.dump(data)
                    }
    return {
        "status": "404",
        "statusDescription": "Not Found",
        "body": "The required custom header was missing from the request"
    }                