// Add button: "Email Results to Dealer"
// onClick event:

const emailData = {
  to: dealerEmail.value,
  from: "julio@cdlsnetwork.com",
  subject: `Your EV ROI Analysis - ${dealerName.value}`,
  html: emailTemplate.value, // your branded template
  attachments: [
    {
      filename: `CDLS_ROI_Analysis_${dealerName.value}.pdf`,
      content: pdfReport.value // auto-generated PDF
    }
  ]
};

sendgridQuery.trigger({
  additionalScope: { emailData }
});

// Show success message
notificationComponent.show("✓ Results emailed to " + dealerEmail.value);