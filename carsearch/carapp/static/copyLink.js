function copyLink(advertId) {
  var link = 'http://127.0.0.1:8000/advert/' + advertId;
  navigator.clipboard.writeText(link).then(function() {
    console.log('Link skopiowany do schowka');
    showToast('Link został skopiowany!')
  }, function(err) {
    console.error('Nie udało się skopiować linku: ', err);
    showToast('Nie udało się skopiować linku!')
  });
}

function shareOnMessenger(advertId) {
  var link = 'http://127.0.0.1:8000/advert/' + advertId;
  var messengerUrl = `fb-messenger://share?link=${encodeURIComponent(link)}`;
  window.open(messengerUrl, '_blank');
}

function shareOnWhatsApp(advertId) {
  var link = 'http://127.0.0.1:8000/advert/' + advertId;
  var whatsappUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(link)}`;
  window.open(whatsappUrl, '_blank');
}

function showToast(message) {
  var toastElement = document.getElementById('copyToast');
  var toastBody = toastElement.querySelector('.toast-body');
  toastBody.textContent = message;
  var toast = new bootstrap.Toast(toastElement);
  toast.show();
}
