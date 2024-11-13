from pyspark.sql.types import StructType, StructField, StringType, FloatType


class STOCK_PRICE_COLUMNS:
    DATE = "Date"
    PRICE = "Price"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    VOLUME = "Vol."
    CHANGE_PERCENT = "Change %"


STOCK_PRICE_SCHEMA = StructType(
    [
        StructField(STOCK_PRICE_COLUMNS.DATE, StringType(), True),
        StructField(STOCK_PRICE_COLUMNS.PRICE, FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.OPEN, FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.HIGH, FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.LOW, FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.VOLUME, StringType(), True),
        StructField(STOCK_PRICE_COLUMNS.CHANGE_PERCENT, StringType(), True),
    ]
)
