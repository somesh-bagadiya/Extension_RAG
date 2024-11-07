chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "sendTextToBackend") {
        console.log("Received text from content script:", request.content);

        // Send the text data to the Python backend
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
        })
        .catch(error => {
            console.error("Error sending text to backend:", error);
        });
    }
});
