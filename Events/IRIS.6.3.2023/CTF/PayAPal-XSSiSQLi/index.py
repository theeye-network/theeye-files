from flask import *

# Create a Flask app instance
app = Flask(__name__)

tables = {
    "SHOW DATABASES" : """LOGS
LAGS
LEAKS""",
    "SELECT * FROM LOGS" : """<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky">IP</th>
    <th class="tg-0pky">Split Total</th>
    <th class="tg-0lax">Split By</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">1.2.3.4</td>
    <td class="tg-0lax">500000</td>
    <td class="tg-0lax">300</td>
  </tr>
  <tr>
    <td class="tg-0lax">2.3.4.5</td>
    <td class="tg-0lax">6032</td>
    <td class="tg-0lax">21</td>
  </tr>
  <tr>
    <td class="tg-0lax">3.4.5.6</td>
    <td class="tg-0lax">453123</td>
    <td class="tg-0lax">3</td>
  </tr>
  <tr>
    <td class="tg-0lax">4.5.6.7</td>
    <td class="tg-0lax">543523</td>
    <td class="tg-0lax">32</td>
  </tr>
  <tr>
    <td class="tg-0lax">5.6.7.8</td>
    <td class="tg-0lax">456354</td>
    <td class="tg-0lax">12</td>
  </tr>
  <tr>
    <td class="tg-0lax">6.7.8.9</td>
    <td class="tg-0lax">434</td>
    <td class="tg-0lax">2</td>
  </tr>
  <tr>
    <td class="tg-0lax">9.0.1.2</td>
    <td class="tg-0lax">21324</td>
    <td class="tg-0lax">43</td>
  </tr>
  <tr>
    <td class="tg-0lax">0.1.2.3</td>
    <td class="tg-0lax">35432</td>
    <td class="tg-0lax">21</td>
  </tr>
  <tr>
    <td class="tg-0lax">2.1.3.4</td>
    <td class="tg-0lax">54325</td>
    <td class="tg-0lax">21</td>
  </tr>
</tbody>
</table>""",
    "SELECT * FROM LAGS": '''<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky">IP</th>
    <th class="tg-0pky">Split Total</th>
    <th class="tg-0lax">Split By</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">1.2.3.4</td>
    <td class="tg-0lax">500000</td>
    <td class="tg-0lax">300</td>
  </tr>
  <tr>
    <td class="tg-0lax">2.3.4.5</td>
    <td class="tg-0lax">6032</td>
    <td class="tg-0lax">21</td>
  </tr>
  <tr>
    <td class="tg-0lax">3.4.5.6</td>
    <td class="tg-0lax">453123</td>
    <td class="tg-0lax">3</td>
  </tr>
  <tr>
    <td class="tg-0lax">4.5.6.7</td>
    <td class="tg-0lax">543523</td>
    <td class="tg-0lax">32</td>
  </tr>
  <tr>
    <td class="tg-0lax">5.6.7.8</td>
    <td class="tg-0lax">456354</td>
    <td class="tg-0lax">12</td>
  </tr>
  <tr>
    <td class="tg-0lax">6.7.8.9</td>
    <td class="tg-0lax">434</td>
    <td class="tg-0lax">2</td>
  </tr>
  <tr>
    <td class="tg-0lax">9.0.1.2</td>
    <td class="tg-0lax">21324</td>
    <td class="tg-0lax">43</td>
  </tr>
  <tr>
    <td class="tg-0lax">0.1.2.3</td>
    <td class="tg-0lax">35432</td>
    <td class="tg-0lax">21</td>
  </tr>
  <tr>
    <td class="tg-0lax">2.1.3.4</td>
    <td class="tg-0lax">54325</td>
    <td class="tg-0lax">21</td>
  </tr>
</tbody>
</table>''',
    "SELECT * FROM LEAKS" : '''<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky">IP</th>
    <th class="tg-0pky">Split Total</th>
    <th class="tg-0lax">Split By</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">1.2.3.4</td>
    <td class="tg-0lax">500000</td>
    <td class="tg-0lax">300</td>
  </tr>
  <tr>
    <td class="tg-0lax">2.3.4.5</td>
    <td class="tg-0lax">6032</td>
    <td class="tg-0lax">21</td>
  </tr>
  <tr>
    <td class="tg-0lax">3.4.5.6</td>
    <td class="tg-0lax">453123</td>
    <td class="tg-0lax">3</td>
  </tr>
  <tr>
    <td class="tg-0lax">4.5.6.7</td>
    <td class="tg-0lax">543523</td>
    <td class="tg-0lax">32</td>
  </tr>
  <tr>
    <td class="tg-0lax">5.6.7.8</td>
    <td class="tg-0lax">456354</td>
    <td class="tg-0lax">12</td>
  </tr>
  <tr>
    <td class="tg-0lax">6.7.8.9</td>
    <td class="tg-0lax">434</td>
    <td class="tg-0lax">2</td>
  </tr>
  <tr>
    <td class="tg-0lax">9.0.1.2</td>
    <td class="tg-0lax">21324</td>
    <td class="tg-0lax">43</td>
  </tr>
  <tr>
    <td class="tg-0lax">0.1.2.3</td>
    <td class="tg-0lax">35432</td>
    <td class="tg-0lax">21</td>
  </tr>
  <tr>
    <td class="tg-0lax">2.1.3.4</td>
    <td class="tg-0lax">54325</td>
    <td class="tg-0lax">21</td>
  </tr>
</tbody>
</table>'''
}

# Define the landing page route
@app.route('/')
def landing_page():
    return render_template("index.html")

# Define the 'calc' route
@app.route('/calc')
def split():
    if (not (request.args.get("amt").isdigit())):
        if (r"SELECT" in request.args.get("amt").upper()) or (r"DESC" in request.args.get("amt").upper()):
            table = tables.get(request.args.get("amt").upper())
            if table == None:
                table = "YESQL. BUT, ASK THE RIGHT QUESTIONS. <p> ~ The Eye ;)</p>"
            return render_template("sqlinj.html", query=request.args.get("amt").upper(), table = table)
    if (not (request.args.get("ppl").isdigit())):
        if r"<script" in request.args.get("ppl").lower():
            if "alert" in request.args.get("ppl").lower():
                return render_template("xssinj.html", query="<script>alert('you\\\'re smart! find the flag from this string \"42d388f8b1db997faaf7dab487f11290 \"');" + str(request.args.get("ppl").lower().replace("<script>","").replace(" ","")))
            else:
                return render_template("xssinj.html", query=request.args.get("ppl").lower())
    splitbill = int(request.args.get("amt"))/int(request.args.get("ppl"))
    return render_template('calculator.html', split=splitbill)

# Run the app if this module is run as the main program
if __name__ == '__main__':
    app.run(debug=True)
