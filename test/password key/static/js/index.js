document.addEventListener("click", function(e) {
    if (e.target.classList.contains("copy")) {
        const text = e.target.dataset.value;
        navigator.clipboard.writeText(text)
            .then(() => console.log("Kopiert:", text))
            .catch(err => console.error("Fehler beim Kopieren:", err));
    }
});
