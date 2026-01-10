document.addEventListener('DOMContentLoaded', () => {

    // ===== DOM ELEMENTS =====
    const tableBody = document.querySelector('#dashboard tbody');
    const assignForm = document.querySelector('#assignForm');
    const modalBarcodesInput = document.querySelector('#modal-barcodes');
    const productActions = document.getElementById('productActions');
    const selectAll = document.querySelector('#selectAll');
    const assignBtn = document.querySelector('#assignBtn');
    const deleteBtn = document.querySelector('.btn-delete');

    const assignModalEl = document.getElementById('assignModal');
    const assignModal = new bootstrap.Modal(assignModalEl);

    const filterBtn = document.querySelector('.filters');
    const filterModalElDOM = document.getElementById('filtersModal');
    const filterModal = new bootstrap.Modal(filterModalElDOM, { backdrop: 'static', keyboard: false });

    const closeBtn = filterModalElDOM.querySelector('.close');
    const filtersApplyBtn = filterModalElDOM.querySelector('.apply-filters');
    const clearFiltersBtn = filterModalElDOM.querySelector('.clear-filters');

    const DEFAULT_SORT = 'date_updated';
    const DEFAULT_ORDER = 'desc';
    const params = new URLSearchParams(window.location.search);

    const currentSort = params.get('sort') || DEFAULT_SORT;
    const currentOrder = params.get('order') || DEFAULT_ORDER;

    loadFilters();
    updateSortIcons();

    // ===== FILTER MODAL =====
    filterBtn?.addEventListener('click', () => {
        // Add fade-in effect
        filterModalElDOM.classList.add('fade');
        filterModal.show();
    });

    closeBtn?.addEventListener('click', () => filterModal.hide());

    filtersApplyBtn?.addEventListener('click', async (e) => {
        e.preventDefault();

        const filters = {};
        filterModalElDOM.querySelectorAll('input, select').forEach(el => {
            if (el.name && el.value) filters[el.name] = el.value;
        });

        // Save filters to localStorage
        localStorage.setItem('filters', JSON.stringify(filters));

        await fetch('/filters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });

        window.location.href = '/dashboard';
    });

    clearFiltersBtn?.addEventListener('click', async () => {
        await fetch('/clear-filters', { method: 'POST' });
        localStorage.removeItem('filters');
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

    assignBtn?.addEventListener('click', () => assignModal.show());

    // ===== ASSIGN FORM =====
    assignForm?.addEventListener('submit', e => {
        const selected = [...tableBody.querySelectorAll('input.barcode:checked')].map(cb => cb.value);

        if (!selected.length) {
            e.preventDefault();
            alert("Select at least one product");
            return;
        }
        modalBarcodesInput.value = selected.join(',');
    });

    // ===== DELETE =====
    deleteBtn?.addEventListener('click', async () => {
        const selected = [...tableBody.querySelectorAll('input.barcode:checked')].map(cb => cb.value);
        if (!selected.length) return alert("Select products first");

        const res = await fetch('/product/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ barcodes: selected })
        });

        if (res.ok) location.reload();
        else alert("Delete failed");
    });

    // ===== SORTING =====
    document.querySelectorAll('.sort-icon').forEach(btn => {
        const icon = btn.querySelector('i');

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

        btn.addEventListener('click', () => {
            const nextOrder = btn.dataset.order === 'asc' ? 'desc' : 'asc';
            btn.dataset.order = nextOrder;

            params.set('sort', btn.id);
            params.set('order', nextOrder);
            params.set('page', 1);

            // Reset icons
            document.querySelectorAll('.sort-icon i').forEach(ic => {
                ic.classList.remove('fa-sort-up', 'fa-sort-down');
                ic.classList.add('fa-sort');
            });

            // Set clicked icon
            if (icon) icon.classList.add(nextOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down');

            window.location.href = `/dashboard?${params.toString()}`;
        });
    });

    // ===== FILTERS STORAGE =====
    function loadFilters() {
        const filters = JSON.parse(localStorage.getItem('filters'));
        if (!filters) return;
        filterModalElDOM.querySelectorAll('input, select').forEach(el => {
            if (el.name && filters[el.name]) el.value = filters[el.name];
        });
    }

    function updateSortIcons() {
        // optional: highlight default sorted column on page load
    }

});
