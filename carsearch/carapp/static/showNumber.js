document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('showPhoneNumber').addEventListener('click', function() {
        var phoneNumber = document.getElementById('phoneNumber').textContent;
        this.innerHTML = phoneNumber;
    });
});
