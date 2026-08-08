import datetime
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Насколько ты меня знаешь?", page_icon="🧩")

# --- ИНИЦИАЛИЗА БАЗЫ ДАННЫХ ---
conn = sqlite3.connect("quiz_results.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        name TEXT,
        score TEXT
    )
"""
)
conn.commit()

# --- ВОПРОСЫ И ПРАВИЛЬНЫЕ ОТВЕТЫ ---
QUESTIONS = [
    {
        "num": 1,
        "text": "1. Где я хочу жить в будущем?",
        "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800",
        "options": ["Турция🇹🇷", "США🇺🇸", "Япония🇯🇵"],
        "correct": "США🇺🇸",
    },
    {
        "num": 2,
        "text": "2. Какое направление в разработке мне ближе всего?",
        "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800",
        "options": [
            "Frontend (интерфейсы)",
            "Мобильные игры",
            "Backend / Внутренние системы",
            "Кибербезопасность",
        ],
        "correct": "Backend / Внутренние системы",
    },
    {
        "num": 3,
        "text": "3. Чем я подзаряжаюсь для бодрости в течение дня?",
        "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800",
        "options": [
            "Дневной сон",
            "Любимый энергетик / кофе",
            "Прогулка на свежем воздухе",
            "Сладости",
        ],
        "correct": "Любимый энергетик / кофе",
    },
    {
        "num": 4,
        "text": "4. Какой жанр сериалов или шоу я скорее выберу для отдыха?",
        "img": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800",
        "options": [
            
            "Ситуационные комедии (ситкомы)",
            "Исторические драмы",
            "Ужасы и триллеры",
            "Реалити-шоу",
        ],
        "correct": "Исторические драмы",
    },
    {
        "num": 5,
        "text": "5. Какой у меня стиль решения новых сложных задач?",
        "img": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800",
        "options": [
            "Сразу бросаюсь делать",
            "Сначала всё глубоко изучаю и планирую",
            "Прошу помощи у других",
            "Откладываю до дедлайна",
        ],
        "correct": "Откладываю до дедлайна",
    },
    {
        "num": 6,
        "text": "6. Какой фастфуд мне нравится больше всего?",
        "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
        "options": [ "пицца🍕", "крылышки🍗","роллы🍣","картошка фри🍟"],
        "correct": "роллы🍣",
    },
    {
        "num": 7,
        "text": "7. Что я хочу больше всего на день рождения?",
        "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
        "options": ["ноутбук", "косметика", "новый телефон", "самокат"],
        "correct": "ноутбук",
    },
    {
        "num": 8,
        "text": "8. Как я отношусь к планированию своего времени?",
        "img": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=800",
        "options": [
            "Всё расписано в заметках/календаре",
            "Держу главный план в голове",
            "Полная импровизация",
            "Планирую только важные события",
        ],
        "correct": "Планирую только важные события",
    },
    {
        "num": 9,
        "text": "9. Какое время года мне больше всего по душе?",
        "img": "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?w=800",
        "options": ["зима❄️","осень🍂","весна🌸", "лето☀️"],
        "correct": "осень🍂",
    },
    {
        "num": 10,
        "text": "10. Какая суперсила мне понравилась бы больше всего?",
        "img": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800",
        "options": [
            "Читать мысли",
            "Телепортация в любую точку",
            "Управлять временем",
            "Понимать любой язык с нуля",
        ],
        "correct": "Понимать любой язык с нуля",
    },
]

# --- ИНТЕРФЕЙС ВИКТОРИНЫ ---
st.title("🧩 Насколько ты меня знаешь?")
st.write(
    "Пройди тест и узнай, насколько хорошо ты ориентируешься в моих вкусах, привычках и планах!"
)

user_name = st.text_input("Введи своё имя:")
st.divider()

user_answers = {}

for q in QUESTIONS:
    st.subheader(q["text"])
    st.image(q["img"], use_container_width=True)
    user_answers[q["num"]] = st.radio(
        "Выбери вариант:", q["options"], key=f"q{q['num']}"
    )
    st.divider()

# --- ПРОВЕРКА И СОХРАНЕНИЕ ---
if st.button("🚀 Узнать результат"):
    if not user_name.strip():
        st.warning("Пожалуйста, введи своё имя перед отправкой!")
    else:
        score = 0
        details = []

        for q in QUESTIONS:
            user_ans = user_answers[q["num"]]
            if user_ans == q["correct"]:
                score += 1
                details.append(
                    f"✅ **Вопрос {q['num']}**: Верно! ({q['correct']})"
                )
            else:
                details.append(
                    f"❌ **Вопрос {q['num']}**: Твой ответ '{user_ans}', а правильно — **{q['correct']}**"
                )

        # Сохраняем результат в базу данных
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute(
            "INSERT INTO results (date, name, score) VALUES (?, ?, ?)",
            (now, user_name, f"{score}/10"),
        )
        conn.commit()

        # Итоговое сообщение
        st.subheader(f"Результат {user_name}: {score} из 10 баллов")
        if score >= 8:
            st.balloons()
            st.success("🎉 Вау! Ты знаешь меня практически идеально!")
        elif score >= 5:
            st.info("👍 Хороший результат! Мы действительно неплохо общаемся.")
        else:
            st.error("😜 Кажется, нам стоит получше узнать друг друга!")

        st.divider()
        st.subheader("📊 Разбор ошибок:")
        for item in details:
            st.write(item)

# --- ПАНЕЛЬ ДЛЯ ТЕБЯ (ОБЗОР РЕЗУЛЬТАТОВ) ---
st.divider()
with st.expander("🔒 Вход для владельца (посмотреть результаты)"):
    password = st.text_input("Введи пароль для доступа:", type="password")
    if password == "2011":  # Здесь можно указать любой свой пароль
        st.subheader("📋 Список всех результатов:")
        df = pd.read_sql_query(
            "SELECT date AS 'Дата', name AS 'Имя', score AS 'Баллы' FROM results ORDER BY id DESC",
            conn,
        )
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Пока никто не прошёл тест.")
    elif password:
        st.error("Неверный пароль!")
