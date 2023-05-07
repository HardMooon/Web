from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web.db'
db = SQLAlchemy(app)


class Univer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(300), nullable=False)
    SecondName = db.Column(db.String(300), nullable=False)
    SurName = db.Column(db.String(300), nullable=False)
    Group = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Univer %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/students')
def students():
    Students = Univer.query.order_by(Univer.date.desc()).all()
    return render_template("students.html", Students=Students)


@app.route('/students/<int:id>')
def students_detail(id):
    Student = Univer.query.get(id)
    return render_template("student_detail.html", Student=Student)


@app.route('/students/<int:id>/del')
def student_delete(id):
    Student = Univer.query.get_or_404(id)

    try:
        db.session.delete(Student)
        db.session.commit()
        return redirect('/students')
    except:
        return "При удалении статьи произошла ошибка"



@app.route('/students/<int:id>/update', methods=['POST','GET'])
def student_update(id):
    Student = Univer.query.get(id)
    if request.method == "POST":
        Student.SecondName = request.form['SecondName']
        Student.FirstName = request.form['FirstName']
        Student.SurName = request.form['SurName']
        Student.Group = request.form['Group']

        try:
            db.session.commit()
            return redirect('/students')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("student_update.html",Student=Student)


@app.route('/create-student', methods=['POST','GET'])
def create_student():
    if request.method == "POST":
        SecondName = request.form['SecondName']
        FirstName = request.form['FirstName']
        SurName = request.form['SurName']
        Group = request.form['Group']

        Student = Univer(SecondName=SecondName, FirstName=FirstName, SurName=SurName, Group=Group)

        try:
            db.session.add(Student)
            db.session.commit()
            return redirect('/students')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-student.html")


if __name__ == "__main__":
    app.run(debug=True)