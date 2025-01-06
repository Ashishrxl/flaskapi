from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Load the trained model
with open('sales_model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json
        product_id = data['product_id']
        date = pd.to_datetime(data['date']).toordinal()
        
        # Predict sales quantity
        prediction = model.predict([[product_id, date]])
        return jsonify({'predicted_quantity': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
