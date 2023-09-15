import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from transformers import AutoModelForCausalLM, AutoTokenizer
import google.cloud.texttospeech as texttospeech
import logging
import torch

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/gogbergrobin/ez/json/decentrafrens-3a6e81f7a3d9.json'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Hugging Face model
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

# Initialize Google TTS client
client = texttospeech.TextToSpeechClient()

# Initialize context memory
chat_contexts = {}

# Function to handle the /hi command
def hi(update, context):
    try:
        user_message = update.message.text[4:].strip()  # Remove '/hi ' from the message
        input_ids = tokenizer.encode(user_message, return_tensors='pt')
        attention_mask = torch.ones(input_ids.shape)
        output = model.generate(input_ids, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        synthesis_input = texttospeech.SynthesisInput(text=generated_text)
        voice = texttospeech.VoiceSelectionParams(language_code='en-US', name='en-US-Wavenet-D')
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        mp3_file_path = '/tmp/generated_audio.mp3'
        with open(mp3_file_path, 'wb') as out:
            out.write(response.audio_content)
        update.message.reply_audio(audio=open(mp3_file_path, 'rb'))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        update.message.reply_text('An error occurred. Please try again.')

# Function to handle the /start command
def start(update, context):
    update.message.reply_text('Hello! Type /hi followed by your question to begin.')

# Function to handle the /q command
def q(update, context):
    try:
        chat_id = update.message.chat_id
        user_message = update.message.text[3:].strip()  # Remove '/q ' from the message
        if chat_id not in chat_contexts:
            chat_contexts[chat_id] = []
        chat_contexts[chat_id].append(tokenizer.encode(user_message))
        input_ids = torch.tensor(chat_contexts[chat_id]).unsqueeze(0)  # Convert list of lists to tensor
        output = model.generate(input_ids, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        chat_contexts[chat_id].append(tokenizer.encode(generated_text))
        update.message.reply_text(generated_text)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        update.message.reply_text('An error occurred. Please try again.')

# Main function
def main():
    updater = Updater(token='6649805356:AAFKOSiikw3wjUXeoxePcM5jaTdB6QKwBW8', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('hi', hi))
    dispatcher.add_handler(CommandHandler('q', q))
    updater.start_polling()
    updater.idle()

# Run the main function if this script is executed
if __name__ == '__main__':
    main()