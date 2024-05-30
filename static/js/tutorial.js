 // JavaScript for the lightbox display
 document.getElementById('tutor').addEventListener('click', function() {
    document.getElementById('lightbox-overlay').style.display = 'flex';
  });

  document.getElementById('lightbox-close').addEventListener('click', function() {
    closeLightbox();
  });

  // Close the lightbox when clicking outside the video content
  document.getElementById('lightbox-overlay').addEventListener('click', function(event) {
    if (event.target === this) {
      closeLightbox();
    }
  });

  function closeLightbox(){
    var lightbox = document.getElementById('lightbox-overlay')
    var video = lightbox.querySelector('video');

    lightbox.style.display = 'none';
    video.pause();
    video.currentTime = 0;
  }