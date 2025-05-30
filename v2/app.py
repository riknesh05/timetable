from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    timetable = None
    classrooms = 0
    if request.method == 'POST':
        days = request.form.getlist('days')
        slots = int(request.form.get('slots'))
        subjects = request.form.get('subjects').strip().split(',')
        classrooms = int(request.form.get('classrooms'))

        # Generate timetable: dictionary with day -> classroom -> list of subjects
        timetable = {}
        sub_index = 0
        for day in days:
            timetable[day] = {}
            for cr in range(1, classrooms + 1):
                timetable[day][f'Classroom {cr}'] = []
                for slot in range(slots):
                    timetable[day][f'Classroom {cr}'].append(subjects[sub_index % len(subjects)].strip())
                    sub_index += 1

    days_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return render_template('index.html', timetable=timetable, days_options=days_options, classrooms=classrooms)

if __name__ == '__main__':
    app.run(debug=True)
