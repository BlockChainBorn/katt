
// Server configuration
const SERVER_PORT = 3000; // Server port
const DEBUG = false; // Debug mode

// Prompt Moderation before sending to OpenAI
const MODERATION = true; // Moderation mode

// Rate limit
const PRIOD = 15 * 1000; // 15 seconds
const RATE_LIMIT = 50; // 50 requests per 15 seconds

// Whitelisted IPs
const WHITELISTED_IPS = [
    // "127.0.0.1"
];

// OpenAI API Keys
let OPENAI_KEYS = [
    "pk-sDltwisEgCTSpyyUHlQQtpvIETpiwdapnoFwhabZ",
];

// Import OpenAI modules
const { Configuration, OpenAIApi } = require("openai");

// Initialize API configuration
const configuration = new Configuration({
    apiKey: "pk-sDltwisEgCTSpyyUHlQQtpvIETpiwdapnoFwhabZ",
    basePath: "https://api.pawan.krd/v1",
});

// Create OpenAI API instance
const openai = new OpenAIApi(configuration);

async function exampleCall() {
    // Example OpenAI API call
    const response = await openai.createCompletion({
        model: "text-davinci-003",
        prompt: "Human: Hello\nAI:",
        temperature: 0.7,
        max_tokens: 256,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0,
        stop: ["Human: ", "AI: "],
    });

    console.log(response.data.choices[0].text);
}

exampleCall();
