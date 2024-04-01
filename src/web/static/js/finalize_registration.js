// static/js/finalize_registration.js

function copyToClipboard(elementId) {
    var element = document.getElementById(`${elementId}_text`).innerText;

    navigator.clipboard.writeText(element.value).then(function() {
        showToast('Copied to clipboard!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });

    document.activeElement.blur();
}
    
function showToast(message) {
    var toast = document.getElementById("toast");
    toast.innerText = 'Copied to clipboard!'; 
    toast.className = "show";
    setTimeout(function(){ toast.className = toast.className.replace("show", ""); }, 5000);
}

document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    
    // Collect form data
    var formData = {
        csr: document.getElementById('csr').value,
        digital_signature: document.getElementById('digital_signature').value,
        oidc_token: document.getElementById('oidc_token').value
    };
    
    // Send the form data as JSON using fetch
    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle registration response
        if (data.status === 'success') {
            // Handle success
            alert('Registration successful.');
            window.location.href = '/'; // Redirect to the homepage or another page
        } else {
            // Handle failure
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => {
        // Handle errors that occur during the fetch
        alert('Error: ' + error.message);
    });
});
