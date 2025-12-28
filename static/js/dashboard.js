document.addEventListener('DOMContentLoaded', () => {
    const table = $('#dashboard').DataTable(); // Your existing DataTable
    const barcodeInput = document.getElementById('barcode-input');
    const categoryCheckboxes = document.querySelectorAll('input[name="category_filter"]');
    const filterModal = document.querySelector('.filters');
    const applyBtn = document.querySelector('.apply-filters');



    filterModal.addEventListener('click', (e) => {
        if (e.target === filterModal) {
            filterModal.style.display = 'none';
        }
    });
    function getSelectedCategories() {
        return Array.from(categoryCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
    }

    function filterTable() {
        const barcode = barcodeInput.value.trim().toLowerCase();
        const selectedCategories = getSelectedCategories();

        table.rows().every(function () {
            const row = this.node();
            const rowData = this.data();

            // Barcode is in column 2 (index 2)
            const rowBarcode = $(row).find('td:eq(2)').text().toLowerCase();

            // Category is in column 8 (index 8)
            const rowCategory = $(row).find('td:eq(8)').text();

            const barcodeMatch = !barcode || rowBarcode.includes(barcode);
            const categoryMatch = !selectedCategories.length || selectedCategories.includes(rowCategory);

            if (barcodeMatch && categoryMatch) {
                $(row).show();
            } else {
                $(row).hide();
            }
        });
    }

    // Apply filters on button click
    applyBtn.addEventListener('click', (e) => {
        e.preventDefault();
        filterTable();
    });

    // Optional: filter dynamically on input change
    barcodeInput.addEventListener('input', filterTable);
    categoryCheckboxes.forEach(cb => cb.addEventListener('change', filterTable));
});
