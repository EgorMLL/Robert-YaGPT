from config import *
from Logging import *
from database import *
import telebot
import requests

API_TOKEN = TOKEN
bot = telebot.TeleBot(API_TOKEN)

users_history = {}
create_table()



@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=["start"])
def start(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    name = message.from_user.first_name
    markup.add("/help")
    logging.info("Функция start сработала")
    bot.send_message(message.chat.id, f"Приветствую, {name}, рад знакомству! Я бот - помощник, основанный на нейросети. Моя нейросеть может ответить на любые ваши вопросы по математике и рисованию! (разумные конечно)\n"
                                      "Ознакомтесь со списком моих команд по команде /help", reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("/help_with_maths")
    markup.add("/help_with_art")
    markup.add("/debug")
    logging.info("Функция help сработала")
    bot.send_message(message.chat.id, "Конечно! Вот список моих комманд:\n"
                                      "/debug - откладка об ошибках.\n"
                                      "/help_with_maths - нейросеть поможет вам с вопросами по математике.\n"
                                      "/help_with_art - нейросеть поможет вам с вопросами по рисованию..", reply_markup=markup)

def end_task_all(message):
    level = message.text
    return level in message.text.lower()


def filter_hello(message):
    word = "прив"
    return word in message.text.lower()

def filter_bye(message):
    word = "пок"
    return word in message.text.lower()


def record2(message):
    level = message.text
    return level in message.text.lower()


def func(message):
    user_promt = message.text
    return user_promt in message.text.lower()


@bot.message_handler(commands=['help_with_maths', 'help_with_art'])
def record(message):
    user_id = message.from_user.id

    task = ""
    answer = "Ответь на вопрос:"
    level = ""

    update_level(level, user_id)
    update_task(task, user_id)
    update_answer(answer, user_id)

    COMMAND_TO_SUBJECT = {
        '/help_with_art': "рисованию",
        "/help_with_maths": "математике"
    }

    subject_from_user = message.text
    subject = COMMAND_TO_SUBJECT.get(subject_from_user)



    user_id = message.from_user.id

    record_data(user_id, subject)
    select_data(user_id)

    if not subject:  # Если у нас нет названия предмета
        bot.send_message(message.chat.id, "Пожалуйста, выбери предмет, введя одну из команд",
                         # Возвращаемся к предыдущему этапу
                         )
        bot.register_next_step_handler(message, record)

    else:
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("начинающий")
        markup.add("профи")
        bot.send_message(message.chat.id, 'Теперь выбери уровень сложности ответа нейросети: начинающий или профи',
                         reply_markup=markup)
        bot.register_next_step_handler(message, record3)
        logging.info("Функция help_with сработала")



@bot.message_handler(func=record2)
def record3(message):
    user_id = message.from_user.id

    COMMAND_TO_SUBJECT = {
        'начинающий': "начинающий",
        "профи": "профи"
    }

    level_user = message.text
    level = COMMAND_TO_SUBJECT.get(level_user)

    if not level:  # Если у нас нет названия предмета
        bot.send_message(message.chat.id, "Пожалуйста, выбери предмет, введя одну из команд",
                         # Возвращаемся к предыдущему этапу
                         )
        bot.register_next_step_handler(message, record3)

    else:
        update_level(level, user_id)
        bot.send_message(message.chat.id, 'Данные успешно сохранены!')

        bot.send_message(message.chat.id, 'Введите комманду /solve_tusk, чтобы отправить нейросети запрос.')
        bot.register_next_step_handler(message, solve_tusk)





@bot.message_handler(commands=['solve_tusk'])
def solve_tusk(message):
    bot.send_message(message.chat.id, "Напишите новый запрос:")
    bot.register_next_step_handler(message, get_promt)
    logging.info("Функция solve_tusk сработала")


@bot.message_handler(content_types=['text'], func=filter_hello)
def say_hello(message):
    name = message.from_user.first_name
    markup.add("/start")
    bot.send_message(message.from_user.id, text=f"Приветствую, {name}! Если вы ещё не ознакомленны со мной, то введите команду /start", reply_markup=markup)

@bot.message_handler(content_types=['text'], func=filter_bye)
def say_hello(message):
    user_name = message.from_user.first_name
    bot.send_message(message.from_user.id, f"Досвидания, {user_name}!")







@bot.message_handler()
def get_promt(message):

    user_promt = message.text
    if user_promt  == "Прекратить общение":
        user_id = message.from_user.id
        bot.send_message(message.chat.id, "Выход из функции solved_tusk.")
        users_history[user_id] = {}
        logging.debug("Окончание запроса сработало.")
        bot.register_next_step_handler(message, end_task_all)
    else:
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        user_id = message.from_user.id

        if message.content_type != "text":
            bot.send_message(user_id, text="Отправь промт текстовым сообщением")
            bot.register_next_step_handler(message, get_promt)
            return


        if (user_id not in users_history or users_history[user_id] == {}) and user_promt == "Продолжить ответ":
            bot.send_message(user_id, "Чтобы продолжить решение, сначала нужно отправить текст задачи")
            bot.send_message(user_id, "Напиши новый запрос:")
            logging.info("Начался новый запрос от прошлого.")
            bot.register_next_step_handler(message, get_promt)
            return


        gpt.count_tokens(user_promt)

        if len(user_promt) > MAX_TOKENS:
            bot.send_message(user_id, "Запрос превышает количество символов\nИсправь запрос")
            bot.register_next_step_handler(message, get_promt)
            return

        bot.send_message(user_id, "Промт принят!")
        bot.send_message(user_id, "Ожидайте ответа")

        results = cur.execute(f'''
                    SELECT * FROM
                    users
                    WHERE
                    user_id = "{user_id}"
                    LIMIT 1;
                    ''')
        value = results.fetchall()[0]
        subject = value[2]
        level = value[3]
        task = value[4]
        answer = value[5]
        logging.info("ВСЕ ДАННЫЕ УСПЕШНО ВЗЯТЫ ИЗ ТАЮЛИЦЫ.")

        print(answer)
        print(task)

        if user_id not in users_history or users_history[user_id] == {}:

            users_history[user_id] = {
                'system_content': f"Ты - дружелюбный человек, который говорит по русски. Ты {level} по {subject} и отвечаешь на вопрос пользователя по данному предмету. Так же ты приветсвуешь пользователя, если он поздоровался.  "
                              f"Если ты начинающий - отвечай на вопросы кратко, без пояснений, от себя ничего не добавляй. "
                              f"Если ты профи - отвечай на вопрос полностью, если это уместно то поясняй ответ, от себя ничего не добавляй. "
                              f"Ответь на следующий вопрос: ",
                'user_content': user_promt,
                'assistant_content': f"Ответь на вопрос{answer}"
            }

        system_content = users_history[user_id]['system_content']
        assistant_content = answer
        user_promt2 = users_history[user_id]['user_content']


        task = users_history[user_id]['user_content']
        update_task(task, user_id)
        logging.debug("ВОПРОС СОХРАНЁН В БАЗУ ДАННЫХ")

        logging.info("Словарь пользователя создался")
        logging.info("Промт попал к нейросети")

        resp = requests.post(

            GPT_LOCAL_URL,

            headers=HEADERS,

            json={
                "messages": [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_promt2},
                    {"role": "assistant", "content": assistant_content}
                ],
                "temperature": 0.6,
                "max_tokens": MAX_TOKENS,
            }
        )

        answer = resp.json()['choices'][0]['message']['content']
        if answer == "":
            bot.send_message(message.from_user.id, 'Нейросеть дала конечный ответ, невозможно продолжить'
                                                   'Если вы хотите задать вопрос нейросети заново - введите комманды по выбору предмета: /help_with_art или /help_with_maths.')

        update_answer(answer, user_id)
        logging.debug("ВОПРОС СОХРАНЁН В БАЗУ ДАННЫХ")

        if resp.status_code == 200 and 'choices' in resp.json():
            bot.send_message(user_id, answer)
        else:
            logging.critical("КРИТИЧЕСКАЯ ОШИБКА В ПРОГРАММЕ: ПРОМТ НЕ БЫЛ ПОЛУЧЕН В НЕЙРОСЕТЬ.")
            bot.send_message(message.from_user.id, 'Не удалось получить ответ от нейросети')

        answer = resp.json()['choices'][0]['message']['content']
        update_answer(answer, user_id)
        logging.debug("ВОПРОС СОХРАНЁН В БАЗУ ДАННЫХ")

        markup.add("Продолжить ответ")
        markup.add("Прекратить общение")

        bot.send_message(message.from_user.id, 'Хотите ли вы продолжить запрос или начать новый? Выберите варианты:', reply_markup=markup,)


        user_content = message.text

        if user_content == "Продолжить ответ":
            update_answer(answer, user_id)
            bot.register_next_step_handler(message, get_promt)

        elif user_content == "Прекратить общение":
            bot.register_next_step_handler(message, end_task_all)







@bot.message_handler(content_types=["text"])
def end_task(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Текущий запрос отменён.")
    users_history[user_id] = {}
    solve_tusk(message)
    logging.info("Окончание запроса сработало.")




@bot.message_handler(content_types=['text'])
def repeat_message(message):
        bot.send_message(message.from_user.id, f"Извините, я не понял ваш запрос. \n"
                                               "Пожалуйста, введите комманду /start для ознакомления с моими способностями.")

if __name__ == "__main__":
    logging.info("Бот запущен")
    bot.polling(non_stop=True)