document.addEventListener('DOMContentLoaded', () => {

    // Elements
    const modal = document.getElementById('assignModal');
    const modalButton = document.getElementById('assignBtn');
    const allElements = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.product-checkbox');
    const deleteButton = document.querySelector('.btn-delete');
    const actionsModal = document.getElementById('productActions');
    const barcodeInput = document.getElementById('barcode');
    const table = document.querySelector('#productTable');
    const tbody = table.querySelector('tbody');
    const headers = table.querySelectorAll('thead th[data-sort]');
    const filterForm = document.querySelector('#filterForm');
    const categorySelect = document.querySelector('#category');
    const resetBtn = document.querySelector('#resetFilters');
    const searchBtn = document.getElementById('barcodeSearchBtn')

    searchBtn.addEventListener('click', () => {
        const barcode = barcodeInput.value.trim();
        if (!barcode) return;

        // Dynamically redirect to the search URL with the barcode
        window.location.href = `/dashboard?barcode=${encodeURIComponent(barcode)}`;
    });

    resetBtn.addEventListener('click', () => {
        // 1️⃣ Reset the select box to default
        filterForm.reset(); // resets category to first option

        // 2️⃣ Show all rows
        Array.from(tbody.querySelectorAll('tr')).forEach(row => {
            row.style.display = '';
        });

        // 3️⃣ Close modal
        const filterModal = bootstrap.Modal.getInstance(document.querySelector('#filterModal'));
        filterModal.hide();
    });

    filterForm.addEventListener('submit', (e) => {
        e.preventDefault(); // prevent form submission

        const selectedCategory = categorySelect.value.trim().toLowerCase();

        Array.from(tbody.querySelectorAll('tr')).forEach(row => {
            const categoryCell = row.children[6]; // 7th column (index 6)
            const categoryText = categoryCell.innerText.trim().toLowerCase();

            if (selectedCategory === '' || categoryText === selectedCategory) {
                row.style.display = ''; // show row
            } else {
                row.style.display = 'none'; // hide row
            }
        });

    // Close modal after applying filter
        const filterModalEl = document.querySelector('#filterModal');
        const filterModal = bootstrap.Modal.getInstance(filterModalEl);
        filterModal.hide();
    });


        headers.forEach((th, headerIndex) => {
        let asc = true;
        th.addEventListener('click', () => {
            sortTableByColumn(headerIndex, asc);
            updateSortIcons(th, asc);
            asc = !asc;
        });
    });

    // Awesomplete for barcode search
    const awesomplete = new Awesomplete(barcodeInput, { minChars: 1, maxItems: 10, autoFirst: true });

    // Show filter modal
    const filterBtn = document.getElementById('filters');
    filterBtn?.addEventListener('click', () => {
        const filterModal = new bootstrap.Modal(document.getElementById('filterModal'));
        filterModal.show();
    });


    function anyChecked() {
        return Array.from(checkboxes).some(cb => cb.checked);
    }

   checkboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            if (anyChecked() && actionsModal.classList.contains('hidden'))
                actionsModal.classList.remove('hidden');
            else 
                actionsModal.classList.add('hidden');
            

            // Update Select All checkbox
            allElements.checked = Array.from(checkboxes).every(c => c.checked);
        });
    });
    // Barcode autocomplete
    barcodeInput?.addEventListener('input', async () => {
        const query = barcodeInput.value;
        if (!query) return;
        try {
            const res = await fetch(`/api/barcodes?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            awesomplete.list = data;
        } catch (err) {
            console.error('Error fetching barcodes:', err);
        }
    });

    allElements?.addEventListener('click', () => {
        
        const checkboxes = document.querySelectorAll('.product-checkbox');
        const anyChecked = document.querySelectorAll('.product-checkbox:checked').length > 0;

        const newState = !anyChecked; // toggle all
        checkboxes.forEach(cb => { cb.checked = newState });

        actionsModal.classList.toggle('hidden', !newState);
    });

    // Delete selected products
    deleteButton?.addEventListener('click', () => {
        const selectedCheckboxes = document.querySelectorAll('.product-checkbox:checked');
        if (!selectedCheckboxes.length) {
            alert('No products selected');
            return;
        }

        const barcodes = Array.from(selectedCheckboxes).map(cb => cb.value);
        fetch(`${window.location.origin}/product/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ barcodes })
        })
        .then(res => res.json())
        .then(() => table.ajax.reload());
    });
    // Convert cell value to comparable type
        function getCellValue(row, index) {
            const cell = row.children[index];
            let text = cell.innerText.trim();

            // Checkbox column
            if (cell.querySelector('input[type="checkbox"]')) return cell.querySelector('input[type="checkbox"]').checked ? 1 : 0;

            // Numeric columns: stock (3), price (4)
            if (index === 3) return parseFloat(text) || 0;
            if (index === 4) return parseFloat(text.replace('€','').replace(',','.')) || 0;

            // Date column (5)
            if (index === 5) {
                const date = new Date(text);
                return isNaN(date) ? new Date(0) : date;
            }

            // All other columns (barcode, description, category)
            return text.toLowerCase();
        }
// Sort rows by column index
    function sortTableByColumn(index, asc = true) {
        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const valA = getCellValue(a, index);
            const valB = getCellValue(b, index);
            if (valA > valB) return asc ? 1 : -1;
            if (valA < valB) return asc ? -1 : 1;
            return 0;
        });

        rows.forEach(row => tbody.appendChild(row));
    }

    function updateSortIcons(activeHeader, asc) {
        // Clear all sort icons first
        document.querySelectorAll('thead th[data-sort] .sort-icon').forEach(span => {
            span.textContent = '';
        });

        // Add arrow to the active header
        const icon = activeHeader.querySelector('.sort-icon');
        if (icon) {
            icon.textContent = asc ? '↑' : '↓';
        }
    }

    // Remove all sort icons
    function clearSortIcons() {
        table.querySelectorAll('.sort-icon').forEach(span => span.textContent = '');
    }

    // Add click listeners to sortable headers
    table.querySelectorAll('thead th[data-sort]').forEach((th, index) => {
        let asc = true; // initial sort order
        th.addEventListener('click', () => {
            sortTableByColumn(index, asc);
            clearSortIcons();
            th.querySelector('.sort-icon').textContent = asc ? '↑' : '↓';
            asc = !asc; // toggle sort order
        });
    });

// Assign to category modal
    modalButton?.addEventListener('click', () => {
        const selected = document.querySelectorAll('.product-checkbox:checked');
        if (!selected.length) {
            alert('No products selected');
            return;
        }

        document.getElementById('modal-barcodes').value = Array.from(selected).map(cb => cb.value).join(',');
        const assignModal = new bootstrap.Modal(modal);
        assignModal.show();
    });

    // Assign form submission
    document.getElementById('assignForm')?.addEventListener('submit', (e) => {
        e.preventDefault();
        const barcodes = document.getElementById('modal-barcodes').value.split(',');
        const categoryId = document.getElementById('category-assign').value;

        fetch(`${window.location.origin}/category/assign-to-category`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ barcodes, category_id: categoryId })
        })
        .then(res => res.json())
        .then(window.location.reload());
    });

});

