document.addEventListener('DOMContentLoaded',()=>{

    let barcode = "";
    let lastKeyTime = Date.now();
    const scanDelay = 30;

 document.addEventListener("keydown", (event) => {
        const now = Date.now();
        const timeDiff = now - lastKeyTime;
        lastKeyTime = now;

        // If typing is too slow, reset barcode (human typed)
        if (timeDiff > scanDelay) {
            barcode = "";
        }

        // Ignore modifier keys
        if (event.key.length === 1) {
            barcode += event.key;
        }

        // Heuristic: if barcode length reaches expected size, trigger fetch
        // Adjust 8–14 depending on your barcode type
        if (barcode.length >= 12) {
            fetchProduct(barcode);
            console.log(barcode);
            barcode = ""; // reset for next scan
        }
    });



    const modal = document.getElementById('assignModal');
    const modalButton = document.querySelector('.assign_btn');
    const closeButton = document.querySelector('.close');


    if(!modalButton || !closeButton)
    {
        console.error('Element not found');
        return;
    }

    closeButton.addEventListener('click',()=>{
        if(!modal.classList.contains('hidden'))
            modal.classList.add('hidden');
    })
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
    .then(data => {
        alert(data.message || data.error);
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