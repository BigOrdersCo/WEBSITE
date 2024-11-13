// Get the text elements for "For Customers" and "For Restaurants"
const forCustomers = document.getElementById('forCustomers');
const forRestaurants = document.getElementById('forRestaurants');

// Get the content sections for Customers and Restaurants
const customersContent = document.getElementById('customersContent');
const restaurantsContent = document.getElementById('restaurantsContent');

// Function to toggle the active class on the selected element
function toggleSelection(selectedElement, otherElement, selectedContent, otherContent) {
  // Remove 'active' class from the other element and hide its content
  otherElement.classList.remove('active');
  otherContent.classList.remove('visible');

  // Add 'active' class to the selected element and show its content
  selectedElement.classList.add('active');
  selectedContent.classList.add('visible');
}

// Set up event listeners for each text
forCustomers.addEventListener('click', function() {
  toggleSelection(forCustomers, forRestaurants, customersContent, restaurantsContent);
});

forRestaurants.addEventListener('click', function() {
  toggleSelection(forRestaurants, forCustomers, restaurantsContent, customersContent);
});

// Optional: Initialize the default selection (e.g., "For Customers" is selected by default)
toggleSelection(forCustomers, forRestaurants, customersContent, restaurantsContent);
