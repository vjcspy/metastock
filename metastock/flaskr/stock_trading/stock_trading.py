from flask import Blueprint, current_app, jsonify
from flask_restful import Api

from metastock.flaskr.stock_trading.controller.analysis_foreign import AnalysisForeign
from metastock.flaskr.stock_trading.controller.analysis_hullma import AnalysisHullmaResource

stock_trading = Blueprint('stock_trading', __name__, url_prefix='/stock-trading')

api = Api(stock_trading)


@stock_trading.route('/')
def index():
    current_app.logger.info(f"Process '/stock-trading'")
    return jsonify({"success": "true", "message": "Stock trading"}), 200


# Controller
api.add_resource(AnalysisHullmaResource, '/analysis/hullma')
api.add_resource(AnalysisForeign, '/analysis/foreign')
