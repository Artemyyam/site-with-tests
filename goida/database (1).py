from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maindatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Промежуточная таблица для связи многие ко многим
association_table = db.Table('association',
    db.Column('main_id', db.Integer, db.ForeignKey('main.id'), primary_key=True),
    db.Column('text_id', db.Integer, db.ForeignKey('text.id'), primary_key=True)
)

# Модель для main
class main(db.Model):
    __tablename__ = 'main'

    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    test = db.Column(db.Text, nullable=False)
    complete_test = db.Column(db.Text, default='Not Complete')
    test_result = db.Column(db.Text, default='Not Complete')

    # Связь многие ко многим
    texts = db.relationship('text', secondary=association_table, back_populates='mains')

# Модель для text
class text(db.Model):
    __tablename__ = 'text'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    # Связь многие ко многим
    mains = db.relationship('main', secondary=association_table, back_populates='texts')

# Команда для создания базы данных и таблиц
with app.app_context():
    db.create_all()

# Функция для добавления вопроса и ответа в text
def add_cqa(category, question, answer):
    text_entry = text(category=category, question=question, answer=answer)
    db.session.add(text_entry)
    db.session.commit()

# Функция для добавления информации в main
def add_information(profession, skills, description, test):
    main_entry = main(profession=profession, skills=skills, description=description, test=test)
    db.session.add(main_entry)
    db.session.commit()

# Функция для обновления статуса теста в main
def update_test_complete(test_id, status):
    main_entry = main.query.get(test_id)
    if main_entry:
        main_entry.complete_test = status
        db.session.commit()

# Функция для обновления результата текстового теста в main
def update_text_result(test_id, status):
    main_entry = main.query.get(test_id)
    if main_entry:
        main_entry.test_result = status
        db.session.commit()

# Функция для листинга всех main
def list_text():
    mains = main.query.all()
    for test in mains:
        print(test)

if __name__ == '__main__':
    app.run(debug=True)