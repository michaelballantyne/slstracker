from slstracker import app, model
from flask import render_template, request, url_for, redirect

@app.route('/')
@app.route('/semesters/')
def show_semesters():
    return render_template('semesters.html', semesters=model.listSemesters())

@app.route('/semesters/new/')
def new_semester_form():
    return render_template('new_semester.html')

@app.route('/semesters/', methods=['POST'])
def new_semester():
    model.addSemester(request.form['name'])
    return redirect(url_for('show_semesters'))

@app.route('/semesters/<id>', methods=['DELETE'])
def delete_semester(id):
    model.delete_semester(int(id));
    return redirect(url_for('show_semesters'))

@app.route('/semesters/<id>')
def show_semester(id):
    if request.args.get('_method', default=None) == 'DELETE':
        return delete_semester(id)
    else:
        return render_template('semester_students.html', 
                students = model.listStudentsForSemester(id),
                semester = model.getSemester(id))

@app.route('/students/<id>')
def show_student(id):
    return render_template('student_semesters.html', 
            student = model.getStudent(id), 
            semesters = model.listSemestersForStudent(id))

@app.route('/students/')
def show_students():
    return render_template('students.html', students=model.listStudents())

@app.route('/students/<student_id>/semesters/<semester_id>')
@app.route('/semesters/<semester_id>/students/<student_id>')
def show_hours(student_id, semester_id):
    return render_template('hours.html', 
            student = model.getStudent(student_id),
            semester = model.getSemester(semester_id),
            entries = model.listHourEntries(student_id, semester_id))

@app.route('/login')
def show_login():
    pass
