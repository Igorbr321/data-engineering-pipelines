# AWS Infrastructure

## Overview

AWS provides the cloud infrastructure for the Banking Data Platform.

The current infrastructure includes:

- Amazon EC2
- Amazon S3
- AWS IAM
- VPC
- Security Group
- EC2 Key Pair

---

## AWS Region

```text
us-east-1
```

---

## EC2

| Property | Value |
|---|---|
| Instance Type | `m7i-flex.large` |
| Operating System | Amazon Linux 2023 |
| vCPU | 2 |
| IMDSv2 | Required |
| Key Pair | `keypairaws` |

The EC2 instance will be used to host the project's Airflow environment.

---

## IAM

The EC2 instance uses the IAM Role:

```text
banking-data-platform-ec2-role
```

The role provides the EC2 instance with AWS permissions without storing long-lived access keys on the server.

---

## S3

Data Lake bucket:

```text
banking-data-platform-lake
```

Planned structure:

```text
banking-data-platform-lake/
├── bronze/
└── silver/
```

- **Bronze:** raw data from the banking API.
- **Silver:** processed data generated with PySpark.

S3 uses SSE-S3 encryption.

---

## Network Security

Inbound access to the EC2 instance is restricted to the developer's IP:

| Port | Purpose |
|---|---|
| `22` | SSH |
| `8080` | Airflow |

Ports `80` and `443` are not exposed.

---

## Validation

EC2 → S3 access was successfully validated using the AWS CLI.

```bash
aws sts get-caller-identity
aws s3 ls s3://banking-data-platform-lake
```

The EC2 instance successfully accessed and wrote data to the S3 bucket using the IAM Role.