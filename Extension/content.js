// content.js

// Function to extract all visible text from the webpage
function extractText() {
    console.log("Extracting text from the webpage...");
    
    // Extract text from all visible elements
    const elements = document.querySelectorAll('body *');
    let visibleText = '';
    elements.forEach((element) => {
      const style = window.getComputedStyle(element);
      if (style.display !== 'none' && style.visibility !== 'hidden') {
        visibleText += element.innerText + ' ';
      }
    });
  
    console.log("Text extraction complete.");
    return visibleText.trim();
  }
  
  // Listen for messages from the popup script
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("Received message:", request);
    if (request.action === 'getText') {
      console.log("Extracting text as per request.");
      const text = extractText();
      console.log("Sending extracted text back to popup.");
      sendResponse({ text: text });
    }
  });
  