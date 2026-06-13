import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import time
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def trigger_alert_notification(instance_name, instance_id, current_state):
    """
    Triggers an AWS SNS topic to send a real Email to the DevOps team.
    """
    print("\n🚨 [ALERT SYSTEM TRIGGERED] 🚨")
    print("📧 Dispatching emergency email via AWS SNS...")
    
    # 1. Format the email subject and body
    subject = f"CRITICAL: EC2 Instance {instance_name} is {current_state.upper()}"
    message = f"""
    ⚠️ AWS INFRASTRUCTURE ALERT ⚠️
    
    Service Impacted: {instance_name}
    Resource ID:      {instance_id}
    Current Status:   {current_state.upper()}
    Region:           {AWS_REGION}
    
    Action Required: Please log into the AWS Console to verify the deployment state immediately.
    """
    
    try:
        # 2. Connect to SNS and fire the message to your Topic ARN
        sns_client = boto3.client('sns', region_name=AWS_REGION)
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        print(f"✅ Email successfully dispatched to Topic Subscribers!")
    except Exception as e:
        print(f"❌ Failed to send email alert: {str(e)}")
        
    print("═" * 50)

def inspect_cloud_resources():
    print(f"🔄 Initializing AWS Resource Audit for region: {AWS_REGION}...")
    print("🔍 Fetching live infrastructure metrics from AWS API...\n")
    
    try:
        ec2_client = boto3.client('ec2', region_name=AWS_REGION)
        response = ec2_client.describe_instances()
        
        instance_count = 0
        alerts_triggered = 0
        
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_count += 1
                instance_id = instance.get('InstanceId')
                state = instance.get('State', {}).get('Name')
                instance_type = instance.get('InstanceType')
                
                tags = instance.get('Tags', [])
                name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'Unnamed Instance')
                
                print(f"🖥️  Monitoring Core Asset: {name_tag}")
                print(f"   ├── ID: {instance_id}")
                print(f"   ├── State: {state.upper()}")
                print(f"   └── Type: {instance_type}")
                
                # Evaluation Logic
                if name_tag == "syspulse-server" and state.lower() == "stopped":
                    trigger_alert_notification(name_tag, instance_id, state)
                    alerts_triggered += 1
                else:
                    print("   └── ✅ Health Check: Status Nominal.")
                print("-" * 50)
                
        print(f"\n📊 --- Audit Summary ---")
        print(f"✅ Total Instances Checked: {instance_count}")
        print(f"⚠️ Total Active Alerts:      {alerts_triggered}")
            
    except (NoCredentialsError, PartialCredentialsError):
        print("❌ Error: AWS Credentials not found or incomplete.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")

import time 

# ... (keep all your other code exactly the same above this) ...

if __name__ == "__main__":
    print("🚀 Starting Continuous Continuous Monitor (Press Ctrl+C to stop)...\n")
    try:
        while True:
            inspect_cloud_resources()
            print("\n⏳ Sleeping for 30 seconds before next health check...")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring manually stopped by user.")