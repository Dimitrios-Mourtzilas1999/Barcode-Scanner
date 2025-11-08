document.addEventListener('DOMContentLoaded',()=>{

    const productCard = document.querySelector('.product');
    console.log(productCard);

    productCard.addEventListener('click',()=>{
        let url = window.location.origin + '/product/edit';
        window.location.href = url;
        
    })
})