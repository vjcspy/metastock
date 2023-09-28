from flask import current_app
from flask_restful import fields, marshal_with, reqparse, Resource

from metastock.modules.com.technical_indicator.hullma import Hullma
from metastock.modules.core.util.datetime.datetime_to_str import datetime_to_str

get_hullma_resource_response = {
    'success': fields.String,
    'data'   : fields.List(fields.Raw)
}

# Khởi tạo parser
parser = reqparse.RequestParser()
parser.add_argument('symbol', type=str, required=True, help='Symbol cannot be blank', location='args')


class AnalysisHullmaResource(Resource):
    @marshal_with(get_hullma_resource_response)
    def get(self):
        args = parser.parse_args()

        symbol = args['symbol']

        current_app.logger.info(f"Process get Hullma for symbol '{symbol}'")

        hullma = Hullma(symbol=symbol)
        hullma_data = hullma.get_data()

        close = hullma.get_price_helper().get_df()['close']
        
        return {
            'success': True,
            'data'   : [
                {
                    'd'     : datetime_to_str(index),
                    'hullma': hullma_data.get(index, None),
                    'close' : value
                }
                for index, value in close.items()
            ]
        }
