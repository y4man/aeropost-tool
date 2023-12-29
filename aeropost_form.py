from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd

app = Flask(__name__)

def read_and_extract_data(csv_file, selected_headers):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Select only the columns specified in selected_headers
    df_selected = df[selected_headers]

    # Convert DataFrame to a dictionary
    header_data = df_selected.to_dict(orient='list')

    # Extract data into separate variables
    consignee = header_data.get('Consignee', [])
    description_code = header_data.get('Description Code', [])
    tin_number = header_data.get('TinNumber', [])

    # Extract 'Value' column as a list of strings
    values_str_list = header_data.get('Value', [])
    

    traffic_code = header_data.get('Traffic Code', [])
    mawb = header_data.get('MAWB', [])
    Weight_Lbs = header_data.get('Weight Lbs', [])

    return consignee, description_code, tin_number, values_str_list, traffic_code, mawb, Weight_Lbs



@app.route('/manifest', methods=['GET', 'POST'])
def manifest_form():
    if request.method == 'POST':
 # Create the root element for the XML document
        root = ET.Element('SADEntry')

         # Retrieve form data from the request object
        dateOfEntry = request.form.get('doe')
        airLine = request.form.get('vesselcode')
        flightNumber = request.form.get('voyogeno')
        carrier = request.form.get('carrier')
        carriername = request.form.get('carriername')
        shippingport = request.form.get('shippingport')
        billnumber = request.form.get('billnumber')
        pkgcount = request.form.get('pkgcount')
        pkgtype = request.form.get('pkgtype')
        grosswt = request.form.get('grosswt')
        grosswtunit = request.form.get('grosswtunit')
        grossvol = request.form.get('grossvol')
        grossvolunit = request.form.get('grossvolunit')
        ffname = request.form.get('ffname')
        ffaddress = request.form.get('ffaddress')
        ffcity = request.form.get('ffcity')
        ffstate = request.form.get('ffstate')
        ffcountry = request.form.get('ffcountry')
        ffzip = request.form.get('ffzip')
        netcost = request.form.get('netcost')
        netfreight = request.form.get('netfreight')
        arrivaldate = request.form.get('arrivaldate')
        departuredate = request.form.get('departuredate')
        dischargeport = request.form.get('dischargeport')
        tod = request.form.get('tod')
        categoryofgoods = request.form.get('categoryofgoods')
        regime = request.form.get('regime')
        contents = request.form.get('contents')
        csv_file = request.files['csv_file']

        # Process uploaded CSV file
        if 'csv_file' in request.files:
            # Read CSV file and get selected header data
            csv_file = request.files['csv_file']
            selected_headers = ['Consignee', 'Description Code', 'TinNumber', 'Value', 'Traffic Code', 'MAWB', 'Weight Lbs']
            consignee, description_code, tin_number, values_str_list, traffic_code, mawb, Weight_Lbs = read_and_extract_data(csv_file, selected_headers)

            # Calculate freight price for each row
            # Calculate freight price for each row
            net_freights = []
            insurance_prices = []

            # Convert netfreight and grosswt to float
            netfreight_float = float(netfreight)
            grosswt_float = float(grosswt)

            for weight, value in zip(Weight_Lbs, values_str_list):
                freight_price = (netfreight_float / grosswt_float) * float(weight)
                net_freights.append(freight_price)

                for ins in net_freights:  
                    # Calculate insurance price for each value and its corresponding net freight
                    insurance_price = (float(value) + ins) * 0.01  
                    insurance_prices.append(insurance_price)

            return render_template('display.html',
            dateOfEntry=dateOfEntry, airLine=airLine, flightNumber=flightNumber, carrier=carrier,regime=regime,
            carriername=carriername, shippingport=shippingport, billnumber=billnumber, pkgcount=pkgcount,
            pkgtype=pkgtype, grosswt=grosswt, grosswtunit=grosswtunit, grossvol=grossvol, contents=contents,grossvolunit=grossvolunit,ffname=ffname, ffaddress=ffaddress, ffcity=ffcity, ffstate=ffstate, ffcountry=ffcountry, ffzip=ffzip,netcost=netcost, netfreight=netfreight, arrivaldate=arrivaldate, departuredate=departuredate,dischargeport=dischargeport, tod=tod, categoryofgoods=categoryofgoods,net_freights=net_freights,insurance_prices=insurance_prices,
            #CSV RETURNS
            consignee=consignee, description_code=description_code, tin_number=tin_number,values_str_list=values_str_list, traffic_code=traffic_code,mawb=mawb, Weight_Lbs=Weight_Lbs, csv_file=csv_file) 

    # ... (handle other cases)
    return render_template('aeropost_form.html')  # Update with your actual form template

if __name__ == '__main__':
    app.run(debug=True)










