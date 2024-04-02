// static/js/register.js

function copyToClipboard(elementId) {
    const elementText = document.getElementById(elementId).value;
    navigator.clipboard.writeText(elementText).then(() => {
        showToast('Copied to clipboard!');
    }, (err) => {
        console.error('Could not copy text: ', err);
    });
}

    
function showToast(message) {
    var toast = document.getElementById("toast");
    toast.innerText = 'Copied to clipboard!'; 
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 5000);
}

document.getElementById('registration-form').addEventListener('submit', (event) => {
    console.log('submitting form')
    event.preventDefault();
    const formData = ['public_key', 'private_key', 'seed', 'auto_id', 'jwt_token'].reduce((acc, key) => {
        acc[key] = document.getElementById(key).value;
        return acc;
    }, {});

    fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Registration successful.');
            window.location.href = `/autoID/${formData.auto_id}`;
        } else {
            alert(`Registration failed: ${data.message}`);
        }
    })
    .catch(error => alert(`Error: ${error.message}`));
});