from typing import List

from flask import Flask
from flask_cors import CORS, cross_origin
from nredarwin.webservice import DarwinLdbSession

from traintimes.models import DepartureJson
from traintimes.timetable import combine_timetables, get_timetable

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

darwin_client = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx")


@app.route('/timetable/ecr2clj-lbg', methods=['GET'])
@cross_origin()
def get_ecr_2_clj_lbg_timetable() -> List[DepartureJson]:
    lbg_timetable = get_timetable(darwin_client, "LBG")
    clj_timetable = get_timetable(darwin_client, "CLJ")
    return combine_timetables(lbg_timetable, clj_timetable)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
