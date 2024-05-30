document.addEventListener('DOMContentLoaded', function() {
    const vehiclePriceElement = document.getElementById('vehicle-price');
    const vehiclePrice = parseFloat(vehiclePriceElement.getAttribute('data-vehicle-price'));
    const downPaymentInput = document.getElementById('down-payment');
    const downPaymentSlider = document.getElementById('down-payment-slider');
    const installmentsInput = document.getElementById('installments');
    const installmentsSlider = document.getElementById('installments-slider');
    const monthlyPaymentElement = document.getElementById('monthly-payment');
    const installmentCountElement = document.getElementById('installment-count');
    const loanAmountElement = document.getElementById('loan-amount');
  
    function calculateLoan() {
      const downPayment = parseFloat(downPaymentInput.value) || 0;
      const installments = parseInt(installmentsInput.value) || 3;
      const loanAmount = vehiclePrice - downPayment;
      const monthlyPayment = loanAmount / installments;
  
      loanAmountElement.innerText = loanAmount.toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      monthlyPaymentElement.innerText = monthlyPayment.toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      installmentCountElement.innerText = installments;
    }
  
    downPaymentInput.addEventListener('input', function() {
      downPaymentSlider.value = downPaymentInput.value;
      calculateLoan();
    });
  
    downPaymentSlider.addEventListener('input', function() {
      downPaymentInput.value = downPaymentSlider.value;
      calculateLoan();
    });
  
    installmentsInput.addEventListener('input', function() {
      installmentsSlider.value = installmentsInput.value;
      calculateLoan();
    });
  
    installmentsSlider.addEventListener('input', function() {
      installmentsInput.value = installmentsSlider.value;
      calculateLoan();
    });
  
    calculateLoan();
  });
  