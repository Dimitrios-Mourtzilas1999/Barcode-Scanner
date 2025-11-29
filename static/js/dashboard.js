document.addEventListener('DOMContentLoaded', () => {

    // Elements
    const modal = document.getElementById('assignModal');
    const modalButton = document.getElementById('assignBtn');
    const allElements = document.getElementById('selectAll');
    const deleteButton = document.querySelector('.btn-delete');
    const actionsModal = document.querySelector('.product-actions');
    const barcodeInput = document.getElementById('barcode');
    const filterForm = document.getElementById('filterForm');

    // Awesomplete for barcode search
    const awesomplete = new Awesomplete(barcodeInput, { minChars: 1, maxItems: 10, autoFirst: true });

    // Show filter modal
    const filterBtn = document.getElementById('filters');
    filterBtn?.addEventListener('click', () => {
        const filterModal = new bootstrap.Modal(document.getElementById('filterModal'));
        filterModal.show();
    });

    // DataTable initialization
    const table = $('#productTable').DataTable({
        ajax: '/api/products',
        columns: [
            { data: 'select', orderable: false },
            { data: 'barcode' },
            { data: 'desc' },
            { data: 'stock' },
            { data: 'price' },
            { data: 'updated' },
            { data: 'category' }
        ],
        order: [[1, 'asc']],
        rowCallback: function(row, data) {
            // Bind checkbox events
            $(row).find('.product-checkbox').on('change', () => {
                const anyChecked = $('.product-checkbox:checked').length > 0;
                if (anyChecked) {
                    actionsModal.classList.remove('hidden');
                } else {
                    actionsModal.classList.add('hidden');
                }
            });
        }
    });

    // Filter form submit → reload table via Ajax
    filterForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = new URLSearchParams(new FormData(filterForm)).toString();
        table.ajax.url(`/api/products?${query}`).load();
        bootstrap.Modal.getInstance(document.getElementById('filterModal')).hide();
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

    // Select All / Deselect All
    allElements?.addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('.product-checkbox');
        const anyChecked = document.querySelectorAll('.product-checkbox:checked').length > 0;

        const newState = !anyChecked; // toggle all
        checkboxes.forEach(cb => cb.checked = newState);

        if (newState) {
            actionsModal.classList.remove('hidden');
        } else {
            actionsModal.classList.add('hidden');
        }
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
        .then(() => table.ajax.reload());
    });

});
