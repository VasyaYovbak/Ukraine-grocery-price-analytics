import enum

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    BooleanType,
    IntegerType,
)


class UKRAINE_PRICE_INITIAL_COLUMNS:
    INDICATOR = "Показник"
    BASE_PERIOD = "Базисний період"
    TERRITORIAL_BREAKDOWN = "Територіальний розріз"
    TYPE_OF_GOODS_AND_SERVICES = "Тип товарів і послуг"
    FREQUENCY = "Періодичність"
    PERIOD = "Період"
    OBSERVATION_VALUE = "Значення спостереження"
    UNIT_OF_MEASUREMENT = "Одиниця виміру"
    SCALING = "Масштабування"
    NUMBER_OF_DECIMAL_PLACES = "Кількість десяткових знаків"
    CONFIDENTIALITY = "Конфіденційність"
    TIME_SERIES_NOTES = "Примітки часового ряду"
    OBSERVATION_NOTES = "Примітки спостереження"


INITIAL_SCHEMA = StructType(
    [
        StructField(UKRAINE_PRICE_INITIAL_COLUMNS.INDICATOR, StringType(), True),
        StructField(UKRAINE_PRICE_INITIAL_COLUMNS.BASE_PERIOD, StringType(), True),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.TERRITORIAL_BREAKDOWN, StringType(), True
        ),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.TYPE_OF_GOODS_AND_SERVICES, StringType(), True
        ),
        StructField(UKRAINE_PRICE_INITIAL_COLUMNS.FREQUENCY, StringType(), True),
        StructField(UKRAINE_PRICE_INITIAL_COLUMNS.PERIOD, StringType(), True),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.OBSERVATION_VALUE, StringType(), True
        ),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.UNIT_OF_MEASUREMENT, StringType(), True
        ),
        StructField(UKRAINE_PRICE_INITIAL_COLUMNS.SCALING, StringType(), True),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.NUMBER_OF_DECIMAL_PLACES, StringType(), True
        ),
        StructField(UKRAINE_PRICE_INITIAL_COLUMNS.CONFIDENTIALITY, StringType(), True),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.TIME_SERIES_NOTES, StringType(), True
        ),
        StructField(
            UKRAINE_PRICE_INITIAL_COLUMNS.OBSERVATION_NOTES, StringType(), True
        ),
    ]
)


class UKRAINE_PRICE_COLUMNS:
    INDICATOR = "indicator"
    BASE_PERIOD = "base_period"
    TERRITORIAL_BREAKDOWN = "territorial_breakdown"
    TYPE_OF_GOODS_AND_SERVICES = "type_of_goods_and_services"
    FREQUENCY = "frequency"
    PERIOD = "period"
    OBSERVATION_VALUE = "observation_value"
    UNIT_OF_MEASUREMENT = "unit_of_measurement"
    SCALING = "scaling"
    NUMBER_OF_DECIMAL_PLACES = "number_of_decimal_places"
    FROM_YEAR = "from_year"
    CORE_INFLATION_DESCRIPTION = "core_inflation_description"
    CORE_INFLATION_CALCULATION = "core_inflation_calculation"
    DATA_EXCLUSION_2014 = "data_exclusion_2014"
    DATA_EXCLUSION_2015_2021 = "data_exclusion_2015_2021"
    DATA_EXCLUSION_2022_2024 = "data_exclusion_2022_2024"
    CLASSIFICATION = "classification"
    DATA_REVIEW = "data_review"
    REGION_CODES = "region_codes"


UKRAINE_PRICE_SCHEMA = StructType(
    [
        StructField(UKRAINE_PRICE_COLUMNS.INDICATOR, StringType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.BASE_PERIOD, StringType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN, StringType(), False),
        StructField(
            UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES, StringType(), False
        ),
        StructField(UKRAINE_PRICE_COLUMNS.FREQUENCY, StringType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.PERIOD, StringType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.OBSERVATION_VALUE, DoubleType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.UNIT_OF_MEASUREMENT, StringType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.SCALING, StringType(), False),
        StructField(
            UKRAINE_PRICE_COLUMNS.NUMBER_OF_DECIMAL_PLACES, StringType(), False
        ),
        StructField(UKRAINE_PRICE_COLUMNS.FROM_YEAR, IntegerType(), False),
        StructField(
            UKRAINE_PRICE_COLUMNS.CORE_INFLATION_DESCRIPTION, BooleanType(), False
        ),
        StructField(
            UKRAINE_PRICE_COLUMNS.CORE_INFLATION_CALCULATION, BooleanType(), False
        ),
        StructField(UKRAINE_PRICE_COLUMNS.DATA_EXCLUSION_2014, BooleanType(), False),
        StructField(
            UKRAINE_PRICE_COLUMNS.DATA_EXCLUSION_2015_2021, BooleanType(), False
        ),
        StructField(
            UKRAINE_PRICE_COLUMNS.DATA_EXCLUSION_2022_2024, BooleanType(), False
        ),
        StructField(UKRAINE_PRICE_COLUMNS.CLASSIFICATION, BooleanType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.DATA_REVIEW, BooleanType(), False),
        StructField(UKRAINE_PRICE_COLUMNS.REGION_CODES, BooleanType(), False),
    ]
)
