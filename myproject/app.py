from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    test = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Text, default=0)
    test_r = db.Column(db.Text, default=0)

    def __repr__(self):
        return '<Article %r>' % self.id

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)

    def __repr__(self):
        return '<Question %r>' % self.id

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

        a = 0
        if None != profession: a = 1

        article = Article(profession=profession, skills=skills, description=description, test=test, completed=completed, test_r=test_r)

        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        value = request.form.get('value')

        questions = Question(q1=q1, q2=q2, q3=q3, q4=q4, value=value)

        try:
            if a == 1:
                db.session.add(article)
            elif a == 0:
                db.session.add(questions)
            db.session.commit()
            return render_template("main.html")
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

        article = Article(profession=profession, skills=skills, description=description, test=test, completed=completed, test_r=test_r)

        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')

        question = Question(q1=q1, q2=q2, q3=q3, q4=q4)
        try:
            if article != 0: db.session.add(article)
            else: db.session.add(question)
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
    articles = Article.query.all()
    return render_template("skills.html", articles=articles)

@app.route("/software_tester/knowledge_of_OS", methods=['POST', 'GET'])
def test_forward():
    articles = Article.query.all()
    return render_template("test.html", articles=articles)

@app.route("/software_tester/knowledge_of_OS/answer", methods=['POST', 'GET'])
def answer():
    if request.method == "POST":
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')

        question = Question(q1=q1, q2=q2, q3=q3, q4=q4)

        try:
            db.session.add(question)
            print(question)
            db.session.commit()
            print(q1, q2, q3, q4)
            return redirect("/software_tester/knowledge_of_OS/answer") #"/software_tester/knowledge_of_OS/answer"
        except:
            return "При выполнении теста произошла ошибка"
    else:
        questions = Question.query.all()
        return render_template("answer.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
