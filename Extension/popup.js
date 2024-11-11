document.addEventListener('DOMContentLoaded', () => {
  console.log("Popup loaded.");

  const extractButton = document.getElementById('extractTextButton');
  const outputDiv = document.getElementById('output');
  const queryInput = document.getElementById('queryInput');
  const sendButton = document.getElementById('sendButton');
  const responseOutput = document.getElementById('responseOutput');
  const spinner1 = document.getElementById('spinner1');
  const spinner2 = document.getElementById('spinner2');
  const dropdownToggle = document.getElementById('dropdownToggle');
  const instructions = document.getElementById('instructions');
  const arrow = dropdownToggle.querySelector('.arrow');

  // Toggle instructions visibility and arrow direction
  dropdownToggle.addEventListener('click', () => {
    if (instructions.style.display === 'none') {
      instructions.style.display = 'block';
      arrow.classList.remove('down');
      arrow.classList.add('up');
    } else {
      instructions.style.display = 'none';
      arrow.classList.remove('up');
      arrow.classList.add('down');
    }
  });

  function showSpinner(spinner) {
    spinner.style.display = 'block';
  }

  function hideSpinner(spinner) {
    spinner.style.display = 'none';
  }

  extractButton.addEventListener('click', () => {
    console.log("Extract Text button clicked.");

    // Clear output and show spinner1
    outputDiv.textContent = "";
    showSpinner(spinner1);

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const activeTab = tabs[0];
      console.log("Active tab ID:", activeTab.id);

      // Send a message to the content script to extract text
      chrome.tabs.sendMessage(activeTab.id, { action: 'getText' }, (response) => {
        if (response && response.text) {
          console.log("Received extracted text from content script:", response.text);

          // Send the extracted text to background.js to handle the backend request
          chrome.runtime.sendMessage({
            action: "sendTextToBackend",
            content: response.text
          });
        } else {
          console.log("No text received or an error occurred.");
          hideSpinner(spinner1);
          outputDiv.textContent = "Please retry";
        }
      });
    });
  });

  // Listen for messages from background.js to control spinner and display response
  chrome.runtime.onMessage.addListener((message) => {
    if (message.action === "showSpinner") {
      showSpinner(spinner1);
    } else if (message.action === "hideSpinnerAndDisplayResponse") {
      hideSpinner(spinner1);
      outputDiv.textContent = message.responseMessage;
    }
  });

  // Send Query button functionality
  sendButton.addEventListener('click', () => {
    console.log("Send Query button clicked.");

    const userQuery = queryInput.value.trim();
    if (userQuery) {
      console.log("User query:", userQuery);

      showSpinner(spinner2);
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
        responseOutput.innerHTML = marked.parse(data.message);
      })
      .catch(error => {
        console.error("Error sending query to backend:", error);
        responseOutput.textContent = "An error occurred while sending the query.";
      })
      .finally(() => {
        // Hide the spinner after receiving the response
        hideSpinner(spinner2);
      });
    } else {
      console.log("Query input is empty.");
      responseOutput.textContent = "Please enter a query.";
    }
  });
});