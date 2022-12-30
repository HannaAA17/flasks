import time
from . import ExcelFile
from flask import Flask, render_template, make_response


app = Flask(__name__)


@app.route("/")
def index():
    """"""
    return render_template("index.html")


@app.route("/serve")
def serve():
    time.sleep(5)
    file_ob = ExcelFile()
    response = make_response(file_ob.file.read())
    response.headers.set(
        "Content-Type",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response.headers.set(
        "Content-Disposition", "attachment", filename="generated_file.xlsx"
    )
    response.headers.set("filename", "generated_file__2.xlsx")
    return response
