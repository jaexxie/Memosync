 document.addEventListener("DOMContentLoaded", function () {
    var tutorButton = document.getElementById('tutor');
    var lightboxOverlay = document.getElementById('lightbox-overlay');
    var lightboxClose = document.getElementById('lightbox-close');
    var video = lightboxOverlay.querySelector('video');

    tutorButton.addEventListener('click',  function () {
        console.log("Tutor button clicked");
        lightboxOverlay.style.display = 'flex';
        video.play();
    });

    lightboxClose.addEventListener('click', function () {
        console.log("Lightbox close button clicked");
        closeLightbox();
    });

    lightboxOverlay.addEventListener('click', function (event) {
        if (event.target === lightboxOverlay){
            console.log("Lightbox overlay clicked");
            closeLightbox();
        }
    });

    function closeLightbox() {
        lightboxOverlay.style.display = 'none';
        video.pause();
        video.currentTime = 0;
    }
 }); 