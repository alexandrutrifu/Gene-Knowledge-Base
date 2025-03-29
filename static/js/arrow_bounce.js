let is_moving = false;

async function addAnimation(arrow, animation_class) {
	return new Promise((resolve) => {
		// Remove residual classNames to start properly
		arrow.classList.remove("move-down", "move-up");

		arrow.classList.add(animation_class);

		// Define animation-end handler
		function handleAnimationEnd() {
			arrow.removeEventListener("animationend", handleAnimationEnd);
			resolve();
		}

		arrow.addEventListener("animationend", handleAnimationEnd);
	});
}

async function startArrowBounceLoop(arrow) {
	is_moving = true;

	while (is_moving) {
		await addAnimation(arrow, "move-down");
		await new Promise((resolve) => setTimeout(resolve, 200));
		await addAnimation(arrow, "move-up");
		await new Promise((resolve) => setTimeout(resolve, 400));
	}
}

export function animateArrow(arrow) {
	const observer_options = {
		root: null,
		threshold: 0.5
	};

	const observer = new IntersectionObserver(entries => {
		for (const entry of entries) {
			if (entry.isIntersecting) {
				if (!is_moving) {
					startArrowBounceLoop(arrow);
				}
			} else {
				// If arrow is not visible, stop animation
				is_moving = false;
			}
		}
	}, observer_options);

	observer.observe(arrow);
}