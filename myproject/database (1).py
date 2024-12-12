from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Промежуточная таблица для связи многие ко многим
association_table = db.Table('association',
    db.Column('texttest_id', db.Integer, db.ForeignKey('t_e_x_ttest.id'), primary_key=True),
    db.Column('mtest_id', db.Integer, db.ForeignKey('m_test.id'), primary_key=True)
)

# Модель для TEXTtest
class TEXTtest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    test = db.Column(db.Text, nullable=False)
    complete_test = db.Column(db.Text, default='Not Complete')
    test_result = db.Column(db.Text, default='Not Complete')

    # Связь многие ко многим
    m_tests = db.relationship('MTest', secondary=association_table, back_populates='texttests')

# Модель для MTest
class MTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    # Связь многие ко многим
    texttests = db.relationship('TEXTtest', secondary=association_table, back_populates='m_tests')

# Команда для создания базы данных и таблиц
with app.app_context():
    db.create_all()

# Функция для добавления вопроса и ответа в MTest
def add_cqa(category, question, answer):
    mtest_entry = MTest(category=category, question=question, answer=answer)
    db.session.add(mtest_entry)
    db.session.commit()

# Функция для добавления информации в TEXTtest
def add_information(profession, skills, description, test):
    texttest_entry = TEXTtest(profession=profession, skills=skills, description=description, test=test)
    db.session.add(texttest_entry)
    db.session.commit()

# Функция для обновления статуса теста в TEXTtest
def update_test_complete(test_id, status):
    texttest_entry = TEXTtest.query.get(test_id)
    if texttest_entry:
        texttest_entry.complete_test = status
        db.session.commit()

# Функция для обновления результата текстового теста в TEXTtest
def update_text_result(test_id, status):
    texttest_entry = TEXTtest.query.get(test_id)
    if texttest_entry:
        texttest_entry.test_result = status
        db.session.commit()

# Функция для листинга всех TEXTtest
def list_text():
    texttests = TEXTtest.query.all()
    for test in texttests:
        print(test)

if __name__ == '__main__':
    app.run(debug=True)
