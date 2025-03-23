export function observeDonorSentinel() {
  const donorSection = document.querySelector('.donor-section');
  const donorSentinel = donorSection.querySelector('.sentinel');

  const observerOptions = {
    root: null,
    threshold: 0.5,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.target === donorSentinel) {
        donorSection.classList.toggle('active', entry.isIntersecting);
      }
    });
  }, observerOptions);

  observer.observe(donorSentinel);
}