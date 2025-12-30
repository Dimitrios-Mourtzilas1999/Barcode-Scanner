document.addEventListener('DOMContentLoaded', () => {
    // ===== ELEMENTS =====
    const table = document.querySelector('#dashboard');
    const assignForm = document.querySelector('#assignForm');
    const modalBarcodesInput = document.querySelector('#modal-barcodes');
    const productActions = document.getElementById('productActions');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const filterBtn = document.querySelector('.filters');
    const filterModal = new window.bootstrap.Modal(document.getElementById('filtersModal'));
    const assignBtn = document.querySelector('#assignBtn');
    const filters = document.querySelector('#filters');
    const assignModal =new window.bootstrap.Modal(document.getElementById('assignModal'));
    const deleteBtn = document.querySelector('.btn-delete');
    const filterInputs = {
        barcode: document.querySelector('#filter-barcode'),
        desc: document.querySelector('#filter-desc'),
        category: document.querySelector('#filter-category'),
        supplier: document.querySelector('#filter-supplier')
    };

    filters.addEventListener('click', () => {
        filterModal.show();
    });

    deleteBtn.addEventListener('click', () => {
        const selectedBarcodes = Array.from(table.querySelectorAll('tbody input.barcode:checked'))
            .map(cb => cb.value);

        console.log(selectedBarcodes);
        if (!selectedBarcodes.length) {
            alert("Please select at least one product!");
            return;
        }
        fetch('/product/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ barcodes: selectedBarcodes })
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                throw new Error('Failed to delete products');
            }
        }).catch(error => {
            console.error(error);            
        })
        })


    assignBtn.addEventListener('click', () => {
        assignModal.show();
    });

    checkboxes.forEach(cb => {
        cb.addEventListener('change', (e) => {
            const isSelectAll = e.target.id === "selectAll";

            // Handle selectAll checkbox
            if (isSelectAll) {
                checkboxes.forEach(box => {
                    if (box.id !== "selectAll") {
                        box.checked = e.target.checked;
                    }
                });
            }

            // Count how many checkboxes (except selectAll) are checked
            const checkedCount = Array.from(checkboxes)
                .filter(box => box.id !== "selectAll" && box.checked).length;

            // Show modal if at least one checkbox is checked, hide if none
            if (checkedCount > 0) {
                productActions.classList.remove('hidden');
            } else {
                productActions.classList.toggle('hidden');
            }
        });
    });

    // ===== ASSIGN FORM SUBMISSION =====
    assignForm.addEventListener('submit', (e) => {
        const selectedBarcodes = Array.from(table.querySelectorAll('tbody input.barcode:checked'))
            .map(cb => cb.value);

        if (!selectedBarcodes.length) {
            e.preventDefault();
            alert("Please select at least one product!");
            return;
        }

        modalBarcodesInput.value = selectedBarcodes.join(',');
        // Form submits normally (POST)
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
        const asc = button.dataset.asc !== "true";
        button.dataset.asc = asc;

        rows.sort((a, b) => {
            const cellA = a.querySelector(`[data-field="${field}"]`)?.textContent.trim().toLowerCase() || '';
            const cellB = b.querySelector(`[data-field="${field}"]`)?.textContent.trim().toLowerCase() || '';

            if (!isNaN(cellA) && !isNaN(cellB) && cellA && cellB) {
                return asc ? cellA - cellB : cellB - cellA;
            }
            return asc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        });

        rows.forEach(row => tbody.appendChild(row));

        // Update icons
        table.querySelectorAll('.sort-icon i').forEach(i => i.className = 'fa-solid fa-sort');
        const icon = button.querySelector('i');
        icon.className = asc ? 'fa-solid fa-sort-up' : 'fa-solid fa-sort-down';
    }

    // ===== TABLE FILTERING =====
    Object.values(filterInputs).forEach(input => {
        input?.addEventListener('input', filterTable);
    });

    function filterTable() {
        const tbody = table.tBodies[0];
        if (!tbody) return;

        const barcodeValue = filterInputs.barcode?.value.trim().toLowerCase() || '';
        const descValue = filterInputs.desc?.value.trim().toLowerCase() || '';
        const categoryValue = filterInputs.category?.value.trim().toLowerCase() || '';
        const supplierValue = filterInputs.supplier?.value.trim().toLowerCase() || '';

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
