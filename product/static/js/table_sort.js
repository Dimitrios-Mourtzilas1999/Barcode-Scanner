document.addEventListener("DOMContentLoaded", () => {
  const table = document.querySelector(".products-table");
  const tbody = document.querySelector("#productTableBody");
  const headers = table.querySelectorAll("th[data-sort]");

  headers.forEach(header => {
    header.addEventListener("click", () => {
      const sortKey = header.dataset.sort;
      const currentOrder = header.classList.contains("asc") ? "asc" : 
                           header.classList.contains("desc") ? "desc" : null;

      // Reset all icons
      headers.forEach(h => h.classList.remove("asc", "desc"));

      // Determine new sort order
      const newOrder = currentOrder === "asc" ? "desc" : "asc";
      header.classList.add(newOrder);

      // Get rows
      const rows = Array.from(tbody.querySelectorAll("tr"));

      // Define sort function
      const getCellValue = (row, key) => {
        switch (key) {
          case "index": return parseInt(row.children[0].textContent.trim());
          case "barcode": return row.children[1].textContent.trim();
          case "desc": return row.children[2].textContent.trim().toLowerCase();
          case "category": return row.children[3].textContent.trim().toLowerCase();
          case "stock": return parseFloat(row.children[4].textContent.trim()) || 0;
          case "price": 
            return parseFloat(row.children[5].textContent.replace("€", "").trim()) || 0;
          default: return row.textContent.trim().toLowerCase();
        }
      };

      // Sort rows
      rows.sort((a, b) => {
        const valA = getCellValue(a, sortKey);
        const valB = getCellValue(b, sortKey);

        if (typeof valA === "number" && typeof valB === "number") {
          return newOrder === "asc" ? valA - valB : valB - valA;
        } else {
          return newOrder === "asc" 
            ? valA.localeCompare(valB)
            : valB.localeCompare(valA);
        }
      });

      // Rebuild table body
      tbody.innerHTML = "";
      rows.forEach(row => tbody.appendChild(row));
    });
  });
});
