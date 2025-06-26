document.addEventListener("DOMContentLoaded", function () {
    document.body.dataset.theme = localStorage.getItem("theme") || "auto";
});
