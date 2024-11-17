from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType
from entities.base_period_model import ENG_BASE_PERIOD_VALUES


class STOCK_PRICE_INITIAL_COLUMNS:
    DATE = "Date"
    PRICE = "Price"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    VOLUME = "Vol."
    CHANGE_PERCENT = "Change %"


STOCK_PRICE_INITIAL_SCHEMA = StructType(
    [
        StructField(STOCK_PRICE_INITIAL_COLUMNS.DATE, StringType(), True),
        StructField(STOCK_PRICE_INITIAL_COLUMNS.PRICE, FloatType(), True),
        StructField(STOCK_PRICE_INITIAL_COLUMNS.OPEN, FloatType(), True),
        StructField(STOCK_PRICE_INITIAL_COLUMNS.HIGH, FloatType(), True),
        StructField(STOCK_PRICE_INITIAL_COLUMNS.LOW, FloatType(), True),
        StructField(STOCK_PRICE_INITIAL_COLUMNS.VOLUME, StringType(), True),
        StructField(STOCK_PRICE_INITIAL_COLUMNS.CHANGE_PERCENT,
                    StringType(), True),
    ]
)


class STOCK_PRICE_UNPROCESED_COLUMNS:
    DATE = "Date"
    PRICE = "Price"
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CHANGE_PERCENT = "Change %"


STOCK_PRICE_UNPROCESED_SCHEMA = StructType(
    [
        StructField(STOCK_PRICE_UNPROCESED_COLUMNS.DATE, StringType(), False),
        StructField(STOCK_PRICE_UNPROCESED_COLUMNS.PRICE, FloatType(), False),
        StructField(STOCK_PRICE_UNPROCESED_COLUMNS.OPEN, FloatType(), False),
        StructField(STOCK_PRICE_UNPROCESED_COLUMNS.HIGH, FloatType(), False),
        StructField(STOCK_PRICE_UNPROCESED_COLUMNS.LOW, FloatType(), False),
        StructField(STOCK_PRICE_UNPROCESED_COLUMNS.CHANGE_PERCENT,
                    StringType(), False),
    ]
)


class STOCK_PRICE_COLUMNS:
    DATE = "Date"
    PRICE = "Price"
    PreviousMonthPrice = ENG_BASE_PERIOD_VALUES.PreviousMonthPrice
    DecemberPreviousYearPrice = ENG_BASE_PERIOD_VALUES.DecemberPreviousYearPrice
    December2010Price = ENG_BASE_PERIOD_VALUES.December2010Price
    SamePeriodPreviousYearPrice = ENG_BASE_PERIOD_VALUES.SamePeriodPreviousYearPrice
    SameMonthPreviousYearPrice = ENG_BASE_PERIOD_VALUES.SameMonthPreviousYearPrice


STOCK_PRICE_SCHEMA = StructType(
    [
        StructField(STOCK_PRICE_COLUMNS.DATE, DateType(), False),
        StructField(STOCK_PRICE_COLUMNS.PRICE, FloatType(), False),
        StructField(STOCK_PRICE_COLUMNS.DecemberPreviousYearPrice,
                    FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.PreviousMonthPrice,
                    FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.December2010Price, FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.SamePeriodPreviousYearPrice,
                    FloatType(), True),
        StructField(STOCK_PRICE_COLUMNS.SameMonthPreviousYearPrice,
                    FloatType(), True),
    ]
)
