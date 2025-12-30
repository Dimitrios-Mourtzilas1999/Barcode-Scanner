document.addEventListener('DOMContentLoaded', () => {

    const table = document.querySelector('#dashboard');
    const filterBtn = document.querySelector('.filters');
    const filterModal = document.querySelector('.filters-modal');
    const sortIcon = document.querySelectorAll('.sort-icon');

    // ===== TABLE SORTING =====
    table?.addEventListener('click', e => {
        const button = e.target.closest('.sort-icon');
        if (!button) return;

        sortRecords(button);
    });


    sortIcon.forEach(icon => {
        icon.addEventListener('click', e => {
            const button = e.target.closest('.sort-icon');
            if (!button) return;
            sortRecords(button);
        });
    });

    const filterInputs = {
        barcode: document.querySelector('#filter-barcode'),
        desc: document.querySelector('#filter-desc'),
        category: document.querySelector('#filter-category'),
        supplier: document.querySelector('#filter-supplier')
    };

    // ===== FILTER MODAL TOGGLE =====
    filterBtn?.addEventListener('click', () => {
        filterModal.classList.add('active'); // CSS handles fade-in
    });

    filterModal?.addEventListener('click', e => {
        if (e.target === filterModal) filterModal.classList.remove('active'); // fade-out
    });

    // ===== TABLE SORTING =====
    table?.addEventListener('click', e => {
        const button = e.target.closest('.sort-icon');
        if (!button) return;
        sortRecords(button);
    });

    function sortRecords(button) {
        const field = button.id;
        const tbody = table.tBodies[0];
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        // toggle asc/desc
        const asc = button.dataset.asc !== "true";
        button.dataset.asc = asc;

        rows.sort((a, b) => {
            const cellA = a.querySelector(`[data-field="${field}"]`)?.textContent.trim().toLowerCase() || '';
            const cellB = b.querySelector(`[data-field="${field}"]`)?.textContent.trim().toLowerCase() || '';

            // numeric sort if both are numbers
            if (!isNaN(cellA) && !isNaN(cellB) && cellA && cellB) {
                return asc ? cellA - cellB : cellB - cellA;
            }

            // string sort
            return asc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        });

        // append sorted rows
        rows.forEach(row => tbody.appendChild(row));

        // update icons
        const icons = table.querySelectorAll('.sort-icon i');
        icons.forEach(i => i.className = 'fa-solid fa-sort'); // reset all
        const icon = button.querySelector('i');
        icon.className = asc ? 'fa-solid fa-sort-up' : 'fa-solid fa-sort-down';
    }
    // ===== TABLE FILTERING =====
    Object.values(filterInputs).forEach(input => {
        input?.addEventListener('input', filterTable);
    });

    function filterTable() {
        const barcodeValue = filterInputs.barcode?.value.trim().toLowerCase() || '';
        const descValue = filterInputs.desc?.value.trim().toLowerCase() || '';
        const categoryValue = filterInputs.category?.value.trim().toLowerCase() || '';
        const supplierValue = filterInputs.supplier?.value.trim().toLowerCase() || '';

        const tbody = table?.tBodies[0];
        if (!tbody) return;

        tbody.querySelectorAll('tr').forEach(row => {
            const cells = row.cells;
            const barcodeCell = cells[1]?.textContent.trim().toLowerCase() || '';
            const descCell = cells[2]?.textContent.trim().toLowerCase() || '';
            const categoryCell = cells[6]?.textContent.trim().toLowerCase() || '';
            const supplierCell = cells[7]?.textContent.trim().toLowerCase() || '';

            const show =
                barcodeCell.includes(barcodeValue) &&
                descCell.includes(descValue) &&
                categoryCell.includes(categoryValue) &&
                supplierCell.includes(supplierValue);

            row.style.display = show ? '' : 'none';
        });
    }

});
