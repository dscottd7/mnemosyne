window.onload = function() {
    // Get the form element
    let form = document.querySelector('form');
    // Add an event listener for form submission
    form.addEventListener('submit', async function(event) {
      
      // Prevent the form from being submitted normally
      event.preventDefault();

      // Get the message input from the form
      let message = document.querySelector('textarea[name="message"]').value;

      // Create a new div element
      const messageDiv = document.createElement('div');

      // Set the style class of the new div
      messageDiv.className = 'container';

      // Set the text content of the new div
      messageDiv.textContent = message;

      // Add the new div to the page
      document.getElementById('exchange').appendChild(messageDiv);

      // Insert loading spinner
    //   let spinner = document.createElement('div');
    //     spinner.className = 'loader';
    //     document.getElementById('exchange').appendChild(spinner);

      // Insert cat gif
        let catGif = document.createElement('img');
            catGif.src = 'https://media.tenor.com/sqzfIppwAWYAAAAi/pop-cat.gif';
            catGif.style.width = '5%';
            document.getElementById('exchange').appendChild(catGif);

      try {
        // Send a POST request to the /chat endpoint
        const response = await fetch('/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: message,
          }),
        });

        const data = await response.json();

        // Create a new div element
        const responseDiv = document.createElement('div');

        // Set the style class of the new div
        responseDiv.className = 'container darker';

        // Set the text content of the new div
        responseDiv.textContent = data.response;

        // Add the new div to the page
        document.getElementById('exchange').appendChild(responseDiv);

        // Remove the loading spinner
        // spinner.remove();
        catGif.remove();

      } catch (error) {
        console.error('Error:', error);
      }
    });
};