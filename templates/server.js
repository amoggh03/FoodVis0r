// server.js

const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const { chat } = require('./gpt'); // Assuming you have a function to interact with GPT

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            const response = await chat(data.message); // Function to interact with GPT
            ws.send(JSON.stringify({ reply: response }));
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

server.listen(3000, () => {
    console.log('Server running on port 3000');
});
