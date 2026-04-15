const express = require('express');
const { Ollama } = require('ollama');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

const ollama = new Ollama();

app.use(express.json());

const authenticateKey = (req, res, next) => {
    const apiKey = req.headers['x-api-key'];
    
    if (!apiKey || apiKey !== process.env.API_KEY) {
        return res.status(401).json({ error: 'Unauthorized: Invalid or missing API key.' });
    }
    
    next();
};

app.get('/api/ping', async (req, res) => {
        res.json({ response: "pong" });
})
app.post('/api/generate', authenticateKey, async (req, res) => {
    const { model, messages } = req.body;
    if (!model || !messages) return res.status(400).json({ error: 'Missing required fields: "model" and "prompt".' });
    console.log(model)
    console.log(messages)
    try {
        const response = await ollama.chat({
            model: model,
            messages: messages,
            stream: false,
        });

        res.json({ response: response.message.content });
        console.log(`Response: ${response.message.content}`)
    } catch (error) {
        console.error('Error communicating with Ollama:', error);
        res.status(500).json({ error: 'Internal server error while generating response.' });
    }
});

app.listen(port, () => {
    console.log(`Secure Ollama wrapper listening on port ${port}`);
});