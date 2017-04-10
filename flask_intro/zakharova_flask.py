from flask import Flask
from flask import render_template, request

app = Flask(__name__)

love = {}
answers = {}


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/result')
def result():
    global love
    global answers
    if request.args:
        name = request.args['name']
        choice = request.args['choice']
        if choice not in love:
            love[choice] = 1
        else:
            love[choice] += 1
        if name not in answers:
            answers[name] = {'count': 1, 'loves': choice}
        else:
            answers[name]['count'] += 1
            answers[name]['loves'] = choice
    return render_template('result.html', love=love, answers=answers)

if __name__ == '__main__':
    app.run(debug=True)
