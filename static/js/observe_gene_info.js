document.addEventListener('DOMContentLoaded', function () {
  const plotSection = document.querySelector('.plot-section');
  const plotSentinel = document.querySelector('.plot-section .sentinel');

  const observerOptions = {
    root: null,
    threshold: 0.5, // At least 50% of the sentinel must be visible
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.intersectionRatio >= 0.5) {
        plotSection.classList.add('active');
      } else {
        plotSection.classList.remove('active');
      }
    });
  }, observerOptions);

  if (plotSentinel) {
    observer.observe(plotSentinel);
  }
});

