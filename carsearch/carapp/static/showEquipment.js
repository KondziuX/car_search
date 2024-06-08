document.addEventListener('DOMContentLoaded', function() {
    var equipmentLists = document.querySelectorAll('.equipment ul');
    
    equipmentLists.forEach(function(list) {
        list.style.display = 'none';
        list.previousElementSibling.style.cursor = 'pointer';
        
        list.previousElementSibling.addEventListener('click', function() {
            if (list.style.display === 'none') {
                list.style.display = 'block';
                this.querySelector('i').classList.remove('bi-chevron-down');
                this.querySelector('i').classList.add('bi-chevron-up');
            } else {
                list.style.display = 'none';
                this.querySelector('i').classList.remove('bi-chevron-up');
                this.querySelector('i').classList.add('bi-chevron-down');
            }
        });
    });
});
