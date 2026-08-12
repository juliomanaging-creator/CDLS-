// Serve documents from S3 with signed URLs
const url = await getSignedURL('packages/sovereign/01_SMUD_Application.pdf');
// Expire after 1 hour for security