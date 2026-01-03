document.addEventListener('DOMContentLoaded', () => {

    const tableBody = document.querySelector('#dashboard tbody');
    const assignForm = document.querySelector('#assignForm');
    const modalBarcodesInput = document.querySelector('#modal-barcodes');
    const productActions = document.getElementById('productActions');
    const selectAll = document.querySelector('#selectAll');
    const assignBtn = document.querySelector('#assignBtn');
    const deleteBtn = document.querySelector('.btn-delete');
    const assignModal = new bootstrap.Modal(document.getElementById('assignModal'));
    const filterBtn = document.querySelector('.filters');
    const filterModalEl = document.getElementById('filtersModal');
    const closeBtn = filterModalEl?.querySelector('.close');
    const filtersApplyBtn = filterModalEl?.querySelector('.apply-filters');
    const clearFiltersBtn = filterModalEl?.querySelector('.clear-filters');
    const DEFAULT_SORT = 'date_updated';
    const DEFAULT_ORDER = 'desc';
    const params = new URLSearchParams(window.location.search);


    const currentSort = params.get('sort') || DEFAULT_SORT;
    const currentOrder = params.get('order') || DEFAULT_ORDER;



    // ===== FILTER MODAL =====
    filterBtn?.addEventListener('click', () => filterModalEl.classList.add('active'));
    closeBtn?.addEventListener('click', () => filterModalEl.classList.remove('active'));

    filtersApplyBtn?.addEventListener('click', async (e) => {
        e.preventDefault();

        const filters = {};
        filterModalEl.querySelectorAll('input, select').forEach(el => {
            if (el.name && el.value) filters[el.name] = el.value;
        });
        console.log(filters);

        await fetch('/filters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });

        window.location.href = '/dashboard';
    });

    clearFiltersBtn?.addEventListener('click', async () => {
        await fetch('/clear-filters', { method: 'POST' });
        window.location.href = '/dashboard';
    });

    // ===== SELECTION =====
    selectAll?.addEventListener('change', e => {
        tableBody.querySelectorAll('input.barcode')
            .forEach(cb => cb.checked = e.target.checked);
        updateSelectedRows();
    });

    tableBody?.addEventListener('change', e => {
        if (e.target.matches('input.barcode')) updateSelectedRows();
    });



    function updateSelectedRows() {
        const selected = tableBody.querySelectorAll('input.barcode:checked').length;
        productActions.classList.toggle('hidden', selected === 0);
        assignBtn.disabled = deleteBtn.disabled = selected === 0;
    }

    assignBtn.addEventListener('click',()=>{
        assignModal.show();

    })

    // ===== ASSIGN =====
    assignForm?.addEventListener('submit', e => {
        const selected = [...tableBody.querySelectorAll('input.barcode:checked')]
            .map(cb => cb.value);

        if (!selected.length) {
            e.preventDefault();
            alert("Select at least one product");
            return;
        }
        modalBarcodesInput.value = selected.join(',');
    });

    // ===== DELETE =====
    deleteBtn?.addEventListener('click', async () => {
        const selected = [...tableBody.querySelectorAll('input.barcode:checked')]
            .map(cb => cb.value);

        if (!selected.length) return alert("Select products first");

        const res = await fetch('/product/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ barcodes: selected })
        });

        if (res.ok) location.reload();
        else alert("Delete failed");
    });

document.querySelectorAll('.sort-icon').forEach(btn => {
        const icon = btn.querySelector('i');

        // Initialize dataset order for toggle
        btn.dataset.order = (btn.id === currentSort) ? currentOrder : DEFAULT_ORDER;

        // Initialize icon classes
        if (icon) {
            if (btn.id === currentSort) {
                icon.classList.remove('fa-sort', 'fa-sort-up', 'fa-sort-down');
                icon.classList.add(currentOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
            } else {
                icon.classList.remove('fa-sort-up', 'fa-sort-down');
                icon.classList.add('fa-sort');
            }
        }

        // Click listener for sorting
        btn.addEventListener('click', () => {
            const nextOrder = btn.dataset.order === 'asc' ? 'desc' : 'asc';
            btn.dataset.order = nextOrder;

            // Update URL params
            params.set('sort', btn.id);
            params.set('order', nextOrder);
            params.set('page', 1);

            // Reset all icons to neutral first
            document.querySelectorAll('.sort-icon i').forEach(ic => {
                ic.classList.remove('fa-sort-up', 'fa-sort-down');
                ic.classList.add('fa-sort');
            });

            // Set clicked column icon
            if (icon) {
                icon.classList.remove('fa-sort');
                icon.classList.add(nextOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
            }

            // Redirect to apply sort
            window.location.href = `/dashboard?${params.toString()}`;
        });
    });

});
