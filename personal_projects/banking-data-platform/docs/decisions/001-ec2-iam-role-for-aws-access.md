# ADR 001 — Use IAM Role for EC2 AWS Access

## Context

The EC2 instance needs access to AWS services such as Amazon S3.

## Decision

Use an IAM Role attached to the EC2 instance instead of storing AWS access keys on the server.

## Rationale

- Avoids storing long-lived credentials.
- Provides temporary AWS credentials through the EC2 instance.
- Centralizes permission management through IAM.
- Supports the principle of least privilege.

## Consequences

The EC2 instance can securely access AWS services according to the permissions defined in the IAM Role.