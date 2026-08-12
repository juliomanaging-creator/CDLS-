const ProgressTracker = () => {
    const stages = [
        'QUOTE_SUBMITTED',
        'DOCUMENTS_UPLOADED',
        'DOCUMENTS_VERIFIED',
        'PAYMENT_RECEIVED',
        'TRANSFER_PROCESSING',
        'TRANSFER_COMPLETE'
    ];

    const calculateProgress = (currentStage) => {
        const currentIndex = stages.indexOf(currentStage);
        return ((currentIndex + 1) / stages.length) * 100;
    };
};