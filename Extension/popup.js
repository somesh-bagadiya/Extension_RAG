// popup.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("Popup loaded.");
    
    const extractButton = document.getElementById('extractTextButton');
    const outputDiv = document.getElementById('output');
  
    extractButton.addEventListener('click', () => {
      console.log("Extract Text button clicked.");
      alert()
      // Query the active tab
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTab = tabs[0];
        console.log("Active tab ID:", activeTab.id);
  
        // Send a message to the content script to extract text
        chrome.tabs.sendMessage(activeTab.id, { action: 'getText' }, (response) => {
          if (response && response.text) {
            console.log("Received extracted text from content script.");
            outputDiv.textContent = response.text;
          } else {
            console.log("No text received or an error occurred.");
            outputDiv.textContent = 'No text extracted or an error occurred.';
          }
        });
      });
    });
  });
  