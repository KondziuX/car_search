document.addEventListener('DOMContentLoaded', function() {
    // Wyświetlanie numeru telefonu
    document.getElementById('showPhoneNumber').addEventListener('click', function() {
        var phoneNumber = document.getElementById('phoneNumber').textContent;
        this.innerHTML = phoneNumber;
    });

    // Wyświetlanie adresu email
    document.getElementById('showEmailAddress').addEventListener('click', function() {
        var emailAddress = document.getElementById('emailAddress').textContent;
        this.innerHTML = emailAddress;
    });
});
