from flask import Flask, render_template, request, send_file
import io
import json
from openpyxl import Workbook

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    timetable = None
    classrooms = 0
    days_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    periods = 0

    if request.method == 'POST':
        days = request.form.getlist('days')
        periods = int(request.form.get('replace'))
        subjects = request.form.get('subjects').strip().split(',')
        classrooms = int(request.form.get('classrooms'))

        timetable = {f'Classroom {cr}': {} for cr in range(1, classrooms + 1)}
        sub_index = 0
        for cr in timetable:
            for day in days:
                timetable[cr][day] = []
                for p in range(periods):
                    timetable[cr][day].append(subjects[sub_index % len(subjects)].strip())
                    sub_index += 1

    return render_template('index.html', timetable=timetable, days_options=days_options,
                           classrooms=classrooms, periods=periods)

@app.route('/download/xlsx', methods=['POST'])
def download_xlsx():
    data = request.form.get('timetable_data')
    timetable = json.loads(data)

    wb = Workbook()
    wb.remove(wb.active)  # remove default sheet

    for classroom, schedule in timetable.items():
        ws = wb.create_sheet(title=classroom)
        # Header row: Periods
        header = ['Day'] + [f'Period {i+1}' for i in range(len(next(iter(schedule.values()))))]
        ws.append(header)

        for day, periods in schedule.items():
            ws.append([day] + periods)

    bio = io.BytesIO()
    wb.save(bio)
    bio.seek(0)

    return send_file(
        bio,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='timetable.xlsx'
    )

if __name__ == '__main__':
    app.run(debug=True)
