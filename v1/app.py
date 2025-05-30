from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    timetable = None
    if request.method == 'POST':
        # Get form data
        days = request.form.getlist('days')
        slots = int(request.form.get('slots'))
        subjects = request.form.get('subjects').strip().split(',')

        # Simple timetable generation logic: assign subjects in round robin fashion
        timetable = {}
        sub_index = 0
        for day in days:
            timetable[day] = []
            for slot in range(slots):
                timetable[day].append(subjects[sub_index % len(subjects)].strip())
                sub_index += 1

    # Days options for form
    days_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return render_template('index.html', timetable=timetable, days_options=days_options)

if __name__ == '__main__':
    app.run(debug=True)
