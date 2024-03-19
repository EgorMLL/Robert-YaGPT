
from telebot.types import ReplyKeyboardMarkup
import logging
from transformers import AutoTokenizer






class GPT:

    @staticmethod
    def count_tokens(prompt):
        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
        return len(tokenizer.encode(prompt))




gpt = GPT()


markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)



logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M",
    filename="log_file.txt",
    filemode="w",
)

