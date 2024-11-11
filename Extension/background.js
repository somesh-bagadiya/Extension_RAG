let requestInProgress = false; // Flag to track if a request is in progress

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "sendTextToBackend" && !requestInProgress) {
        console.log("Received text from content script");

        requestInProgress = true; // Set the flag to true

        // Show spinner
        chrome.runtime.sendMessage({ action: "showSpinner" });

        // Send request to the backend
        fetch("http://127.0.0.1:8000/process-text/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content: request.content })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Response from backend:", data);
                chrome.runtime.sendMessage({
                    action: "hideSpinnerAndDisplayResponse",
                    responseMessage: "RAGE is ready."
                });
            })
            .catch(error => {
                console.error("Error sending text to backend (Background.js):", error);
                chrome.runtime.sendMessage({
                    action: "hideSpinnerAndDisplayResponse",
                    responseMessage: "An error occurred while processing the text."
                });
            })
            .finally(() => {
                requestInProgress = false; // Reset the flag after the request is complete
            });
    }
});
