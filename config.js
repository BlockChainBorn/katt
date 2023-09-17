
// Server configuration
export const SERVER_PORT = 3000; // Server port
export const DEBUG = false; // Debug mode

// Prompt Moderation before sending to OpenAI
export const MODERATION = true; // Moderation mode

// Rate limit
export const PRIOD = 15 * 1000; // 15 seconds
export const RATE_LIMIT = 50; // 50 requests per 15 seconds

// Whitelisted IPs
export const WHITELISTED_IPS = [
    // "127.0.0.1"
];

// OpenAI API Keys
export let OPENAI_KEYS = [
    "pk-sDltwisEgCTSpyyUHlQQtpvIETpiwdapnoFwhabZ",
];

// Import OpenAI modules
import { Configuration, OpenAIApi } from "openai";

// Initialize API configuration
const configuration = new Configuration({
    apiKey: "pk-sDltwisEgCTSpyyUHlQQtpvIETpiwdapnoFwhabZ",
    basePath: "https://api.pawan.krd/v1",
});

// Create OpenAI API instance
const openai = new OpenAIApi(configuration);

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
