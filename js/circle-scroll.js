window.addEventListener('scroll', function() {
    // Get the scroll position
    const scrollY = window.scrollY;
  
    // Select the circles
    const circle1 = document.getElementById('circle1');
    const circle2 = document.getElementById('circle2');
    const circle3 = document.getElementById('circle3');
  
    // Calculate the progress of the scroll (normalize to [0, 1])
    const maxScroll = document.body.scrollHeight - window.innerHeight;
    const scrollProgress = Math.min(scrollY / maxScroll, 1);
  
    // Calculate the movement distance based on scroll progress
    const moveDistance = scrollProgress * 400; // Controls how far they move towards each other

    // Adjust the position of both circles to move towards each other
    circle1.style.transform = `translateX(${moveDistance}px)`;
    circle2.style.transform = `translateX(-${moveDistance}px)`;
    circle3.style.transform = `translateY(${moveDistance/10}px)`;

    // After the circles merge, show new text
    if (scrollY > maxScroll / 2) {
      circle1.style.display = 'none'; // Hide first circle
      circle2.style.display = 'none'; // Hide second circle
      circle3.style.display = 'flex';

    } else if (scrollY > maxScroll / 2 && scrollY < maxScroll / .5 ) { //fix logic to erase glitch
        circle1.style.display = 'none'; // Hide first circle
        circle2.style.display = 'none'; // Hide second circle
        circle3.style.display = 'none'; // Hide third circle
    } else {
    circle1.style.display = 'flex'; // Show first circle again
    circle2.style.display = 'flex'; // Show second circle again
    circle3.style.display = 'none'; // Show second circle again
    }
  });
  