document.addEventListener('DOMContentLoaded', () => {
    // ===== ELEMENTS =====
    const table = document.querySelector('#dashboard');
    const tableBody = table.querySelector('tbody');
    const assignForm = document.querySelector('#assignForm');
    const modalBarcodesInput = document.querySelector('#modal-barcodes');
    const productActions = document.getElementById('productActions');
    const selectAll = document.querySelector('#selectAll');
    const assignModal = new bootstrap.Modal(document.getElementById('assignModal'));
    const assignBtn = document.querySelector('#assignBtn');
    const deleteBtn = document.querySelector('.btn-delete');
    const filterBtn = document.querySelector('.filters');
    const filterModalEl = document.getElementById('filtersModal');
    const closeBtn = filterModalEl?.querySelector('.close');
    const filtersApplyBtn = filterModalEl?.querySelector('.apply-filters');
    const paginationEl = document.querySelector('.pagination');

    // ===== EVENT LISTENERS =====
    assignBtn?.addEventListener('click', () => assignModal.show());
    filterBtn?.addEventListener('click', () => filterModalEl.classList.add('active'));
    closeBtn?.addEventListener('click', () => filterModalEl.classList.remove('active'));

    selectAll?.addEventListener('change', (e) => {
        tableBody.querySelectorAll('input.barcode').forEach(cb => cb.checked = e.target.checked);
        updateSelectedRows();
    });

    tableBody.addEventListener('change', e => {
        if (e.target.matches('input.barcode')) updateSelectedRows();
    });

    assignForm?.addEventListener('submit', e => {
        e.preventDefault();
        const selected = Array.from(tableBody.querySelectorAll('input.barcode:checked')).map(cb => cb.value);
        if (!selected.length) { e.preventDefault(); alert("Please select at least one product!"); return; }
        modalBarcodesInput.value = selected.join(',');
    });

    deleteBtn?.addEventListener('click', () => {
        const selected = Array.from(tableBody.querySelectorAll('input.barcode:checked')).map(cb => cb.value);
        if (!selected.length) return alert("Please select at least one product!");
        fetch('/product/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ barcodes: selected })
        }).then(res => res.ok ? location.reload() : alert('Failed to delete'));
    });

    filtersApplyBtn?.addEventListener('click', (e) => {
        e.preventDefault();
        fetchFilteredProducts(1);  // page 1 when applying new filters
        filterModalEl.classList.remove('active');
    });

    // ===== FUNCTIONS =====
    function updateSelectedRows() {
        const selectedRows = Array.from(tableBody.querySelectorAll('input.barcode:checked'));
        productActions.classList.toggle('hidden', selectedRows.length === 0);
        assignBtn.disabled = deleteBtn.disabled = selectedRows.length === 0;
    }

    async function fetchFilteredProducts(page = 1) {
        // Collect filter values
        const filters = {};
        Array.from(filterModalEl.querySelectorAll('input, select')).forEach(input => {
            if (input.name && input.value) filters[input.name] = input.value;
        });
        filters.page = page;

        const response = await fetch('/filters', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(filters)
        });
        const data = await response.json();
        renderTable(data.products);
        renderPagination(data.page, data.pages);
    }

    function renderTable(products) {
        tableBody.innerHTML = "";
        products.forEach((p, i) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td><input type="checkbox" class="barcode" value="${p.barcode}"></td>
                <td>${i + 1}</td>
                <td><a href="/product/edit/${p.barcode}">${p.barcode}</a></td>
                <td>${p.desc}</td>
                <td>${p.stock}</td>
                <td>${p.price}</td>
                <td>${p.updated_at}</td>
                <td>${p.category}</td>
                <td>${p.supplier}</td>
            `;
            tableBody.appendChild(row);
        });
        updateSelectedRows();
    }

    function renderPagination(current, totalPages) {
        paginationEl.innerHTML = "";
        if (totalPages <= 1) return;

     const addPageItem = (label, disabled, callback) => {
    const li = document.createElement("li");
    li.className = `page-item ${disabled ? "disabled" : ""}`;
    li.innerHTML = `<a class="page-link" href="#">${label}</a>`;
    if (!disabled) {
        li.querySelector("a").addEventListener("click", (e) => {
            e.preventDefault();   // <-- prevent page reload
            callback();
        });
    }
    paginationEl.appendChild(li);
};

    addPageItem("«", current === 1, () => fetchFilteredProducts(current - 1));
    for (let i = 1; i <= totalPages; i++) {
        addPageItem(i, false, () => fetchFilteredProducts(i));
    }
    addPageItem("»", current === totalPages, () => fetchFilteredProducts(current + 1));

}

});
