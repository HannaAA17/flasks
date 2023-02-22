from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # Get the image file from the request
        image_file = request.files['image']

        # Load the image file using the Python Imaging Library (PIL)
        image = Image.open(io.BytesIO(image_file.read()))

        # Convert the image to PDF
        pdf_file = io.BytesIO()
        image.save(pdf_file, format='PDF')

        # Set the bytes to the beginning of the file
        pdf_file.seek(0)

        # Return the PDF file as a response
        return send_file(pdf_file, download_name='converted.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
