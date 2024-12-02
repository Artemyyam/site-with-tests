from flask import Flask, render_template, Response, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/main")
def main():
    return render_template("main.html")



@app.route('/<string:profession>')
def skills(profession):
    return render_template("skills.html")


@app.route('/<string:profession>/<string:skills>')
def test(profession, skills):
    return render_template("test.html") 


@app.route("/<string:profession>/<string:skills>/forward/", methods=['POST'])
def test_forward():

    

    forward_message = "Moving forward... "
    return render_template("test.html", forward_message=forward_message)


@app.route('/<string:profession>/<string:skills>/answer')
def answer(profession, skills):
    return render_template("answer.html")


if __name__ == "__main__":
    app.run(debug = True)
