from flask import Flask, jsonify
from flask_cors import CORS
from backend.config import Config
from backend.routes.auth_routes import auth_bp
from backend.routes.farmer_routes import farmer_bp
from backend.routes.shop_routes import shop_bp
from backend.routes.predict_routes import predict_bp
from backend.routes.market_routes import market_bp
from backend.routes.ai_service import ai_service_bp
from backend.routes.pilot_routes import pilot_bp
from backend.routes.analytics_routes import analytics_bp
from backend.routes.notification_routes import notification_bp
from backend.ml_service import get_ml_service
import os

from backend import db

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{Config.DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Initialize ML Service (loads models at startup)
ml_service = get_ml_service()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(farmer_bp, url_prefix='/api/farmer')
app.register_blueprint(shop_bp, url_prefix='/api/shop')
app.register_blueprint(predict_bp, url_prefix='/api/predict')
app.register_blueprint(market_bp, url_prefix='/api/market')
app.register_blueprint(ai_service_bp)
app.register_blueprint(pilot_bp, url_prefix='/api/pilot')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(notification_bp, url_prefix='/api/notifications')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "HarvestLink API"})

@app.route('/api/model/info', methods=['GET'])
def model_info():
    return jsonify({
        "models": [
            {"name": "Crop Recommendation", "accuracy": "94.5%", "algorithm": "Random Forest"},
            {"name": "Market Demand", "score": "99.5%", "algorithm": "Random Forest Regressor"},
            {"name": "Price Crash", "recall": "91%", "algorithm": "Random Forest Classifier"},
            {"name": "Spoilage Risk", "score": "95%", "algorithm": "Random Forest"}
        ]
    })

if __name__ == '__main__':
    # Ensure database exists
    if not os.path.exists(Config.DB_PATH):
        print("Database not found. Please run database/init_db.py first.")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
