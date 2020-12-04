from flask import Flask, request, render_template, jsonify
import coordinates_to_crops

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
    res = coordinates_to_crops.list_of_crops(lat_in,long_in,district)
    
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)