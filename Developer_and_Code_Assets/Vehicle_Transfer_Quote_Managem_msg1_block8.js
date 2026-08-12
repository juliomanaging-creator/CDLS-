const REG262Handler = {
    validateForm: (formData) => {
        const required = [
            'vehicleIdentificationNumber',
            'licensePlateNumber',
            'sellerInformation',
            'buyerInformation',
            'odometerReading',
            'salePrice'
        ];

        return required.every(field => formData[field]);
    }
};