document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup loaded.");

  const extractButton = document.getElementById('extractTextButton');
  const outputDiv = document.getElementById('output');
  const queryInput = document.getElementById('queryInput');
  const sendButton = document.getElementById('sendButton');
  const responseOutput = document.getElementById('responseOutput');
  const spinner = document.getElementById('spinner');  // Get the spinner element

  // Function to show the spinner
  function showSpinner() {
      spinner.style.display = 'block';
  }

  // Function to hide the spinner
  function hideSpinner() {
      spinner.style.display = 'none';
  }

  // Extract Text button functionality
  extractButton.addEventListener('click', () => {
      console.log("Extract Text button clicked.");

      // Show the spinner while the extraction is processing
      showSpinner();
      outputDiv.textContent = "";  // Clear previous text

      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const activeTab = tabs[0];
          console.log("Active tab ID:", activeTab.id);

          // Send a message to the content script to extract text
          chrome.tabs.sendMessage(activeTab.id, { action: 'getText' }, (response) => {
              if (response && response.text) {
                  console.log("Received extracted text from content script.");
                  // outputDiv.textContent = response.text;
                  response.text = "RAG Ready"
              } else {
                  console.log("No text received or an error occurred.");
                  // outputDiv.textContent = 'No text extracted or an error occurred.';
                  response.text = "Please retry"
              }
              
              fetch("http://127.0.0.1:8000/process-text/",).finally(() => {
                // Hide the spinner after receiving the response
                hideSpinner();
                outputDiv.textContent = response.text;
              });
          });
      });
  });

  // Send Query button functionality
  sendButton.addEventListener('click', () => {
      console.log("Send Query button clicked.");

      const userQuery = queryInput.value.trim();
      if (userQuery) {
          console.log("User query:", userQuery);

          showSpinner();
          responseOutput.textContent = "";

          // Send the user query to the backend server
          fetch("http://127.0.0.1:8000/process-query/", {  // Use your backend server URL here
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({ content: userQuery })
          })
          .then(response => response.json())
          .then(data => {
              console.log("Response from backend:", data);
              responseOutput.textContent = data.message;
          })
          .catch(error => {
              console.error("Error sending query to backend:", error);
              responseOutput.textContent = "An error occurred while sending the query.";
          })
          .finally(() => {
              // Hide the spinner after receiving the response
              hideSpinner();
          });
      } else {
          console.log("Query input is empty.");
          responseOutput.textContent = "Please enter a query.";
      }
  });
});
