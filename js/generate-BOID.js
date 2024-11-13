// Generate a random 4-digit BOID
function generateBOID() {
    return Math.floor(1000 + Math.random() * 9000).toString(); // 4-digit number
  }
  
  // Update the DOM with the generated BOID
  document.getElementById('generate-boid-btn').addEventListener('click', function() {
    const generatedBOID = generateBOID();
    document.getElementById('generated-boid').textContent = generatedBOID;
    document.getElementById('add-boid-btn').disabled = false;
  });
  
  // Add the generated BOID to the validBOIDs list in localStorage
  document.getElementById('add-boid-btn').addEventListener('click', function() {
    const newBOID = document.getElementById('generated-boid').textContent;
    
    // Add the new BOID to the validBOIDs list and save it to localStorage
    let validBOIDs = JSON.parse(localStorage.getItem('validBOIDs')) || [];
    if (!validBOIDs.includes(newBOID)) {
      validBOIDs.push(newBOID);
      localStorage.setItem('validBOIDs', JSON.stringify(validBOIDs));
      alert(`Your BigOrderID is ${newBOID}. Start sharing!`);
    } else {
      alert(`BOID ${newBOID} already exists.`);
    }
  });
  