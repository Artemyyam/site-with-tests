from flask import Flask, render_template, Response, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from FDataBase import FDataBase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Test Data Base.db'
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


@app.route("/")
@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/software_tester", methods=['POST', 'GET']) #/<string:profession>
def skills():
    if request.method == "POST":
        profession = request.form.get('profession')
        skills = request.form.get('skills')
        description = request.form.get('description')
        test = request.form.get('test')
        completed = request.form.get('completed')
        test_r = request.form.get('test_r')

        article = Article(profession=profession, skills=skills, description=description, test=test, completed=completed, test_r=test_r)

        try:
            #db.session.add(article)
            #db.session.commit()
            
            return render_template()
        except:
            return "При выполнении теста произошла ошибка"
    else:
        db = get_db()
        dbase = FDataBase(db)
        return render_template("skills.html", menu = dbase.getMenu())


@app.route("/software_tester/knowledg_of_OS", methods=['POST', 'GET']) #/<string:profession>/<string:skills>
def test_forward():
    if request.method == "POST":
        profession = request.form.get('profession')
        skills = request.form.get('skills')
        description = request.form.get('description')
        test = request.form.get('test')
        completed = request.form.get('completed')
        test_r = request.form.get('test_r')

        article = Article(profession=profession, skills=skills, description=description, test=test, completed=completed, test_r=test_r)

        try:
            #db.session.add(article)
            #db.session.commit()
            
            return render_template("test.html")
        except:
            return "При выполнении теста произошла ошибка"
    else:
        return render_template("answer.html")


@app.route("/software_tester/knowledg_of_OS/answer", methods=['POST', 'GET']) #/<string:profession>/<string:skills>
def answer():
    if request.method == "POST":
        profession = request.form['profession']
        skills = request.form['skills']
        description = request.form['description']
        test = request.form['test']
        completed = request.form['completed']
        test_r = request.form['test_r']

        article = Article(profession=profession, skills=skills, description=description, test=test, completd=completed, test_r=test_r)

        try:
            db.session.add(article)
            db.session.commit()
            return render_template("test.html")
        except:
            return "При выполнении теста произошла ошибка"
    else:
        return render_template("answer.html")


if __name__ == "__main__":
    app.run(debug = True)
