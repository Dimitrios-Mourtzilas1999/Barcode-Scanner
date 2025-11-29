  
  document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebarMenu");

  document.addEventListener("mousemove", function(e) {
        if (e.clientX <= 5) { // 5px from left edge
            sidebar.style.left = "0"; // slide in
        }
    });

    // Detect mouse leaving sidebar
    sidebar.addEventListener("mouseleave", function() {
        sidebar.style.left = "-250px"; // slide out
    });
  });