"""Q06: lista chaves, tamanho e data de modificacao no bucket grupo2; so leitura."""
import os
from pathlib import Path
import boto3

root = Path(__file__).resolve().parents[3]
env_file = root / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

endpoint = os.environ.get("MINIO_ENDPOINT", "http://35.226.64.52:9010")
bucket = os.environ.get("MINIO_BUCKET", "grupo2")
s3 = boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
)
objects = []
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket):
    objects.extend(page.get("Contents", []))
for obj in sorted(objects, key=lambda item: item["Key"]):
    print(f"{obj['Key']}\t{obj['Size']} bytes\t{obj['LastModified'].isoformat()}")
print(f"TOTAL_OBJECTS={len(objects)}")
print(f"TOTAL_BYTES={sum(obj['Size'] for obj in objects)}")
