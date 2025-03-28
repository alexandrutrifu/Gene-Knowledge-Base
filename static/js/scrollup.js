import {animateArrow} from "./arrow_bounce.js";

document.addEventListener('DOMContentLoaded', function () {
  const hero_container = document.querySelector('.hero-container');
  const hero_title = hero_container.querySelector(".hero-title");
  const arrow = hero_container.querySelector(".down-arrow-container");

  const observerOptions = {
    root: null,
    threshold: 0.5
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.intersectionRatio >= 0.5) {
        hero_container.classList.add('active');
        animateArrow(arrow);
      } else {
        hero_container.classList.remove('active');
      }
    });
  }, observerOptions);

  if (hero_title) {
    observer.observe(hero_title);
  }
});