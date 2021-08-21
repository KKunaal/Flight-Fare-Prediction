#Necessary Library Imports
from CustomLogger.logger import Logger
import numpy as np
from DatabaseConnection.Database import Connector
from flask import Flask, request, render_template
from forms import SignUpForm
from joblib import load
from featureSetting import getResult

# Secret key to keep the client-side sessions secure
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABC235G5K8'


logging = Logger('logFiles/test.log')


@app.route("/", methods = ['GET','POST'])
def home():
    form = SignUpForm()
    if request.method == 'POST':
        logging.info('INFO', 'Requested method : POST')
        if form.is_submitted():
            model = load('FinalModel.pkl')
            logging.info('INFO', 'Pickle Model Loaded')
            result = request.form.to_dict()
            try:
                logging.info('INFO', 'Data Converted ')
                result['Total_Duration'] = int(result['Total_Duration'])
                if result['Source'] == result['Destination']:
                    return render_template('index.html', form=form, value1=0, value2=0,Rs='Rs')
                else:
                    if result['Total_Duration'] < 10:
                        result = getResult(result)
                        output = model.predict(result)
                        logging.info('INFO', 'Prediction success!')
                        minfare = np.round(output) - 1000
                        maxfare = np.round(output) + 1000
                        logging.info('INFO', 'Output displayed!')
                        return render_template('index.html', form=form, value1=int(minfare), value2=int(maxfare),Rs='Rs')
                    else:
                        return render_template('index.html', form=form, value1='Duration Should be less than 10 Hour')
            except:
                logging.info('ERROR', "Excepted integer got String")
                return render_template('index.html', form=form,value1='Give Duration In numbers Only')


    return render_template('index.html',form=form,value1=None,value2=None)

#DataBase API
@app.route("/DatabaseData", methods = ['GET','POST'])
def test():
    heading = ("id", "Airline", "Destination", "Day", "Month", "Source", "Total_Duration","Total_Stops")
    data = Connector()
    return render_template('Databasedata.html', heading=heading, data=data.getData())


# Main File Run Debug Mode
if __name__ == "__main__":
    app.run(port=8000,host='0.0.0.0')