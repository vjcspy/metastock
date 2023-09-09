from marshmallow import Schema, fields, validate


class PriceHistorySchema(Schema):
    date = fields.Date(required = True)
    high = fields.Integer(required = True, validate = validate.Range(min = 0))
    low = fields.Integer(required = True, validate = validate.Range(min = 0))
    close = fields.Integer(required = True, validate = validate.Range(min = 0))
    open = fields.Integer(required = True, validate = validate.Range(min = 0))
    volume = fields.Integer(required = True, validate = validate.Range(min = 0))
    trade = fields.Integer(required = True, validate = validate.Range(min = 0))
    value = fields.Integer(required = True, validate = validate.Range(min = 0))
    buy = fields.Integer(required = True, validate = validate.Range(min = 0))
    buyQuantity = fields.Integer(required = True, validate = validate.Range(min = 0))
    sell = fields.Integer(required = True, validate = validate.Range(min = 0))
    sellQuantity = fields.Integer(required = True, validate = validate.Range(min = 0))


priceHistorySchema = PriceHistorySchema()
