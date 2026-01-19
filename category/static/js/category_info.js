document.addEventListener('DOMContentLoaded', function() {
  const selectAllCheckbox = document.getElementById('selectAll');
  const checkboxes = document.querySelectorAll('.products-table tbody .checkbox');

  // Array to store selected barcode values
  let selectedBarcodes = [];

  // Function to update selectedBarcodes array
  function updateSelectedBarcodes() {
    selectedBarcodes = [];
    checkboxes.forEach(cb => {
      if (cb.checked) selectedBarcodes.push(cb.value);
    });
    console.log('Selected barcodes:', selectedBarcodes); // For testing
  }

  // Handle selectAll checkbox
  selectAllCheckbox.addEventListener('change', function() {
    checkboxes.forEach(cb => {
      cb.checked = selectAllCheckbox.checked;
    });
    updateSelectedBarcodes();
  });

  // Handle individual checkboxes
  checkboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      // If any checkbox is unchecked, uncheck selectAll
      if (!cb.checked) {
        selectAllCheckbox.checked = false;
      } else if (Array.from(checkboxes).every(c => c.checked)) {
        // If all checkboxes are checked, check selectAll
        selectAllCheckbox.checked = true;
      }
      updateSelectedBarcodes();
    });
  });
});