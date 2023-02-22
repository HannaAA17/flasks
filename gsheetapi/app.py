import io, csv, pandas as pd

from flask import Flask, jsonify, request, send_file


app = Flask(__name__)

# read the data from the csv file
with open('companies_4.csv', 'r', encoding='utf-8-sig') as f:
    DF_LIST = list(csv.DictReader(f))
    DF = pd.DataFrame(DF_LIST)
    EXPORT_COLUMNS = DF.columns.tolist()[1:]
    # EXPORT_COLUMNS = [
    #     'العام', 'الفترة', 'المبيعات', 'تكاليف المبيعات', 'اجمالي الدخل', 
    #     'دخل العمليات', 'صافي الدخل', 'ربح السهم الصافي', 'عدد الأسهم',
    #     'رأس المال'
    # ]


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/json', methods=['GET', 'POST'])
def json():
    if request.method == 'GET':
        if request.args.get('comp_id'):
            comp_id = request.args.get('comp_id')
            print('GET request with filter', comp_id)
            
            # retrun the data as json
            return jsonify([
                {k: _[k] for k in EXPORT_COLUMNS}
                # _
                for _ in DF_LIST 
                if comp_id == _['comp_id']
            ])

        else:
            return jsonify(DF_LIST[:50])


@app.route('/csv', methods=['GET', 'POST'])
def csv():
    if request.method == 'GET':
        if request.args.get('comp_id'):
            comp_id = request.args.get('comp_id')
            print('GET request with filter', comp_id)
            
            # extract the data for the given comp_id
            df = DF[DF['comp_id'] == comp_id].iloc[:, 1:].copy()
            
            # return the data as csv
            csv_file = io.BytesIO()
            df.to_csv(csv_file, sep='\t', encoding='utf-8-sig', index=False)
            csv_file.seek(0)
            return send_file(csv_file, download_name='data.csv', as_attachment=True)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
