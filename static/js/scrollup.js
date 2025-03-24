document.addEventListener('DOMContentLoaded', function () {
  const heroTitle = document.querySelector('.hero-title');

  const observerOptions = {
    root: null,
    threshold: 0.5
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.intersectionRatio >= 0.5) {
        heroTitle.classList.add('active');
      } else {
        heroTitle.classList.remove('active');
      }
    });
  }, observerOptions);

  if (heroTitle) {
    observer.observe(heroTitle);
  }
});