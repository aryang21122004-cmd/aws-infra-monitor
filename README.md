\# aws-infra-monitor



A lightweight Python daemon that continuously audits AWS EC2 

infrastructure and dispatches real-time alerts via SNS when 

instances enter a stopped or failed state.



\## How it works



1\. Authenticates to AWS via environment variables (IAM credentials)

2\. Polls EC2 every 30 seconds using boto3 `describe\_instances()`

3\. Evaluates each instance against expected state

4\. If a monitored instance is stopped — publishes to an SNS topic

5\. SNS delivers an email alert to all topic subscribers instantly



\## Stack

\- Python · boto3 (AWS SDK)

\- AWS EC2 · AWS SNS · AWS IAM

\- python-dotenv (credential management)



\## Setup



\### 1. Create SNS Topic

\- AWS Console → SNS → Create topic (Standard)

\- Add your email as a subscriber

\- Confirm the subscription email



\### 2. Create IAM credentials

Your IAM user needs these permissions:

\- `ec2:DescribeInstances`

\- `sns:Publish`



\### 3. Configure environment

```bash

cp .env.example .env

\# Fill in your values

```



\### 4. Run

```bash

pip install boto3 python-dotenv

python monitor.py

```



\## Validated via failure simulation

Manually stopped the monitored EC2 instance while the script 

was running. Alert email received within 30 seconds of state change.



\## Environment Variables

| Variable | Description |

|---|---|

| `AWS\_ACCESS\_KEY\_ID` | IAM access key |

| `AWS\_SECRET\_ACCESS\_KEY` | IAM secret key |

| `AWS\_REGION` | Target region (e.g. ap-south-1) |

| `SNS\_TOPIC\_ARN` | Full ARN of your SNS alert topic |

| `MONITORED\_INSTANCE` | Name tag of instance to watch |

