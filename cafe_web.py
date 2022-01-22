# Copied form day #62
# The app will run at port 8000

from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
import requests
import os
from dotenv import load_dotenv      # pip install python-dotenv

load_dotenv()

API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")

print(f'first: {API_URL}')

app_web = Flask(__name__)
app_web.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")       # read from .env file
Bootstrap(app_web)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Image (URL)', validators=[DataRequired(), URL()])
    location = StringField('Cafe Location', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    toilet = SelectField(u'Does it have toilet?', choices=['Yes', 'No'], validators=[DataRequired()])
    wifi = SelectField(u'Does it have wifi?', choices=['Yes', 'No'], validators=[DataRequired()])
    sockets = SelectField(u'Does it have power sockets?', choices=['Yes', 'No'], validators=[DataRequired()])
    take_calls = SelectField(u'Can you take calls?', choices=['Yes', 'No'], validators=[DataRequired()])
    coffee_price = StringField('Coffee price in GBP', validators=[DataRequired()])
    submit = SubmitField('Submit')
    # open = StringField('Opening Time e.g. 8.00 AM', validators=[DataRequired()])
    # close = StringField('Closing Time e.g. 5.30 PM', validators=[DataRequired()])
    # coffee_rating = SelectField(u'Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    # wifi_rating = SelectField(u'Wifi Strength Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    # power_rating = SelectField(u'Power Socket Availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])


@app_web.route("/")
def home():
    return render_template("index.html")


@app_web.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_endpoint = f"{API_URL}/add"
        cafe_parameters = {
                "name": form.name.data,
                "map_url": form.map_url.data,
                "img_url": form.img_url.data,
                "location": form.location.data,
                "seats": form.seats.data,
                "has_toilet": 1 if form.toilet.data == 'Yes' else 0,
                "has_wifi": 1 if form.wifi.data == 'Yes' else 0,
                "has_sockets": 1 if form.sockets.data == 'Yes' else 0,
                "can_take_calls": 1 if form.take_calls.data == 'Yes' else 0,
                "coffee_price": form.coffee_price.data,
            }
        cafe_headers = {
        #         "x-app-id": APP_ID,
        #         "x-app-key": API_KEY,
                "Content-Type": "application/json",
            }
        print(API_URL)
        response = requests.post(url=cafe_endpoint, json=cafe_parameters, headers=cafe_headers)
        response.raise_for_status()
        print(f'add: {response.json()}')
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app_web.route('/cafes')
def cafes():
    response = requests.get(url=f"{API_URL}/all")
    all_cafes = response.json()['cafes']
    all_cafes_list = [list(all_cafes[i].values()) for i in range(0, len(all_cafes))]
    heading = list(all_cafes[0].keys())
    all_cafes_list.insert(0, heading)
    return render_template('cafes.html', cafes=all_cafes_list, length=len(all_cafes_list))

@app_web.route('/delete/<int:cafe_id>', methods=['GET', 'POST'])
def delete_cafe(cafe_id):
    # http://127.0.0.1:5000/report-closed/25?api-key=TopSecretAPIKey

    response = requests.delete(f"{API_URL}/report-closed/{cafe_id}?api-key={API_KEY}")
    print(f"delete: {response.json()}")
    return redirect(url_for('cafes'))

if __name__ == '__main__':
    app_web.run(debug=True, host="127.0.0.1", port=8000)

