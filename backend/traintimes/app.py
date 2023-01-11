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


@app.route('/timetable/<source>2<destination>', methods=['GET'])
@cross_origin()
def get_ecr_2_clj_lbg_timetable(source: str, destination: str) -> List[DepartureJson]:
    destinations = destination.split(",")
    if len(destinations) > 2:
        raise RuntimeError("Only 2 destinations are currently supported")
    elif len(destinations) == 2:
        timetable_1 = get_timetable(darwin_client, source, destinations[0])
        timetable_2 = get_timetable(darwin_client, source, destinations[1])
        return combine_timetables(timetable_1, timetable_2)
    elif len(destinations) == 1:
        return get_timetable(darwin_client, source, destination)
    else:
        raise RuntimeError("Destination must be provided")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
