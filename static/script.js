
function createStar() {
    const star = document.createElement("div");
    star.className = "star";
    const size = Math.random() * 6 + 3; // Size between 3px and 9px
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.left = `${Math.random() * 100}vw`;
    star.style.top = `${Math.random() * 100}vh`;

    document.body.appendChild(star);

    // Remove star after animation
    setTimeout(() => {
        star.remove();
    }, 2000); // Duration should match the animation duration
}

// Create more stars by reducing the interval time
setInterval(createStar, 200); // Create a new star every 200ms
