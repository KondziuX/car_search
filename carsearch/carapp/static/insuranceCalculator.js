document.addEventListener('DOMContentLoaded', function () {
    const coOwnerSelect = document.getElementById('co-owner');
    const coOwnerDetails = document.getElementById('co-owner-details');
    const calculateButton = document.getElementById('calculate-insurance');
    const insuranceAmountSpan = document.getElementById('insurance-amount');
  
    coOwnerSelect.addEventListener('change', function () {
      if (coOwnerSelect.value === 'yes') {
        coOwnerDetails.classList.remove('d-none');
      } else {
        coOwnerDetails.classList.add('d-none');
      }
    });
  
    calculateButton.addEventListener('click', function () {
      const driverAge = parseInt(document.getElementById('driver-age').value);
      const licenseYears = parseInt(document.getElementById('license-years').value);
      const engineCapacity = parseInt(document.getElementById('engine-capacity').value);
      const enginePower = parseInt(document.getElementById('engine-power').value);
      const mileage = parseInt(document.getElementById('mileage').value);
      const coOwner = coOwnerSelect.value === 'yes';
      let coOwnerLicenseYears = 0;
  
      if (coOwner) {
        coOwnerLicenseYears = parseInt(document.getElementById('co-owner-license-years').value);
      }
  
      // Prosty kalkulator ubezpieczenia - przykładowe wartości
      let insuranceAmount = 500; // Bazowa kwota ubezpieczenia
  
      // Dodajemy lub odejmujemy kwotę w zależności od wieku kierowcy
      if (driverAge < 25) {
        insuranceAmount += 300;
      } else if (driverAge > 60) {
        insuranceAmount += 150;
      }
  
      // Dodajemy lub odejmujemy kwotę w zależności od liczby lat posiadania prawa jazdy
      if (licenseYears < 5) {
        insuranceAmount += 250;
      } else if (licenseYears > 20) {
        insuranceAmount -= 100;
      }
  
      // Uwzględniamy pojemność silnika
      if (engineCapacity > 2000) {
        insuranceAmount += 300;
      } else if (engineCapacity < 1000) {
        insuranceAmount -= 200;
      }
  
      // Uwzględniamy moc silnika
      if (enginePower > 150) {
        insuranceAmount += 200;
      } else if (enginePower < 70) {
        insuranceAmount -= 150;
      }
  
      // Uwzględniamy przebieg
      if (mileage > 200000) {
        insuranceAmount += 200;
      }

          // Uwzględniamy liczbę drzwi
    if (num_of_doors < 4) {
        insuranceAmount += 100;
      } else if (num_of_doors > 4) {
        insuranceAmount -= 50;
      }
  
      // Uwzględniamy typ nadwozia
      if (variant === 'Coupe' || variant === 'Kabriolet') {
        insuranceAmount += 200;
      } else if (variant === 'Kombi' || variant === 'Kompakt') {
        insuranceAmount -= 100;
      }
  
      // Uwzględniamy współwłaściciela
      if (coOwner) {
        if (coOwnerLicenseYears < 5) {
          insuranceAmount += 300;
        } else if (coOwnerLicenseYears > 10) {
          insuranceAmount -= 200;
        }
      }
  
      insuranceAmountSpan.textContent = insuranceAmount.toFixed(2);
    });
  });
  