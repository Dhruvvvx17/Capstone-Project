from flask import Flask, request, render_template, jsonify
import client

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    lat_in = request.form['lat']
    #word = request.args.get('lat')
    long_in = request.form['lon']
    district=request.form['district']
    area=request.form['area']

    res = client.suggest_crops(lat_in,long_in,district,area)
    
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/api', methods=['POST'])
def my_api_post(): 
    request_data=request.get_json() 

    lat_in = float(request_data['lat'])
    #word = request.args.get('lat')
    long_in = float(request_data['lon'])
    district=request_data['district']
    area=float(request_data['area'])
    if(lat_in<9.9477 or lat_in >20.0210 or long_in<70.8157 or long_in > 85.1463):
        return jsonify({"error" : "Coordinates out of range"})
    res = client.suggest_crops(lat_in,long_in,district,area)
    
    result = {
        "output": res
    }
    
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)



if __name__ == '__main__':
    app.run(debug=True)