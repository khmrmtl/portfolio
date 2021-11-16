from flask import Flask, render_template, send_file, flash
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
import email_validator
import os
import smtplib


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

PASSWORD = os.environ.get("PASSWORD")
EMAIL = os.environ.get("EMAIL")


class contactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(
      label='Your Email', validators=[DataRequired(), Email(granular_message=True)])
    message = StringField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label="Send")


@app.route("/", methods=["GET", "POST"])
def home():
    cform = contactForm()
    if cform.validate_on_submit():
        print("gumana boi")
        try:
            # send me an email
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, "motalkhmer@gmail.com",
                                f"Subject: Portfolio message\n\nName: {cform.name.data}\n"
                                f"E-mail :{cform.email.data}\nMessage: {cform.message.data}"
                                )
            # also send an email to the one who left a message
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.sendmail(EMAIL, f"{cform.email.data}",
                                f"Subject: Khmer's Portfolio\n\nFrom: Khmer Motal\n"
                                f"I am glad that you contacted me, I will get back to you as soon as I can"
                                )
            flash("Your message has been delivered")
        except Exception as e:
            flash("I'm sorry, but there seems to be a problem sending your message. Try using a gmail account", e)

    return render_template("index.html", form=cform)


@app.route('/download-app')
def download_app():
    return send_file('static/food_nutrition.apk',
                     mimetype='application/vnd.android.package-archive',
                     attachment_filename='food-nutrition.apk',
                     as_attachment=True)


@app.route('/download-resume')
def download_resume():
    return send_file('static/resume.pdf',
                     mimetype='application/pdf',
                     attachment_filename='Khmer Motal.pdf',
                     as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
