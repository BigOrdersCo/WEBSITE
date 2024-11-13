// Initialize the validBOIDs list from localStorage, or an empty list if not found
let validBOIDs = JSON.parse(localStorage.getItem('validBOIDs')) || ['1234', '5678', '9012', '3456'];

document.getElementById('submit-btn').addEventListener('click', function() {
  const boidInput = document.getElementById('boid-input').value.trim();
  const messageSection = document.getElementById('message-section');

  // Clear any previous messages
  messageSection.innerHTML = '';

  if (boidInput.length !== 4 || isNaN(boidInput)) {
    messageSection.innerHTML = `<p class="failure-message">Please enter a valid 4-digit BOID.</p>`;
    return;
  }

  // Check if the entered BOID exists in the predefined list
  if (validBOIDs.includes(boidInput)) {
    messageSection.innerHTML = `<p class="success-message">Success! BOID ${boidInput} exists.</p>`;
  } else {
    messageSection.innerHTML = `<p class="failure-message">Failure! BOID ${boidInput} does not exist.</p>`;
  }
});
