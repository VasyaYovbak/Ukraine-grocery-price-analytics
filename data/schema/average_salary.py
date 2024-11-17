from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType
from entities.base_period_model import ENG_BASE_PERIOD_VALUES


class AVERAGE_SALARY_INITIAL_COLUMNS:
    DATE = "Date"
    SALARY = "Salary"


AVERAGE_SALARY_INITIAL_SCHEMA = StructType(
    [
        StructField(AVERAGE_SALARY_INITIAL_COLUMNS.DATE, StringType(), True),
        StructField(AVERAGE_SALARY_INITIAL_COLUMNS.SALARY, FloatType(), True),
    ]
)


class AVERAGE_SALARY_COLUMNS:
    DATE = "Date"
    SALARY = "Salary"
    PreviousMonthPrice = ENG_BASE_PERIOD_VALUES.PreviousMonthPrice
    DecemberPreviousYearPrice = ENG_BASE_PERIOD_VALUES.DecemberPreviousYearPrice
    December2010Price = ENG_BASE_PERIOD_VALUES.December2010Price
    SamePeriodPreviousYearPrice = ENG_BASE_PERIOD_VALUES.SamePeriodPreviousYearPrice
    SameMonthPreviousYearPrice = ENG_BASE_PERIOD_VALUES.SameMonthPreviousYearPrice


AVERAGE_SALARY_SCHEMA = StructType(
    [
        StructField(AVERAGE_SALARY_COLUMNS.DATE, DateType(), False),
        StructField(AVERAGE_SALARY_COLUMNS.SALARY, FloatType(), False),
        StructField(AVERAGE_SALARY_COLUMNS.DecemberPreviousYearPrice,
                    FloatType(), True),
        StructField(AVERAGE_SALARY_COLUMNS.PreviousMonthPrice,
                    FloatType(), True),
        StructField(AVERAGE_SALARY_COLUMNS.December2010Price,
                    FloatType(), True),
        StructField(AVERAGE_SALARY_COLUMNS.SamePeriodPreviousYearPrice,
                    FloatType(), True),
        StructField(AVERAGE_SALARY_COLUMNS.SameMonthPreviousYearPrice,
                    FloatType(), True),
    ]
)
