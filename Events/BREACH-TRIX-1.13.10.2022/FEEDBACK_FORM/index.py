from flask import *
import uuid, json, io
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = "KrrrzPPghtfgSKbtJEQCTA"

app.PROPAGATE_EXCEPTIONS = True

def reg():
    with open("attendees.json") as file:
        data = json.load(file)
    return data

@app.route('/', methods=['GET', 'POST'])
def feedback():
    rolls = []
    feedbacks = []
    c=0
    for i in sorted(reg(), key=lambda d: d['roll_no']):
        c+=1
        if i["roll_no"].upper() not in rolls:
            rolls.append(i["roll_no"].upper())
            if i.get("feedback"):
                feedbacks.append(i["roll_no"].upper())
    if request.args.get("roll") in rolls:
        if request.method=='GET':
            if request.args.get("roll").upper() in feedbacks:
                feedbacked="true"
            else:
                feedbacked="false"
            return render_template("feedback.html", roll=request.args.get("roll"), feedbacked=feedbacked)
        if request.method=='POST':
            roll = request.form.get("roll")
            feedback = request.form.get("gen-feedback")
            interActiValues = {
                "1": "Not At All Interactive",
                "2": "Decent",
                "3": "Very Interactive",
            }

            effeValues = {
                "1": "Couldn't Understand Hands-On",
                "2": "Hands-On was a good teaching aid",
                "3": "Learnt A Lot through Hands-On",
            }

            frenValues = {
                "1": "The Presenters were Hostile",
                "2": "The Presenters were friendly, couldn't answer my doubts",
                "3": "The Presenters were very friendly and approachable",
            }

            learnValues = {
                "1": "Topics were useless",
                "2": "Topics were well planned, but I don't see the scope",
                "3": "Well Planned and topics and the workshop was very useful!",
            }

            speedValues = {
                "1": "Presenters presented too slow, boring.",
                "2": "Presenters presented too fast, couldn't catch up.",
                "3": "Presenters presented at perfect speed.",
            }
            feedback = f'''{feedback}. {interActiValues.get(request.form.get('inteRangeInput'))}.
{effeValues.get(request.form.get('effeRangeInput'))}. {learnValues.get(request.form.get('learnRangeInput'))}.
{frenValues.get(request.form.get('frenRangeInput'))}. {speedValues.get(request.form.get('speedRangeInput'))}'''.replace("\n"," ")
            feedbacks = []
            for i in reg():
                if i["roll_no"].upper()!=roll.upper():
                    feedbacks.append(i)
                else:
                    print(i)
                    i["feedback"] = feedback
                    feedbacks.append(i)
            with open("attendees.json", "w") as file:
                json.dump(feedbacks,file, indent=4)
            return redirect(f"{url_for('feedback')}?roll={roll}")
    else:
        return render_template("index.html")

@app.route('/view-feedback', methods=['POST', 'GET'])
def view_feedback():
    rolls = []
    tableau = [["#", "Name", "Roll Number", "Email", "Phone Number", "Feedback"]]
    attendees = []
    c=0
    for i in sorted(reg(), key=lambda d: d['roll_no']):
        c+=1
        if i["roll_no"].upper() not in rolls:
            rolls.append(i["roll_no"].upper())
            tableau.append([str(c),i["name"],i["roll_no"].upper(),f'{i["roll_no"].upper()}@psgtech.ac.in',i['phone_no'],i['feedback']])
    for i in tableau:
        attendees.append({"#":i[0],
                          "name":i[1],
                          "roll":i[2],
                          "email":i[3],
                          "phone":i[4],
                          "feedback":i[5]})

def main():
  app.run(debug=True,
          host='0.0.0.0',
          port=56789)

if __name__ == '__main__':
  main()