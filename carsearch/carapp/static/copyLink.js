document.addEventListener('DOMContentLoaded', function() {
  var copyToastEl = document.getElementById('copyToast');
  var copyToast = new bootstrap.Toast(copyToastEl);
  var searchToastEl = document.getElementById('searchToast');
  var searchToast = new bootstrap.Toast(searchToastEl);
  var loadSearchButton = document.getElementById('load-search');
  var clearSearchButton = document.getElementById('clear-search');

  // Disable buttons if there is no saved search
  if (!document.cookie.split('; ').find(row => row.startsWith('saved_search'))) {
    loadSearchButton.disabled = true;
    clearSearchButton.disabled = true;
  } else {
    loadSearchButton.disabled = false;
    clearSearchButton.disabled = false;
  }

  if (localStorage.getItem('showToastAfterReload')) {
    var action = localStorage.getItem('showToastAfterReload');
    if (action === 'save'){
      showToast('searchToast', 'Filtry zapisane!');
    }else if (action === 'load'){
      showToast('searchToast', 'Filtry odtworzone!');
    } else if (action === 'clear') {
      showToast('searchToast', 'Filtry wyczyszczone!');
    }
    localStorage.removeItem('showToastAfterReload');
  }

  document.getElementById('save-search').addEventListener('click', function() {
    fetch(window.location.pathname + '?' + new URLSearchParams(new FormData(document.querySelector('form'))).toString() + '&save_search=true')
      .then(response => response.json())
      .then(data => {
        setTimeout(function() {
          localStorage.setItem('showToastAfterReload', 'save');
          window.location.reload();
        })
      })
      .catch(error => console.error('Error:', error));
  });

  document.getElementById('load-search').addEventListener('click', function() {
    localStorage.setItem('showToastAfterReload', 'load');
    setTimeout(function() {
      window.location.href = window.location.pathname + '?load_search=true';
    })
  });

  document.getElementById('clear-search').addEventListener('click', function() {
    fetch(window.location.pathname + '?clear_search=true')
      .then(response => response.json())
      .then(data => {
        setTimeout(function() {
          localStorage.setItem('showToastAfterReload', 'clear');
          window.location.reload();  // Przeładowuje stronę
        })
      })
      .catch(error => console.error('Error:', error));
  });
});

function copyLink(advertId) {
  var link = 'http://127.0.0.1:8000/advert/' + advertId;
  navigator.clipboard.writeText(link).then(function() {
    console.log('Link skopiowany do schowka');
    showToast('copyToast', 'Link został skopiowany!');
  }, function(err) {
    console.error('Nie udało się skopiować linku: ', err);
    showToast('copyToast', 'Nie udało się skopiować linku!');
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

function showToast(toastId, message) {
  var toastElement = document.getElementById(toastId);
  var toastBody = toastElement.querySelector('.toast-body');
  toastBody.textContent = message;
  var toast = new bootstrap.Toast(toastElement);
  toast.show();
}
