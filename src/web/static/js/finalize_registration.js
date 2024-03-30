// static/js/finalize_registration.js

function toggleOIDCToken() {
    var x = document.getElementById("oidc_token");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
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
