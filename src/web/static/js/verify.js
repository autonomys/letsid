// static/js/verify.js

document.getElementById('verify-form').onsubmit = function(event) {
    event.preventDefault(); // Prevent the default form submission
    var autoIdValue = document.getElementById('auto_id').value;
    var actionUrl = '/verify/' + encodeURIComponent(autoIdValue);
    window.location.href = actionUrl; // Redirect to the constructed URL
};