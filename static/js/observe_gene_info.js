document.addEventListener('DOMContentLoaded', function () {
  const plotSection = document.querySelector('.plot-section');
  const plotSentinel = plotSection.querySelector('.plot-section .sentinel');

  const observerOptions = {
    root: null,
    threshold: 0.5
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.target === plotSentinel) {
        plotSection.classList.toggle('active', entry.isIntersecting);
      }
    });
  }, observerOptions);

  if (plotSentinel) {
    observer.observe(plotSentinel);
  }
});