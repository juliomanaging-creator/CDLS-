const DocumentUpload = () => {
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    const handleUpload = async (file) => {
        if (!allowedTypes.includes(file.type)) {
            throw new Error('Invalid file type');
        }
        
        if (file.size > maxSize) {
            throw new Error('File too large');
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('documentType', 'REG262'); // or 'TITLE'

        await fetch('/api/v1/documents/upload', {
            method: 'POST',
            body: formData
        });
    };
};