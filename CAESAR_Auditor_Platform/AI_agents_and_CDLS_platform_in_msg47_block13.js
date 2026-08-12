async function handleRegistration(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    // ADD THIS:
    try {
        const response = await fetch('http://localhost:3001/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('registrationForm').classList.add('hidden');
            document.getElementById('registrationSuccess').classList.remove('hidden');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}