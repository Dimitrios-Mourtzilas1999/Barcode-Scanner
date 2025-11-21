document.addEventListener('DOMContentLoaded',()=>{


    const modal = document.getElementById('assignModal');
    const modalButton = document.getElementById('assignBtn');
    const searchButton = document.querySelector('.sidebar__search-btn');
    const sidebar = document.getElementById("sidebarMenu");
    const allElements = document.getElementById('selectAll');
    const deleteButton = document.querySelector('.btn-delete');


    deleteButton?.addEventListener('click',()=>{
        const checkboxes = document.querySelectorAll('input[name="barcodes"]:checked');
        const barcodes = Array.from(checkboxes).map(cb => cb.value);
        let url = window.location.origin = 'product/delete';
        console.log(barcodes);
        if(barcodes.length == 0){
            alert('No products selected');
            return;
        }
        fetch(url,{
            method:"POST",
            body:JSON.stringify({'barcodes':barcodes}),
            headers: { 'Content-Type': 'application/json' },

        }).then(response=>{
            return response.json();
        }).then(()=>{
            window.location.reload();
        })
    })

    allElements.addEventListener('click',()=>{
        let checkboxes = document.querySelectorAll('.product-checkbox');
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = selectAll.checked;
        });
    })

    document.addEventListener("mousemove", function(e) {
        if (e.clientX <= 5) { // 5px from left edge
            sidebar.style.left = "0"; // slide in
        }
    });

    // Detect mouse leaving sidebar
    sidebar.addEventListener("mouseleave", function() {
        sidebar.style.left = "-250px"; // slide out
    });

    searchButton.addEventListener('click',()=>{
        let barcode = document.querySelector('.sidebar__input');
        if(barcode.value == ""){
            let warningElement = document.querySelector('.warning-container');
            if(!warningElement) return;
            if(warningElement.classList.contains('hidden')) warningElement.classList.remove('hidden');
            warningElement.textContent = "Εισάγετε barcode";

            
        }
        
    })


    if(!modalButton)
    {
        console.error('Element not found');
        return;
    }

 
    modalButton.addEventListener('click',()=>{
        if(modal.classList.contains('hidden'))
            modal.classList.remove('hidden');
    })
    modalButton.addEventListener('click', function() {
    const selected = Array.from(document.querySelectorAll('input[name="barcodes"]:checked'));
    if (!selected.length) {
        alert('No products selected');
        return;
    }

    document.getElementById('modal-barcodes').value = selected.map(cb => cb.value).join(',');

    const modal = new bootstrap.Modal(document.getElementById('assignModal'));

    modal.show();
});

// Handle form submit via AJAX
document.getElementById('assignForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const barcodes = document.getElementById('modal-barcodes').value.split(',');
    const categoryId = document.getElementById('categories').value;
    const url = window.location.origin + '/assign-to-category';

    fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ barcodes, category_id: categoryId })
    })
    .then(res => res.json())
    .then(() => {
        location.reload(); // refresh dashboard to show changes
    });
});

})


function fetchProduct(barcode){
    fetch(`/fetch-product/${barcode}`)
    .then(response =>{
        if(!response.ok) throw new Error('Product not found')
        return response.json();
    })
    .then((data)=>{
        if(data.status == "success")
            window.location.href = window.location.oeiin
        else
            alert(data.message);
    })
    .catch(err=>{
        console.error(err);
        alert('Product not found');
    })
}