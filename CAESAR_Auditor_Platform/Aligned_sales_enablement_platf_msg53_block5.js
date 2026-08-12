const pdfBlob = doc.output('blob');
const reader = new FileReader();
reader.readAsDataURL(pdfBlob);
reader.onloadend = function() {
  const base64data = reader.result;
  
  // Pass to SendGrid query as attachment
  sendgridQuery.trigger({
    additionalScope: {
      attachments: [{
        content: base64data.split(',')[1],
        filename: `CDLS_Analysis_${dealerName.value}.pdf`,
        type: 'application/pdf',
        disposition: 'attachment'
      }]
    }
  });
};