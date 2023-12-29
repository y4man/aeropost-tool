from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', download_link=None)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        df = pd.read_csv(file)
        xml_data = df.to_xml(index=False)

        # Save the XML data to a BytesIO buffer
        xml_buffer = BytesIO()
        xml_buffer.write(xml_data.encode())
        xml_buffer.seek(0)

        download_link = url_for('download', filename='output.xml')
        return render_template('index.html', download_link=download_link)

@app.route('/download/<filename>')
def download(filename):
    return send_file(
        'output.xml',
        download_name='output.xml',
        as_attachment=True,
        mimetype='application/xml'
    )

if __name__ == '__main__':
    app.run(debug=True)
