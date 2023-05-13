import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

# Настройки бота и логирования
logging.basicConfig(level=logging.INFO)
bot = Bot(token='YOUR_TOKEN_HERE')
dp = Dispatcher(bot, storage=MemoryStorage())

# Определение стейтов
class PetContest(StatesGroup):
    waiting_for_name = State()
    waiting_for_photo = State()
    waiting_for_description = State()

# Команда /start для начала работы с ботом
@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для сбора заявок на участие в конкурсе самых забавных питомцев. Для того, чтобы зарегистрировать своего питомца, напиши его имя.")

    # Переход в стейт ожидания имени
    await PetContest.waiting_for_name.set()

# Обработка имени питомца
@dp.message_handler(state=PetContest.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    # Переход в стейт ожидания фото
    await PetContest.waiting_for_photo.set()
    await message.reply("Отлично! Теперь отправьте фотографию своего питомца.")

# Обработка фото питомца
@dp.message_handler(content_types=types.ContentType.PHOTO, state=PetContest.waiting_for_photo)
async def process_photo(message: types.Message, state: FSMContext):
    # Сохраняем фото питомца на сервере Telegram
    file_id = message.photo[-1].file_id

    # Сохраняем данные в контексте FSM
    async with state.proxy() as data:
        data['photo'] = file_id

    # Переход в стейт ожидания описания
    await PetContest.waiting_for_description.set()
    await message.reply("Отлично! Теперь опишите своего питомца.")

# Обработка описания питомца
@dp.message_handler(state=PetContest.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    # Сохраняем описание питомца
    async with state.proxy() as data:
        data['description'] = message.text

    # Получаем данные из контекста FSM
    data = await state.get_data()

    # Отправляем сообщение о том, что заявка на участие зарегистрирована
    await bot.send_message(chat_id=message.chat.id, text=md.text(
    md.text("Заявка на участие в конкурсе зарегистрирована!"),
    md.text(f"Имя питомца: {data['name']}"),
    md.text(f"Описание питомца: {data['description']}"),
    md.text("Спасибо за участие в конкурсе!")
    ), parse_mode=ParseMode.MARKDOWN)

# Очистка контекста FSM
await state.finish()

if name == 'main':
    from aiogram import executor executor.start_polling(dp.skip_updates=True)