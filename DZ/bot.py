import asyncio
from datetime import date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
from database import Database

# Инициализация бота и БД
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
db = Database()


# States для FSM
class HabitForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_frequency = State()


# Клавиатуры
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои привычки"), KeyboardButton(text="➕ Новая привычка")],
            [KeyboardButton(text="✅ Отметить сегодня"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="🗑 Удалить привычку"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard


def habits_keyboard(habits):
    keyboard = InlineKeyboardBuilder()
    for habit_id, name, *_ in habits:
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"habit_{habit_id}"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def habit_detail_keyboard(habit_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Выполнено сегодня", callback_data=f"done_{habit_id}"))
    keyboard.add(InlineKeyboardButton(text="❌ Не выполнено", callback_data=f"undone_{habit_id}"))
    keyboard.add(InlineKeyboardButton(text="📊 Статистика", callback_data=f"stats_{habit_id}"))
    keyboard.add(InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{habit_id}"))
    keyboard.adjust(1)
    return keyboard.as_markup()


def confirmation_keyboard(habit_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_{habit_id}"))
    keyboard.add(InlineKeyboardButton(text="❌ Нет, отмена", callback_data="cancel_delete"))
    keyboard.adjust(2)
    return keyboard.as_markup()


# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

    welcome_text = """
    🎯 Добро пожаловать в Habit Tracker Bot!

    С помощью этого бота вы сможете:
    • Создавать привычки для отслеживания
    • Отмечать выполнение каждый день
    • Смотреть статистику и прогресс
    • Следить за своей серией (streak)

    Используйте меню ниже или команды:
    /habits - список привычек
    /add - добавить привычку
    /today - что нужно сделать сегодня
    /stats - статистика
    /help - помощь
    """
    await message.answer(welcome_text, reply_markup=main_menu())


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
    📚 **Помощь по использованию бота:**

    **Основные команды:**
    /start - начать работу с ботом
    /habits - показать все ваши привычки
    /add - добавить новую привычку
    /today - показать привычки на сегодня
    /stats - общая статистика
    /help - эта справка

    **Как работать:**
    1. Добавьте привычку через "➕ Новая привычка"
    2. Каждый день отмечайте выполнение через "✅ Отметить сегодня"
    3. Следите за прогрессом в "📊 Статистика"

    **Что такое streak?**
    Это количество дней подряд, когда вы выполняли привычку без пропусков!
    """
    await message.answer(help_text, parse_mode="Markdown")


@dp.message(Command("habits"))
@dp.message(F.text == "📋 Мои привычки")
async def cmd_habits(message: types.Message):
    habits = db.get_user_habits(message.from_user.id)

    if not habits:
        await message.answer("У вас пока нет привычек. Добавьте первую через меню!")
        return

    text = "📋 **Ваши привычки:**\n\n"
    for i, (habit_id, name, description, frequency) in enumerate(habits, 1):
        stats = db.get_habit_stats(habit_id, 7)
        text += f"{i}. **{name}**\n"
        if description:
            text += f"   _{description}_\n"
        text += f"   📈 За неделю: {stats['completed']}/7 дней | Streak: {stats['current_streak']} дней\n\n"

    await message.answer(text, parse_mode="Markdown", reply_markup=habits_keyboard(habits))


@dp.message(Command("today"))
@dp.message(F.text == "✅ Отметить сегодня")
async def cmd_today(message: types.Message):
    habits = db.get_today_habits(message.from_user.id)

    if not habits:
        await message.answer("У вас пока нет привычек для отслеживания.")
        return

    today = date.today().strftime("%d.%m.%Y")
    text = f"✅ **Привычки на сегодня ({today}):**\n\n"

    for habit_id, name, description, completed in habits:
        status = "✅" if completed else "⏳"
        text += f"{status} **{name}**\n"
        if description:
            text += f"   _{description}_\n"
        text += f"   [Отметить выполнение](/habit{habit_id})\n\n"

    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("stats"))
@dp.message(F.text == "📊 Статистика")
async def cmd_stats(message: types.Message):
    habits = db.get_user_habits(message.from_user.id)

    if not habits:
        await message.answer("У вас пока нет привычек для статистики.")
        return

    text = "📊 **Ваша статистика:**\n\n"
    total_completed = 0
    total_days = 0
    best_streak = 0

    for habit_id, name, *_ in habits:
        stats = db.get_habit_stats(habit_id, 30)
        total_completed += stats['completed']
        total_days += stats['total_days']
        if stats['current_streak'] > best_streak:
            best_streak = stats['current_streak']

        text += f"• **{name}**: {stats['success_rate']}% успеха (streak: {stats['current_streak']})\n"

    overall_rate = round(total_completed / total_days * 100, 2) if total_days > 0 else 0

    text += f"\n**Общая статистика за 30 дней:**\n"
    text += f"• Выполнено: {total_completed} из {total_days} возможных\n"
    text += f"• Успешность: {overall_rate}%\n"
    text += f"• Лучший streak: {best_streak} дней\n"

    # Простая визуализация
    if overall_rate >= 80:
        text += "🎉 Отличная работа! Вы на правильном пути!"
    elif overall_rate >= 50:
        text += "👍 Хорошие результаты! Продолжайте в том же духе!"
    else:
        text += "💪 Не сдавайтесь! Каждый день - новая возможность!"

    await message.answer(text, parse_mode="Markdown")


# Добавление новой привычки
@dp.message(Command("add"))
@dp.message(F.text == "➕ Новая привычка")
async def cmd_add_habit(message: types.Message, state: FSMContext):
    await message.answer("Введите название новой привычки (например: 'Утренняя зарядка'):")
    await state.set_state(HabitForm.waiting_for_name)


@dp.message(HabitForm.waiting_for_name)
async def process_habit_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Добавьте описание (или отправьте '-' чтобы пропустить):")
    await state.set_state(HabitForm.waiting_for_description)


@dp.message(HabitForm.waiting_for_description)
async def process_habit_description(message: types.Message, state: FSMContext):
    description = message.text if message.text != "-" else ""
    await state.update_data(description=description)

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Ежедневно", callback_data="freq_daily"))
    keyboard.add(InlineKeyboardButton(text="По будням", callback_data="freq_weekdays"))
    keyboard.add(InlineKeyboardButton(text="По выходным", callback_data="freq_weekends"))
    keyboard.adjust(1)

    await message.answer("Выберите частоту выполнения:", reply_markup=keyboard.as_markup())
    await state.set_state(HabitForm.waiting_for_frequency)


@dp.callback_query(F.data.startswith("freq_"), HabitForm.waiting_for_frequency)
async def process_habit_frequency(callback: types.CallbackQuery, state: FSMContext):
    freq_map = {
        "freq_daily": "daily",
        "freq_weekdays": "weekdays",
        "freq_weekends": "weekends"
    }

    data = await state.get_data()
    habit_id = db.add_habit(
        callback.from_user.id,
        data['name'],
        data['description'],
        freq_map[callback.data]
    )

    await callback.message.edit_text(f"✅ Привычка '{data['name']}' успешно добавлена!")
    await state.clear()
    await callback.answer()


# Обработка нажатий на кнопки привычек
@dp.callback_query(F.data.startswith("habit_"))
async def show_habit_detail(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    habits = db.get_user_habits(callback.from_user.id)
    habit = next((h for h in habits if h[0] == habit_id), None)

    if not habit:
        await callback.answer("Привычка не найдена!")
        return

    habit_id, name, description, frequency = habit
    stats = db.get_habit_stats(habit_id, 7)

    text = f"**{name}**\n"
    if description:
        text += f"_{description}_\n\n"

    text += f"📅 Частота: {frequency}\n"
    text += f"📊 За неделю: {stats['completed']}/7 дней\n"
    text += f"🔥 Текущий streak: {stats['current_streak']} дней\n"
    text += f"✅ Успешность: {stats['success_rate']}%\n\n"

    # Отметки за последние 7 дней
    text += "Последние 7 дней:\n"
    for log_date, completed in stats['logs'][-7:]:
        day = date.fromisoformat(log_date).strftime("%d.%m")
        text += f"{day}: {'✅' if completed else '❌'}  "

    await callback.message.edit_text(text, parse_mode="Markdown",
                                     reply_markup=habit_detail_keyboard(habit_id))
    await callback.answer()


@dp.callback_query(F.data.startswith("done_"))
async def mark_habit_done(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    db.mark_habit_done(habit_id)

    # Получаем название привычки для сообщения
    habits = db.get_user_habits(callback.from_user.id)
    habit_name = next((h[1] for h in habits if h[0] == habit_id), "Привычка")

    await callback.answer(f"✅ {habit_name} отмечена как выполненная!")

    # Обновляем сообщение
    await show_habit_detail(callback)


@dp.callback_query(F.data.startswith("undone_"))
async def mark_habit_undone(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    db.mark_habit_undone(habit_id)

    habits = db.get_user_habits(callback.from_user.id)
    habit_name = next((h[1] for h in habits if h[0] == habit_id), "Привычка")

    await callback.answer(f"❌ {habit_name} отмечена как невыполненная")
    await show_habit_detail(callback)


@dp.callback_query(F.data.startswith("stats_"))
async def show_habit_stats(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    stats_30 = db.get_habit_stats(habit_id, 30)
    stats_7 = db.get_habit_stats(habit_id, 7)

    habits = db.get_user_habits(callback.from_user.id)
    habit_name = next((h[1] for h in habits if h[0] == habit_id), "Привычка")

    text = f"📊 **Статистика для '{habit_name}'**\n\n"
    text += f"**За 30 дней:**\n"
    text += f"• Выполнено: {stats_30['completed']} из {stats_30['total_days']} дней\n"
    text += f"• Успешность: {stats_30['success_rate']}%\n"
    text += f"• Текущий streak: {stats_30['current_streak']} дней\n\n"

    text += f"**За 7 дней:**\n"
    text += f"• Выполнено: {stats_7['completed']} из 7 дней\n"
    text += f"• Успешность: {stats_7['success_rate']}%\n\n"

    # Простая визуализация прогресса
    progress_bar_length = 20
    filled = int(stats_30['success_rate'] / 100 * progress_bar_length)
    text += "Прогресс: [" + "▓" * filled + "░" * (progress_bar_length - filled) + "]\n"

    if stats_30['current_streak'] >= 7:
        text += "🔥 Отличная серия! Продолжайте в том же духе!"
    elif stats_30['current_streak'] >= 3:
        text += "👍 Хорошо получается! Не сбавляйте темп!"
    else:
        text += "💪 Начните новую серию сегодня!"

    await callback.message.edit_text(text, parse_mode="Markdown",
                                     reply_markup=habit_detail_keyboard(habit_id))
    await callback.answer()


@dp.callback_query(F.data.startswith("delete_"))
async def ask_delete_confirmation(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[1])

    habits = db.get_user_habits(callback.from_user.id)
    habit_name = next((h[1] for h in habits if h[0] == habit_id), "Привычка")

    text = f"⚠️ Вы уверены, что хотите удалить привычку '{habit_name}'?\n\n"
    text += "Все данные о выполнении будут удалены безвозвратно!"

    await callback.message.edit_text(text, reply_markup=confirmation_keyboard(habit_id))
    await callback.answer()


@dp.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete_habit(callback: types.CallbackQuery):
    habit_id = int(callback.data.split("_")[2])
    db.delete_habit(habit_id, callback.from_user.id)

    await callback.message.edit_text("✅ Привычка успешно удалена!")
    await callback.answer()


@dp.callback_query(F.data == "cancel_delete")
async def cancel_delete(callback: types.CallbackQuery):
    await callback.message.edit_text("Удаление отменено.")
    await callback.answer()


# Удаление привычки через меню
@dp.message(Command("delete"))
@dp.message(F.text == "🗑 Удалить привычку")
async def cmd_delete_habit(message: types.Message):
    habits = db.get_user_habits(message.from_user.id)

    if not habits:
        await message.answer("У вас нет привычек для удаления.")
        return

    text = "🗑 **Выберите привычку для удаления:**\n\n"
    for i, (habit_id, name, description, _) in enumerate(habits, 1):
        text += f"{i}. {name}\n"
        if description:
            text += f"   _{description}_\n"

    await message.answer(text, parse_mode="Markdown", reply_markup=habits_keyboard(habits))


# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
