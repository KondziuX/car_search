document.addEventListener('DOMContentLoaded', function() {
    const compareCheckboxes = document.querySelectorAll('.compare-checkbox');
    const compareButton = document.getElementById('compare-button');
    const comparisonTableBody = document.getElementById('comparisonTableBody');
    const compareTitlesDiv = document.getElementById('compare-titles');
    let selectedAds = [];
    let selectedAdsTitles = [];

    function updateCompareButton() {
        compareButton.disabled = selectedAds.length < 2;
        compareButton.innerText = 'Porównaj wybrane oferty (' + selectedAds.length + ')';
        if (selectedAds.length === 0) {
            compareButton.style.display = 'none';
            compareTitlesDiv.innerHTML = '';
        } else {
            compareButton.style.display = 'inline-block';
            compareTitlesDiv.innerHTML = '<h5>' + selectedAdsTitles.join(', ') + '</h5>';
        }
    }

    compareCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const adTitle = this.getAttribute('data-ad-title');
            if (this.checked) {
                if (selectedAds.length < 3) {
                    selectedAds.push(this.value);
                    selectedAdsTitles.push(adTitle);
                } else {
                    this.checked = false;
                    alert('Można porównać maksymalnie 3 pojazdy.');
                }
            } else {
                selectedAds = selectedAds.filter(id => id !== this.value);
                selectedAdsTitles = selectedAdsTitles.filter(title => title !== adTitle);
            }
            updateCompareButton();
        });
    });

    compareButton.addEventListener('click', function() {
        if (selectedAds.length >= 2) {
            fetch('/compare-ads/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({ ad_ids: selectedAds })
            })
            .then(response => response.json())
            .then(data => {
                comparisonTableBody.innerHTML = '';

                const attributes = [
                    'Nazwa', 'Zdjęcie', 'Cena', 'Marka', 'Model', 'Typ nadwozia', 'Rok produkcji', 'Pojemność silnika', 'Moc', 
                    'Przebieg', 'Rodzaj paliwa', 'Spalanie w mieście', 'Spalanie poza miastem', 'Spalanie cykl mieszany', 
                    'Emisja CO2', 'Klasa emisji spalin', 'Skrzynia biegów', 'Napęd', 'Ekoplakietka', 'Bezwypadkowy', 
                    'Uszkodzony', 'Stan', 'Czy posiada numer rejestracyjny', 'Zarejestrowany w Polsce', 'Zarejestrowany jako zabytek', 
                    'Pierwszy właściciel', 'Serwisowany w ASO', 'Importowany', 'Prawostronny', 'Homologacja ciężarowa', 'Kolor', 
                    'Typ koloru', 'Liczba drzwi', 'Kraj pochodzenia', 'Wyposażenie'
                ];

                attributes.forEach(attribute => {
                    const row = document.createElement('tr');
                    row.innerHTML = `<th class="align-middle text-end bg-light">${attribute}</th>`;
                    comparisonTableBody.appendChild(row);
                });

                data.forEach(ad => {
                    let idx = 0;
                    comparisonTableBody.querySelectorAll('tr').forEach(row => {
                        if (idx === 0) {
                            row.innerHTML += `<td class="text-center align-middle">${ad.title}</td>`;
                        } else if (idx === 1) {
                            row.innerHTML += `<td class="text-center align-middle"><img src="${ad.featured_image1}" alt="Zdjęcie" class="img-fluid img-compare"></td>`;
                        } else if (attributes[idx] === 'Cena') {
                            row.innerHTML += `<td class="text-center align-middle text-danger fw-bold">${ad.price}</td>`;
                        } else if (idx < attributes.length - 1) {
                            row.innerHTML += `<td class="text-center align-middle">${ad[Object.keys(ad)[idx]]}</td>`;
                        } else {
                            const equipmentArray = Object.values(ad.equipment).flat();
                            const equipmentHtml = equipmentArray.length > 0 ? `<ul>${equipmentArray.map(item => `<li>${item}</li>`).join('')}</ul>` : 'Brak danych';
                            row.innerHTML += `<td class="text-center align-middle">${equipmentHtml}</td>`;
                        }
                        idx++;
                    });
                });

                const modal = new bootstrap.Modal(document.getElementById('compareModal'));
                modal.show();
            });
        }
    });

    updateCompareButton();
});