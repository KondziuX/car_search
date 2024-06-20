document.addEventListener('DOMContentLoaded', function() {
    $('.btn-danger').hide();
    $('input[type="checkbox"]').change(function() {
        var anyChecked = $('input[type="checkbox"]:checked').length > 0;
        var trashButton = $('.btn-danger');
        if (anyChecked) {
            trashButton.show();
        } else {
            trashButton.hide();
        }
    });
    document.querySelector('.btn-danger').addEventListener('click', function() {
        // Wyświetl toast
        const toast = new bootstrap.Toast(document.getElementById('deleteToast'));
        toast.show();
      });
});



