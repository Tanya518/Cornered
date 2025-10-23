# 🌐 Інструкція: Як запустити гру в браузері через Pygbag

Pygbag конвертує Pygame гри в WebAssembly, щоб вони працювали прямо в браузері!

## 📋 Крок 1: Встановити Pygbag

Відкрий термінал і встанови pygbag:

```bash
pip install pygbag
```

## 🎮 Крок 2: Зібрати гру

У папці `game_py` виконай команду:

```bash
pygbag main.py
```

Або з повним шляхом:

```bash
cd "C:\Users\tanya\OneDrive\Documents\Game_python\game_py"
pygbag main.py
```

## 🚀 Крок 3: Запустити локально

Після збірки pygbag автоматично запустить локальний сервер. Відкрий браузер і перейди на:

```
http://localhost:8000
```

Гра має запуститись у браузері! 🎉

## 📤 Крок 4: Завантажити на GitHub Pages

### 4.1 Створити репозиторій на GitHub
1. Іди на [github.com](https://github.com)
2. Натисни **New Repository**
3. Назви репозиторій, наприклад: `pygame-game`
4. Зроби його **Public**
5. Створи репозиторій

### 4.2 Завантажити файли
У папці `game_py` виконай:

```bash
git init
git add main.py index.html README.md
git commit -m "Initial commit - Pygame Web Game"
git branch -M main
git remote add origin https://github.com/твій-username/pygame-game.git
git push -u origin main
```

### 4.3 Увімкнути GitHub Pages
1. У репозиторії іди в **Settings**
2. Прокрути до **Pages**
3. У **Source** вибери **main branch**
4. Натисни **Save**

Через кілька хвилин гра буде доступна за адресою:
```
https://твій-username.github.io/pygame-game/
```

## 🎯 Альтернатива - itch.io

Можна завантажити на [itch.io](https://itch.io):

1. Створи акаунт на itch.io
2. Натисни **Upload New Project**
3. Завантаж згенеровані файли з папки `build/web/`
4. Встанови "This file will be played in the browser"
5. Опублікуй!

## ⚠️ Важливо для Pygbag

У коді **main.py** важливі ці зміни:

1. **Async функція**: весь головний цикл обгорнутий в `async def main()`
2. **await asyncio.sleep(0)**: критично важливий рядок у циклі для роботи в браузері
3. **asyncio.run(main())**: запуск async функції

```python
async def main():
    while playing:
        # game loop
        pygame.display.flip()
        await asyncio.sleep(0)  # ⬅️ Обов'язково!

asyncio.run(main())
```

## 📁 Структура файлів

Після збірки маєш бути такі файли:
```
game_py/
├── main.py          # Головний файл гри (з asyncio)
├── index.html       # HTML сторінка для браузера
├── README.md        # Опис проєкту
└── build/           # Згенерована pygbag папка
    └── web/         # Веб-файли для хостингу
```

## 🐛 Проблеми та рішення

**Pygbag не встановлюється:**
```bash
python -m pip install --upgrade pip
pip install pygbag
```

**Гра не запускається в браузері:**
- Перевір що є `await asyncio.sleep(0)` у головному циклі
- Перевір консоль браузера (F12) на помилки

**GitHub Pages не працює:**
- Зачекай 5-10 хвилин після увімкнення Pages
- Перевір що репозиторій Public

## 🎊 Готово!

Тепер твоя гра працює в браузері і люди можуть грати без скачування Python або Pygame!

Поділись посиланням з друзями! 🚀
