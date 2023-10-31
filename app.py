from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import DateField, SubmitField
from wtforms import validators
from main import playlistMaker, fetchTop100

LINK_URL = "https://open.spotify.com/playlist/"

app = Flask(__name__)

app.config["SECRET_KEY"] = "admin"


class DateForm(FlaskForm):
    date = DateField("Date", format="%Y-%m-%d", validators=(validators.DataRequired(),))
    submit = SubmitField("Submit")


class SubmitForm(FlaskForm):
    submit = SubmitField("Create!")


@app.route("/", methods=["GET", "POST"])
def home():
    form = DateForm()
    if form.validate_on_submit():
        date = form.date.data
        print(date)
        return redirect(url_for("fetchDate", date=date))
    return render_template("index.html", form=form)


@app.route("/fetchDate/<date>", methods=["POST", "GET"])
def fetchDate(date):
    print("Second Half " + date)

    top_titles, artists = fetchTop100(date)

    result = dict(zip(top_titles, artists))

    form = SubmitForm()
    
    if form.validate_on_submit():
        playlistID = playlistMaker(date, top_titles)
        
        print(playlistID)
        return redirect(url_for("playlistCreated", id=playlistID))

    return render_template("date.html", result=result, date=date, form=form)


@app.route("/playlist/<id>", methods=["POST", "GET"])
def playlistCreated(id):
    return render_template("created.html", link = LINK_URL + id)

if __name__ == "__main__":
    app.run(debug=True)
