const NotificationService = {
    async sendUpdate(quoteId, status) {
        // Send email notification
        await EmailService.send({
            template: 'STATUS_UPDATE',
            data: {
                quoteId,
                status,
                timestamp: new Date()
            }
        });

        // Send SMS if opted in
        if (customer.smsOptIn) {
            await SMSService.send({
                phone: customer.phone,
                message: `Your vehicle transfer quote ${quoteId} status: ${status}`
            });
        }
    }
};