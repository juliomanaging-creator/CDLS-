# AWS Technical Reference: S3 and Lambda
## Service: Amazon S3
- **Purpose**: Object storage for high-durability data.
- **Security**: Supports AES-256 server-side encryption and IAM bucket policies.
- **Best Practice**: Use 'S3 Versioning' to protect against accidental deletes.

## Service: AWS Lambda
- **Type**: Serverless Compute.
- **Scaling**: Scales automatically based on incoming request volume.
- **Constraint**: Execution timeout is capped at 15 minutes (900 seconds).
