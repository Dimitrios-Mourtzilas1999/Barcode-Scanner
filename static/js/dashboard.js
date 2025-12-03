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
    const savedBarcode = localStorage.getItem('barcode');
    const filtersSubmit= document.querySelector('.apply-filters');
    console.log(filtersSubmit);

    filtersSubmit.addEventListener('click', async (e) => {
        e.preventDefault(); // prevent default form submission

        const data = {
            category: categorySelect.value,
            barcode: barcodeInput.value
        };

        try {
            const response = await fetch('/filters', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log(result);
            // optionally update the page with results
        } catch (err) {
            console.error('Error:', err);
        }
    });


    if (savedBarcode) {
        barcodeInput.value = savedBarcode;
        localStorage.removeItem('barcode');
    }

    resetBtn.addEventListener('click', () => {
        // 1️⃣ Reset the form fields
        filterForm.reset();

        // 2️⃣ Redirect to dashboard without query parameters
        window.location.href = '/dashboard';

        // 3️⃣ Close the modal (optional if using Bootstrap modal)
        const filterModal = bootstrap.Modal.getInstance(document.querySelector('#filterModal'));
        if (filterModal) filterModal.hide();
    });

    filterForm.addEventListener('submit', (e) => {
        e.preventDefault(); // prevent default form submission

        // Get selected filter values
        const selectedCategory = categorySelect.value.trim();
        const selectedBarcode = barcodeInput ? barcodeInput.value.trim() : '';

        // Build URL with query parameters
        const params = new URLSearchParams();

        if (selectedCategory) params.append('category', selectedCategory);
        if (selectedBarcode) params.append('barcode', selectedBarcode);

        // Redirect to dashboard with filters applied
        window.location.href = `/dashboard?${params.toString()}`;
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

