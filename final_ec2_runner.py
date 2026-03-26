import boto3
import os
import time

BUCKET_NAME = "green-compute-demo-sanika"
BUCKET_REGION = "ap-south-1"   # where your bucket exists


def generate_job_id():
    return f"job-{int(time.time())}"


def get_ami_id(region):
    ssm = boto3.client('ssm', region_name=region)

    response = ssm.get_parameter(
        Name='/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id'
    )

    return response['Parameter']['Value']


def upload_to_s3(file_path, job_id):
    s3 = boto3.client('s3', region_name=BUCKET_REGION)
    file_name = os.path.basename(file_path)

    s3_key = f"{job_id}/input/{file_name}"

    s3.upload_file(file_path, BUCKET_NAME, s3_key)
    print(f"✅ Uploaded to {s3_key}")

    return file_name


def run_ec2(region, file_name, job_id):
    ec2 = boto3.client('ec2', region_name=region)

    print("🚀 Fetching AMI dynamically...")
    ami_id = get_ami_id(region)

    print(f"✅ Using AMI: {ami_id}")

    user_data_script = f"""#!/bin/bash
exec > /var/log/user-data.log 2>&1
set -ex

echo "===== START ====="

sleep 40

apt-get update -y
apt-get install -y python3 awscli unzip

cd /home/ubuntu

echo "Downloading input"
aws s3 cp s3://{BUCKET_NAME}/{job_id}/input/{file_name} . --region {BUCKET_REGION}

echo "Files after download:"
ls -l

echo "Check if zip"
if [[ "{file_name}" == *.zip ]]; then
    unzip {file_name}
    FILE=$(find . -name "*.py" | head -n 1)
else
    FILE="{file_name}"
fi

echo "Selected file: $FILE"

if [ -z "$FILE" ]; then
    echo "No Python file found" > output.txt
else
    python3 $FILE > output.txt 2>&1
fi

echo "Uploading output"
aws s3 cp output.txt s3://{BUCKET_NAME}/{job_id}/output/output.txt --region {BUCKET_REGION}

echo "Uploading logs"
aws s3 cp /var/log/user-data.log s3://{BUCKET_NAME}/{job_id}/logs/full_log.txt --region {BUCKET_REGION}

echo "===== DONE ====="

sleep 60
shutdown -h now
"""

    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1,
        IamInstanceProfile={
            'Name': 'ec2-s3-access-role'
        },
        UserData=user_data_script
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"🎉 EC2 created: {instance_id}")
    print(f"📁 Job Folder: {job_id}")


# ✅ NEW FUNCTION (for backend integration)
def run_job(region, file_path):
    print("🔥 RUN_JOB CALLED")
    print("Region:", region)
    print("File path:", file_path)
    if not os.path.exists(file_path):
        print("❌ File not found")
        return None

    job_id = generate_job_id()

    file_name = upload_to_s3(file_path, job_id)
    run_ec2(region, file_name, job_id)

    return job_id


# ✅ KEEP THIS for manual testing (optional)
if __name__ == "__main__":
    region = input("Enter region (e.g., us-east-1, ap-south-1): ")
    file_path = input("Enter file path (.py or .zip): ")

    run_job(region, file_path)