from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    test = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Integer, default=0)
    test_r = db.Column(db.Text, default=0)

    def __repr__(self):
        return '<Main %r>' % self.id

class Association(db.Model):
    text_id = db.Column(db.Integer, primary_key=True)
    main_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Association %r>' % self.id

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Test %r>' % self.id

with app.app_context():
    db.create_all()


@app.route("/")
@app.route("/main", methods=['POST', 'GET'])
def main():
    if request.method == "POST":
        profession = request.form.get('profession')
        skills = request.form.get('skills')
        description = request.form.get('description')
        test = request.form.get('test')
        completed = request.form.get('completed')
        test_r = request.form.get('test_r')

        main = Main(profession=profession, skills=skills, description=description, test=test, completed=completed, test_r=test_r)

        try:
            db.session.add(main)
            db.session.commit()
            return redirect("/") #render_template("main.html")
        except:
            return "При выполнении теста произошла ошибка"
    else:
        return render_template("main.html")

@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        profession = request.form.get('profession')
        skills = request.form.get('skills')
        description = request.form.get('description')
        test = request.form.get('test')
        completed = request.form.get('completed')
        test_r = request.form.get('test_r')

        main = Main(profession=profession, skills=skills, description=description, test=test, completed=completed, test_r=test_r)
        try:
            db.session.add(main)
            db.session.commit()
            return redirect('/')
        except:
            return "При выполнении теста произошла ошибка"
    else:
        return render_template("create.html")

@app.route('/software_tester/description')
def description():
    return render_template("skill-description.html")

@app.route("/software_tester", methods=['POST', 'GET'])
def skills():
    text = Main.query.all()
    return render_template("skills.html", text=text)

@app.route("/software_tester/knowledge_of_OS", methods=['POST', 'GET'])
def test_forward():
    text = Main.query.all()
    return render_template("test.html", text=text)

@app.route("/software_tester/knowledge_of_OS/answer", methods=['POST', 'GET'])
def answer():
    if request.method == "POST":
        test_r = request.form.get('test_r')

        main = Main(test_r=test_r)

        try:
            db.session.add(main)
            db.session.commit()
            return redirect("/software_tester/knowledge_of_OS/answer") #"/software_tester/knowledge_of_OS/answer"
        except:
            return "При выполнении теста произошла ошибка"
    else:
        questions = Main.query.all()
        return render_template("answer.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
