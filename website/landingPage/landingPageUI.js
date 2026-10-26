// Holt sich Elemente
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");

function onImageClick(img) {
    console.log("User presed the Image!");

    // Übernimmt Bild-Quelle
    lightboxImg.src = img.src;
    // Übernimmt Alt-Text
    lightboxImg.alt = img.alt;
    // Zeight das Bild
    lightbox.style.display = "flex";
}

function closeLightbox() {
    // Entfernt das Bild
    lightbox.style.display = "none";
}