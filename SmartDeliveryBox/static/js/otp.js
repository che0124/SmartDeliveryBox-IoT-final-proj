function sendOTP() {
    fetch('/send-otp', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.otp);
        });
}

function verifyOTP() {
    const otp = document.getElementById('otp').value;
    fetch('/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ otp: otp })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        });
}