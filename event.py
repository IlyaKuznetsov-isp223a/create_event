from flask import Flask, render_template_string, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

events = []

class Event:
    def __init__(self, title, description, date, time, location):
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.location = location
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"Event(title='{self.title}', date='{self.date}', time='{self.time}')"


@app.route("/")
def index():
    sorted_events = sorted(events, key=lambda event: datetime.strptime(f"{event.date} {event.time}", "%Y-%m-%d %H:%M"), reverse=True)

    template = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Список мероприятий</title>
    </head>
    <body>
        <h1>Список мероприятий</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <a href="{{ url_for('create_event') }}">Создать мероприятие</a>

        {% if events %}
            <ul>
                {% for event in events %}
                    <li>
                        <strong>{{ event.title }}</strong> - {{ event.date }} {{ event.time }} - {{ event.location }}
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p>Нет запланированных мероприятий.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(template, events=sorted_events)


@app.route("/create", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]
        time = request.form["time"]
        location = request.form["location"]

        if not title or not date or not time:
            flash("Пожалуйста, заполните все обязательные поля (Название, Дата, Время)", "error")
            return redirect(url_for("create_event"))

        try:
            datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash("Неверный формат даты или времени. Используйте формат ГГГГ-ММ-ДД и ЧЧ:ММ", "error")
            return redirect(url_for("create_event"))

        new_event = Event(title, description, date, time, location)
        events.append(new_event)
        flash(f"Мероприятие '{title}' успешно создано!", "success")
        return redirect(url_for("index"))

    template = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Создать мероприятие</title>
    </head>
    <body>
        <h1>Создать мероприятие</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="post">
            <label for="title">Название:</label><br>
            <input type="text" id="title" name="title" required><br><br>

            <label for="description">Описание:</label><br>
            <textarea id="description" name="description"></textarea><br><br>

            <label for="date">Дата (ГГГГ-ММ-ДД):</label><br>
            <input type="date" id="date" name="date" required><br><br>

            <label for="time">Время (ЧЧ:ММ):</label><br>
            <input type="time" id="time" name="time" required><br><br>

            <label for="location">Местоположение:</label><br>
            <input type="text" id="location" name="location"><br><br>

            <input type="submit" value="Создать">
        </form>

        <a href="{{ url_for('index') }}">Назад к списку мероприятий</a>
    </body>
    </html>
    """
    return render_template_string(template)


if __name__ == "__main__":
    app.run(debug=True)
