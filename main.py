import flask
from flask import request,jsonify
from database import fetch_annaul_data,load_data

app = flask.Flask(__name__)

@app.route('/data')
def get_data():
    """
    API endpoint to retrieve annual data for a well.
    """

    # Fetch data from request
    api_well_number = request.args.get('well')

    # Check if the required parameter 'well' is present
    if not api_well_number:
        return jsonify({"error": "Missing required parameter"}), 400 
 
    # Call the fetch_annual_data function to retrieve data for the well
    annual_well_data =  fetch_annaul_data(int(api_well_number))
    
    # Check if data was found
    if annual_well_data:
        return jsonify(annual_well_data)
    else:
        return jsonify({"error": "No data found for this well"}), 404  


if __name__ == '__main__':
    excel_path = r'C:\Users\Ebin\Desktop\python\Python-Flask-application\20210309_2020_1 - 4 (1) (1) (1) (1).xls' 
    load_data(excel_path)
    app.run(host='0.0.0.0', port=8080) 