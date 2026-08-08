import datetime
import sqlite3
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# НАСТРОЙКИ СТРАНИЦЫ
# =========================================================

st.set_page_config(
    page_title="Насколько ты меня знаешь?",
    page_icon="🧩",
    layout="centered"
)

# =========================================================
# CSS — КРАСИВЫЙ ДИЗАЙН
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

/* Фон */
.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(255, 105, 180, 0.18), transparent 25%),
        radial-gradient(circle at 90% 10%, rgba(138, 43, 226, 0.18), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(0, 191, 255, 0.12), transparent 30%),
        linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

/* Заголовок */
h1 {
    text-align: center;
    font-weight: 800 !important;
    background: linear-gradient(
        90deg,
        #ff69b4,
        #c77dff,
        #7dd3fc,
        #ff69b4
    );
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 5s linear infinite;
}

@keyframes gradientMove {
    0% { background-position: 0% center; }
    100% { background-position: 300% center; }
}

/* Текст */
p, label, .stMarkdown {
    color: #ffffff !important;
}

/* Карточки вопросов */
div[data-testid="stVerticalBlock"] div[data-testid="stExpander"] {
    border-radius: 20px;
}

/* Картинки */
img {
    border-radius: 20px !important;
    transition: transform 0.3s ease;
}

img:hover {
    transform: scale(1.02);
}

/* Кнопки */
.stButton > button {
    width: 100%;
    border-radius: 18px;
    border: none;
    padding: 15px 20px;
    font-size: 18px;
    font-weight: 700;
    color: white;
    background: linear-gradient(
        135deg,
        #ff4ecd,
        #8b5cf6,
        #3b82f6
    );
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 40px rgba(255, 78, 205, 0.5);
}

/* Поле имени */
input {
    border-radius: 15px !important;
}

/* Радиокнопки */
div[role="radiogroup"] {
    background: rgba(255,255,255,0.06);
    padding: 12px;
    border-radius: 15px;
}

/* Разделители */
hr {
    border-color: rgba(255,255,255,0.15);
}

/* Результат */
.result-box {
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    margin: 20px 0;
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.15);
}

.result-score {
    font-size: 60px;
    font-weight: 800;
    margin: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ЭФФЕКТЫ
# =========================================================

def hearts_effect():
    components.html("""
    <script>
    const hearts = ["❤️","💖","💕","💗","💓","💘","💝"];

    for(let i = 0; i < 45; i++){
        let heart = document.createElement("div");

        heart.innerHTML =
            hearts[Math.floor(Math.random() * hearts.length)];

        heart.style.position = "fixed";
        heart.style.left = Math.random() * 100 + "vw";
        heart.style.top = "100vh";
        heart.style.fontSize = (20 + Math.random() * 35) + "px";
        heart.style.zIndex = "999999";
        heart.style.pointerEvents = "none";

        document.body.appendChild(heart);

        let duration = 2 + Math.random() * 3;

        heart.animate([
            {
                transform: "translateY(0) rotate(0deg)",
                opacity: 1
            },
            {
                transform:
                    "translateY(-110vh) rotate(" +
                    (Math.random() * 720 - 360) +
                    "deg)",
                opacity: 0
            }
        ], {
            duration: duration * 1000,
            easing: "ease-out"
        });

        setTimeout(() => heart.remove(), duration * 1000);
    }
    </script>
    """, height=0)


def fireworks_effect():
    components.html("""
    <script>

    const canvas = document.createElement("canvas");

    canvas.style.position = "fixed";
    canvas.style.left = "0";
    canvas.style.top = "0";
    canvas.style.width = "100vw";
    canvas.style.height = "100vh";
    canvas.style.zIndex = "999998";
    canvas.style.pointerEvents = "none";

    document.body.appendChild(canvas);

    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let particles = [];

    function createFirework(x, y) {

        for(let i = 0; i < 100; i++){

            const angle =
                Math.random() * Math.PI * 2;

            const speed =
                Math.random() * 7 + 2;

            particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 100,
                size: Math.random() * 4 + 2
            });
        }
    }

    createFirework(
        Math.random() * canvas.width,
        canvas.height * 0.35
    );

    setTimeout(() => {
        createFirework(
            canvas.width * 0.25,
            canvas.height * 0.3
        );
    }, 300);

    setTimeout(() => {
        createFirework(
            canvas.width * 0.75,
            canvas.height * 0.3
        );
    }, 600);

    function animate(){

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        particles.forEach((p, index) => {

            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.08;
            p.life--;

            ctx.globalAlpha = p.life / 100;

            ctx.beginPath();

            ctx.arc(
                p.x,
                p.y,
                p.size,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                "hsl(" +
                Math.random() * 360 +
                ",100%,70%)";

            ctx.fill();

            if(p.life <= 0){
                particles.splice(index,1);
            }

        });

        if(particles.length > 0){
            requestAnimationFrame(animate);
        } else {
            canvas.remove();
        }
    }

    animate();

    </script>
    """, height=0)


def sad_effect():
    components.html("""
    <script>

    const emojis = ["😭","💔","🥲","😢"];

    for(let i = 0; i < 25; i++){

        let e = document.createElement("div");

        e.innerHTML =
            emojis[Math.floor(Math.random()*emojis.length)];

        e.style.position = "fixed";
        e.style.left = Math.random()*100 + "vw";
        e.style.top = "-50px";
        e.style.fontSize = "30px";
        e.style.zIndex = "999999";
        e.style.pointerEvents = "none";

        document.body.appendChild(e);

        let duration = 2 + Math.random()*2;

        e.animate([
            {transform:"translateY(0)", opacity:1},
            {transform:"translateY(110vh)", opacity:0}
        ],{
            duration:duration*1000,
            easing:"linear"
        });

        setTimeout(
            () => e.remove(),
            duration*1000
        );
    }

    </script>
    """, height=0)


def sparkle_effect():
    components.html("""
    <script>

    const emojis = ["✨","⭐","🌟","💫"];

    for(let i = 0; i < 35; i++){

        let e = document.createElement("div");

        e.innerHTML =
            emojis[Math.floor(Math.random()*emojis.length)];

        e.style.position = "fixed";
        e.style.left = Math.random()*100 + "vw";
        e.style.top = Math.random()*100 + "vh";
        e.style.fontSize = (15 + Math.random()*30) + "px";
        e.style.zIndex = "999999";
        e.style.pointerEvents = "none";

        document.body.appendChild(e);

        e.animate([
            {transform:"scale(0)", opacity:0},
            {transform:"scale(1.5)", opacity:1},
            {transform:"scale(0)", opacity:0}
        ],{
            duration:1500 + Math.random()*1500,
            easing:"ease-in-out"
        });

        setTimeout(() => e.remove(), 3000);
    }

    </script>
    """, height=0)


# =========================================================
# ЭФФЕКТ ПРИ ПЕРВОМ ВХОДЕ
# =========================================================

if "visited" not in st.session_state:

    st.session_state.visited = True

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:25px;
            border-radius:25px;
            background:rgba(255,255,255,0.08);
            margin-bottom:20px;
        ">
            <h2>✨ Добро пожаловать! ✨</h2>
            <p style="font-size:18px;">
                Сейчас узнаем, насколько хорошо ты меня знаешь 💕
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    sparkle_effect()


# =========================================================
# БАЗА ДАННЫХ
# =========================================================

conn = sqlite3.connect(
    "quiz_results.db",
    check_same_thread=False
)

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


# =========================================================
# ВОПРОСЫ
# =========================================================

QUESTIONS = [

    {
        "num": 1,
        "text": "1. Где я хочу жить в будущем?",
        "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800",
        "options": [
            "Турция🇹🇷",
            "США🇺🇸",
            "Япония🇯🇵"
        ],
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
        "options": [
            "пицца🍕",
            "крылышки🍗",
            "роллы🍣",
            "картошка фри🍟"
        ],
        "correct": "роллы🍣",
    },

    {
        "num": 7,
        "text": "7. Что я хочу больше всего на день рождения?",
        "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
        "options": [
            "ноутбук",
            "косметика",
            "новый телефон",
            "самокат"
        ],
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
        "options": [
            "зима❄️",
            "осень🍂",
            "весна🌸",
            "лето☀️"
        ],
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


# =========================================================
# ЗАГОЛОВОК
# =========================================================

st.title("🧩 Насколько ты меня знаешь?")

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:18px;
        margin-bottom:25px;
    ">
        Пройди тест и узнай, насколько хорошо ты
        знаешь мои вкусы, привычки и планы! 💕
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ИМЯ
# =========================================================

user_name = st.text_input(
    "👤 Введи своё имя:"
)

st.divider()


# =========================================================
# ВОПРОСЫ
# =========================================================

user_answers = {}

for q in QUESTIONS:

    st.subheader(q["text"])

    st.image(
        q["img"],
        use_container_width=True
    )

    user_answers[q["num"]] = st.radio(
        "Выбери вариант:",
        q["options"],
        key=f"q{q['num']}"
    )

    st.divider()


# =========================================================
# КНОПКА РЕЗУЛЬТАТА
# =========================================================

if st.button("🚀 Узнать результат"):

    if not user_name.strip():

        st.warning(
            "⚠️ Пожалуйста, введи своё имя перед отправкой!"
        )

    else:

        score = 0
        details = []

        for q in QUESTIONS:

            user_ans = user_answers[q["num"]]

            if user_ans == q["correct"]:

                score += 1

                details.append(
                    f"✅ **Вопрос {q['num']}**: "
                    f"Верно! ({q['correct']})"
                )

            else:

                details.append(
                    f"❌ **Вопрос {q['num']}**: "
                    f"Твой ответ '{user_ans}', "
                    f"а правильно — **{q['correct']}**"
                )


        # =================================================
        # СОХРАНЕНИЕ
        # =================================================

        now = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        cursor.execute(
            """
            INSERT INTO results
            (date, name, score)
            VALUES (?, ?, ?)
            """,
            (
                now,
                user_name,
                f"{score}/10"
            ),
        )

        conn.commit()


        # =================================================
        # РЕЗУЛЬТАТ
        # =================================================

        st.markdown(
            f"""
            <div class="result-box">

                <div style="font-size:25px;">
                    🎊 Результат для
                </div>

                <div style="
                    font-size:35px;
                    font-weight:800;
                ">
                    {user_name} 💕
                </div>

                <div class="result-score">
                    {score}/10
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # =================================================
        # ЭФФЕКТЫ ПО РЕЗУЛЬТАТУ
        # =================================================

        if score >= 8:

            fireworks_effect()
            hearts_effect()

            st.balloons()

            st.success(
                "🏆 ВАУ!!! Ты знаешь меня практически идеально!"
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:25px;
                    padding:20px;
                ">
                    👑 Легендарный уровень 👑
                    <br>
                    💕 Ты реально очень хорошо меня знаешь! 💕
                </div>
                """,
                unsafe_allow_html=True
            )


        elif score >= 5:

            hearts_effect()

            st.info(
                "💖 Хороший результат! "
                "Мы действительно неплохо общаемся."
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:22px;
                    padding:20px;
                ">
                    ✨ Ещё немного — и будет идеальный результат! ✨
                </div>
                """,
                unsafe_allow_html=True
            )


        else:

            sad_effect()

            st.error(
                "😜 Кажется, нам стоит получше узнать друг друга!"
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:22px;
                    padding:20px;
                ">
                    😭 Ты меня совсем не знаешь...
                    <br><br>
                    💔 Нам срочно нужно больше общаться!
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # РАЗБОР ОТВЕТОВ
        # =================================================

        st.divider()

        st.subheader("📊 Разбор ответов")

        for item in details:
            st.write(item)


# =========================================================
# ПАНЕЛЬ ВЛАДЕЛЬЦА
# =========================================================

st.divider()

with st.expander(
    "🔒 Вход для владельца (посмотреть результаты)"
):

    password = st.text_input(
        "Введи пароль для доступа:",
        type="password"
    )

    if password == "2011":

        st.subheader(
            "📋 Список всех результатов:"
        )

        df = pd.read_sql_query(
            """
            SELECT
                date AS 'Дата',
                name AS 'Имя',
                score AS 'Баллы'
            FROM results
            ORDER BY id DESC
            """,
            conn,
        )

        if not df.empty:

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "Пока никто не прошёл тест."
            )

    elif password:

        st.error(
            "❌ Неверный пароль!"
        )