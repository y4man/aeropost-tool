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
    values_str_list = header_data.get('Value', [])
    traffic_code = header_data.get('Traffic Code', [])
    mawb = header_data.get('MAWB', [])
    Weight_Lbs = header_data.get('Weight Lbs', [])

    return consignee, description_code, tin_number, values_str_list, traffic_code, mawb, Weight_Lbs


def create_items_element(data_item):
    items_element = ET.Element('Items')

    code_element = ET.Element('Code')
    code_element.text = data_item.get('Code', '')
    items_element.append(code_element)

    desc_element = ET.Element('Desc')
    desc_element.text = data_item.get('Desc', '')
    items_element.append(desc_element)

    cpc_element = ET.Element('CPC')
    cpc_element.text = data_item.get('CPC', '')
    items_element.append(cpc_element)

    preference_element = ET.Element('Preference')
    preference_element.text = data_item.get('Preference', '')
    items_element.append(preference_element)

    origin_element = ET.Element('Origin')
    origin_element.text = data_item.get('Origin', '')
    items_element.append(origin_element)

    qty_element = ET.Element('Qty')
    qty_element.text = data_item.get('Qty', '')
    items_element.append(qty_element)

    qty_unit_element = ET.Element('QtyUnit')
    qty_unit_element.text = data_item.get('QtyUnit', '')
    items_element.append(qty_unit_element)

    cost_element = ET.Element('Cost')
    cost_element.text = data_item.get('Cost', '')
    items_element.append(cost_element)

    insurance_element = ET.Element('Insurance')
    insurance_element.text = data_item.get('Insurance', '')
    items_element.append(insurance_element)

    freight_element = ET.Element('Freight')
    freight_element.text = data_item.get('Freight', '')
    items_element.append(freight_element)

    inv_number_element = ET.Element('InvNumber')
    inv_number_element.text = data_item.get('InvNumber', '')
    items_element.append(inv_number_element)

    waiver_pct_element = ET.Element('WaiverPct')
    waiver_pct_element.text = data_item.get('WaiverPct', '')
    items_element.append(waiver_pct_element)

    return items_element


def create_consolidated_item_element(data_item):
    consolidated_item_element = ET.Element('ConsolidatedItem')

    importer_element = ET.Element('Importer')
    importer_number_element = ET.Element('Number')
    importer_number_element.text = str(data_item['Importer']['Number'])
    importer_element.append(importer_number_element)
    consolidated_item_element.append(importer_element)

    exporter_element = ET.Element('Exporter')
    exporter_name_element = ET.Element('Name')
    exporter_name_element.text = data_item['Exporter']['Name']
    exporter_element.append(exporter_name_element)
    # ... add other exporter elements

    # Add Consignment, Shipment, Packages, Valuation, and other elements here based on data_item

    items_element = create_items_element(data_item['Items'])
    consolidated_item_element.append(items_element)

    return consolidated_item_element


@app.route('/manifest', methods=['GET', 'POST'])
def manifest_form():
    if request.method == 'POST':
        # Create the root element for the XML document
        root = ET.Element('SADEntry')

        # Retrieve form data from the request object
        dateOfEntry = request.form.get('doe')
        regime = request.form.get('regime')

        # Assuming you have multiple items, create a list of dictionaries
        your_data = [
            {
                'Importer': {'Number': '20001428'},
                'Exporter': {
                    'Name': 'AEROPOST INTERNATIONAL',
                    'Address': 'AEROPOST',
                    'City': 'DORAL',
                    'State': 'FL',
                    'PostalCode': '33172',
                    'Country': 'USA',
                },
                'Consignment': {
                    'DepartureDate': '2023-12-19',
                    'ArrivalDate': '2023-12-19',
                    'ExportCountry': 'USA',
                    'ImportCountry': 'CYM',
                    'ShippingPort': 'USMIA',
                    'DischargePort': 'KYGCM',
                    'TransportMode': 'AIR',
                },
                'Shipment': {
                    'VesselCode': 'II',
                    'VoyageNo': '211',
                    'ShippingAgent': 'II',
                    'BillNumber': '17522497123',
                    'BillType': 'CONSOLIDATED',
                },
                'Packages': {
                    'PkgCount': '17',
                    'PkgType': 'BG',
                    'GrossWt': '814',
                    'GrossWtUnit': 'LB',
                    'GrossVol': '1',
                    'GrossVolUnit': 'CF',
                    'Contents': 'General merchandise',
                    'CategoryOfGoods': '1',
                },
                'Valuation': {
                    'Currency': 'USD',
                    'NetCost': '23961.85',
                    'NetInsurance': '283.47',
                    'NetFreight': '4384.80',
                    'TermsOfDelivery': 'FOB',
                },
                # ... add other fields for the first item
            },
            {
                'Importer': {'Number': '21639542'},
                'Exporter': {
                    'Name': 'AEROPOST INTERNATIONAL',
                    'Address': 'AEROPOST',
                    'City': 'DORAL',
                    'State': 'FL',
                    'PostalCode': '33172',
                    'Country': 'USA',
                    'Phone': '',
                },
                'Finance': {
                    'FinanceParty': 'T',
                    'GuaranteeType': 'BD',
                },
                'BillNumber': 'ABBEY-101PM-7123',
                'Packages': {
                    'PkgCount': '1',
                    'PkgType': 'BG',
                    'GrossWt': '0.00',
                    'GrossWtUnit': 'LB',
                    'GrossVol': '0',
                    'GrossVolUnit': 'CF',
                    'Contents': '17522497123 - ABBEYGAIL ROBINSON - General merchandise',
                    'CategoryOfGoods': '1',
                },
                'Valuation': {
                    'Currency': 'USD',
                    'NetCost': '116.45',
                    'NetInsurance': '1.21',
                    'NetFreight': '4.31',
                    'TermsOfDelivery': 'FOB',
                },
                'Items': {
                    'Code': '9802.00.61',
                    'Desc': 'WIG',
                    'CPC': 'IM100',
                    'Preference': '0',
                    'Origin': 'USA',
                    'Qty': '1.0000',
                    'QtyUnit': 'KG',
                    'Cost': '116.45',
                    'Insurance': '1.21',
                    'Freight': '4.31',
                    'InvNumber': 'ATTACHED',
                    'WaiverPct': '0.00',
                },
                'MoneyDeclaredFlag': 'N',
                # ... add other fields for the second item
            },
            # ... add more dictionaries for additional items
        ]

        consolidated_items_element = ET.Element('ConsolidatedItems')

        # Iterate through your data and create elements
        for data_item in your_data:
            consolidated_item_element = create_consolidated_item_element(data_item)
            consolidated_items_element.append(consolidated_item_element)

        root.append(consolidated_items_element)

        # Convert the XML structure to a formatted string
        xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

        # Save or use the XML string as needed
        with open("output2.xml", "w") as xml_file:
            xml_file.write(xml_string)

        # Process uploaded CSV file
        if 'csv_file' in request.files:
            # Read CSV file and get selected header data
            csv_file = request.files['csv_file']
            selected_headers = ['Consignee', 'Description Code', 'TinNumber', 'Value', 'Traffic Code', 'MAWB', 'Weight Lbs']
            consignee, description_code, tin_number, values_str_list, traffic_code, mawb, Weight_Lbs = read_and_extract_data(csv_file, selected_headers)

            # Calculate freight price for each row
            net_freights = []
            insurance_prices = []

            netfreight_float = float(request.form.get('netfreight'))
            grosswt_float = float(request.form.get('grosswt'))

            for weight, value in zip(Weight_Lbs, values_str_list):
                freight_price = (netfreight_float / grosswt_float) * float(weight)
                net_freights.append(freight_price)

                for ins in net_freights:
                    insurance_price = (float(value) + ins) * 0.01
                    insurance_prices.append(insurance_price)

            return render_template('display.html',
                                   dateOfEntry=dateOfEntry, regime=regime,
                                   net_freights=net_freights, insurance_prices=insurance_prices,
                                   consignee=consignee, description_code=description_code,
                                   tin_number=tin_number, values_str_list=values_str_list,
                                   traffic_code=traffic_code, mawb=mawb, Weight_Lbs=Weight_Lbs,
                                   csv_file=csv_file)

    return render_template('aeropost_form.html')

if __name__ == '__main__':
    app.run(debug=True)
