// src/static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const statusMessage = document.getElementById('status-message');
    const sourceDocumentsDiv = document.getElementById('source-documents');

    const API_BASE_URL = window.location.origin; // Dynamically get base URL

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        addMessageToChatBox(query, 'user-message');
        userInput.value = '';
        statusMessage.textContent = 'Thinking...';
        sourceDocumentsDiv.innerHTML = '<p>Retrieving and generating...</p>'; // Clear and show loading

        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Something went wrong on the server.');
            }

            const data = await response.json();
            addMessageToChatBox(data.response, 'bot-message');
            displaySourceDocuments(data.source_documents);
            statusMessage.textContent = '';

        } catch (error) {
            console.error('Error:', error);
            statusMessage.textContent = `Error: ${error.message}`;
            addMessageToChatBox('Sorry, I am unable to process your request at the moment. Please try again later.', 'bot-message');
            sourceDocumentsDiv.innerHTML = '<p>Failed to load source documents.</p>';
        } finally {
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }
    });

    function addMessageToChatBox(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function displaySourceDocuments(documents) {
        sourceDocumentsDiv.innerHTML = ''; // Clear previous documents
        if (documents && documents.length > 0) {
            documents.forEach(doc => {
                const docDiv = document.createElement('div');
                docDiv.classList.add('source-document');
                let content = doc.content.length > 300 ? doc.content.substring(0, 300) + '...' : doc.content;
                let metadataHtml = '';
                if (doc.metadata) {
                    metadataHtml += '<strong>Source:</strong> ' + (doc.metadata.source || 'N/A');
                    if (doc.metadata.id) metadataHtml += `, <strong>ID:</strong> ${doc.metadata.id}`;
                    if (doc.metadata.condition) metadataHtml += `, <strong>Condition:</strong> ${doc.metadata.condition}`;
                    if (doc.metadata.drug1) metadataHtml += `, <strong>Drug1:</strong> ${doc.metadata.drug1}`;
                    if (doc.metadata.drug2) metadataHtml += `, <strong>Drug2:</strong> ${doc.metadata.drug2}`;
                }
                docDiv.innerHTML = `<p>${content}</p><p class="metadata">${metadataHtml}</p>`;
                sourceDocumentsDiv.appendChild(docDiv);
            });
        } else {
            sourceDocumentsDiv.innerHTML = '<p>No specific source documents retrieved for this query, or the information was generated from broad knowledge.</p>';
        }
    }
});