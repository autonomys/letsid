// static/js/utils.js

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
