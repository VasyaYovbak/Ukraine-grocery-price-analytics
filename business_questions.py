from bokeh.io import curdoc
from bokeh.plotting import figure
from streamlit import bokeh_chart
from bokeh.models import Span
from bokeh.plotting import figure
from entities.base_period_model import BASE_PERIOD_UKRAINE_ENG_MAPPER
from pyspark.sql import SparkSession
import pandas as pd
import streamlit as st
from pyspark.sql.functions import col, to_timestamp
from data.schema.ukraine_price_dataset import UKRAINE_PRICE_SCHEMA, UKRAINE_PRICE_COLUMNS
from data.schema.usd_currency_dataset import STOCK_PRICE_COLUMNS, STOCK_PRICE_SCHEMA
from data.schema.average_salary import AVERAGE_SALARY_COLUMNS, AVERAGE_SALARY_SCHEMA
import numpy as np
import sys
import os
from bokeh.models import Range1d, LinearAxis
from sarimax import initialize_sarimax_model, get_trained_sarimax_predictions, get_future_sarimax_predicitons
from chronos_predictions import get_chronos_future_predicitons
from chat_openai_predictions import get_openai_future_predicitons
from pyspark.sql import SparkSession


# from dataplane import s3_download
import os
import boto3
from botocore.client import Config
import json

from pathlib import Path
from st_files_connection import FilesConnection

parent_dir = Path().resolve().parent

if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

parent_dir = str(parent_dir).replace("\\", "/") + "/"


curdoc().theme = 'dark_minimal'

spark = SparkSession.builder.appName("ukrainian_prices").getOrCreate()

DATA_LOADERS = {
    "Середні ціни споживчих товарів": "average_consuming_goods_prices",
    "Базові індекси споживчих цін": "base_index_consuming_prices",
    "Індекси споживчих цін": "index_consuming_prices"
}

AccountID = os.environ["secret_dp_S3_ACCOUNT_ID"]
Bucket = os.environ["secret_dp_BUCKET_NAME"]
ClientAccessKey = os.environ["secret_dp_S3_ACCESS_KEY"]
ClientSecret = os.environ["secret_dp_S3_SECRET"]
ConnectionUrl = f"https://{AccountID}.r2.cloudflarestorage.com"


S3Connect = boto3.client(
    's3',
    endpoint_url=ConnectionUrl,
    aws_access_key_id=ClientAccessKey,
    aws_secret_access_key=ClientSecret,
    config=Config(signature_version='s3v4'),
)


def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3r = boto3.resource('s3', aws_access_key_id=ClientAccessKey,
                         aws_secret_access_key=ClientSecret, endpoint_url=ConnectionUrl)
    bucket = s3r.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix=remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key)


# File Locations
file_locations = [
    "usd_uah_currency_with_basis.csv",
    "splited_data/average_consuming_goods_prices.csv",
    "splited_data/base_index_consuming_prices.csv",
    "splited_data/index_consuming_prices.csv",
    "average_salary.csv"
]

if not os.path.exists('average_salary.csv'):
    print("Downloading files from S3...")
    for file_path in file_locations:
        local_file_path = os.path.join(
            'temp_data', os.path.basename(file_path))
        downloadDirectoryFroms3(Bucket, file_path,)
else:
    print("Files already downloaded.")


def load_data(data_type):
    csv_file_path = f"splited_data/{data_type}.csv"
    df = (spark.read.format("csv")
          .option("header", "true")
          .schema(UKRAINE_PRICE_SCHEMA)
          .load(csv_file_path))

    filtered_df = df.filter(~(df[UKRAINE_PRICE_COLUMNS.BASE_PERIOD].isin(
        "Рік до попереднього року", "Грудень до грудня попереднього року")))

    return filtered_df


def load_usd_currency_data():
    csv_file_path = f"usd_uah_currency_with_basis.csv"
    return (spark.read.format("csv")
            .option("header", "true")
            .schema(STOCK_PRICE_SCHEMA)
            .load(csv_file_path))


def load_average_salary_data():
    csv_file_path = f"average_salary.csv"
    return (spark.read.format("csv")
            .option("header", "true")
            .schema(AVERAGE_SALARY_SCHEMA)
            .load(csv_file_path))


def filter_data(df, column, value):
    return df.filter(col(column) == value)


def select_training_data_from_df(df):
    return df.select(
        to_timestamp(col(UKRAINE_PRICE_COLUMNS.PERIOD),
                     "yyyy-'M'MM").alias("date"),
        col(UKRAINE_PRICE_COLUMNS.OBSERVATION_VALUE).alias("price"),
    ).toPandas().sort_values("date")


def select_data_from_usd_currency_df(df, base_period):
    return df.select(
        to_timestamp(col(STOCK_PRICE_COLUMNS.DATE)).alias("date"),
        col(base_period).alias("price"),
    ).toPandas().sort_values("date")


def select_data_from_average_salary_df(df, base_period):
    return df.select(
        to_timestamp(col(AVERAGE_SALARY_COLUMNS.DATE)).alias("date"),
        col(base_period).alias("salary"),
    ).toPandas().sort_values("date")


def st_show_relative_prices():
    def visualize_predictions(real_data, usd_currency_data, average_salary_data, title='Predictions', show_normilized_value=True):
        p = figure(title=title, x_axis_label='Час', x_axis_type='datetime',
                   y_axis_label='Значення', width=800, height=400)
        p.line(x=real_data['date'], y=real_data['price'], line_width=2,
               color='red', legend_label='Goods Price Data')

        if not show_normilized_value:
            p.extra_y_ranges = {
                "usd_curr": Range1d(start=usd_currency_data['price'].iloc[0], end=usd_currency_data['price'].iloc[-1]*1.1),
                "avg_salary": Range1d(start=average_salary_data['salary'].iloc[0], end=average_salary_data['salary'].iloc[-1]*1.1)
            }

            p.add_layout(LinearAxis(y_range_name="usd_curr"), 'right')
            p.add_layout(LinearAxis(y_range_name="avg_salary"), 'right')
            p.y_range = Range1d(real_data['price'].iloc[0],
                                real_data['price'].iloc[-1]*1.1)

            p.line(x=usd_currency_data['date'], y=usd_currency_data['price'], line_width=2,
                   color='green', legend_label='Usd Currency Data', y_range_name="usd_curr")

            p.line(x=average_salary_data['date'], y=average_salary_data['salary'], line_width=2,
                   color='blue', legend_label='Avarege Salary Data', y_range_name="avg_salary")
        else:
            p.line(x=usd_currency_data['date'], y=usd_currency_data['price'], line_width=2,
                   color='green', legend_label='Usd Currency Data')

            p.line(x=average_salary_data['date'], y=average_salary_data['salary'], line_width=2,
                   color='blue', legend_label='Avarege Salary Data')

        p.x_range = Range1d(
            real_data['date'].iloc[0], real_data['date'].iloc[-1])

        p.legend.location = "top_left"
        p.legend.title = "Дані"
        p.legend.click_policy = "hide"

        bokeh_chart(p, use_container_width=True)

    st.title("Прогнозування споживчих цін України")

    # Step 1: Select data type
    data_type = st.selectbox("Оберіть тип даних:", list(
        DATA_LOADERS.keys()), index=None)
    if data_type:
        st.success(f"Ви обрали: {data_type}")

        # Step 2: Load and select product
        df = load_data(DATA_LOADERS[data_type])
        usd_currency_df = load_usd_currency_data()
        avarage_salary_df = load_average_salary_data()
        products = df.select(
            UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES).distinct().toPandas()
        product_name = st.selectbox(
            "Оберіть товар:", products[UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES], index=None)
        if product_name:
            st.success(f"Ви обрали: {product_name}")
            df = filter_data(
                df, UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES, product_name)

            # Step 3: Select base period
            base_periods = df.select(
                UKRAINE_PRICE_COLUMNS.BASE_PERIOD).distinct().toPandas()
            base_period = st.selectbox(
                "Оберіть базисний період:", base_periods[UKRAINE_PRICE_COLUMNS.BASE_PERIOD], index=None)
            if base_period:
                st.success(f"Ви обрали: {base_period}")
                df = filter_data(
                    df, UKRAINE_PRICE_COLUMNS.BASE_PERIOD, base_period)

                # Step 4: Select region
                regions = df.select(
                    UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN).distinct().toPandas()
                region = st.selectbox(
                    "Оберіть регіон:", regions[UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN], index=None)
                if region:
                    st.success(f"Ви обрали: {region}")
                    df = filter_data(
                        df, UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN, region)

                    # Step 5: Train model
                    data = select_training_data_from_df(df)
                    usd_currency_data = select_data_from_usd_currency_df(
                        usd_currency_df, BASE_PERIOD_UKRAINE_ENG_MAPPER[base_period] if base_period != "Не застосовується" else STOCK_PRICE_COLUMNS.PRICE)
                    average_salary_data = select_data_from_average_salary_df(
                        avarage_salary_df, BASE_PERIOD_UKRAINE_ENG_MAPPER[base_period] if base_period != "Не застосовується" else AVERAGE_SALARY_COLUMNS.SALARY)

                    visualize_predictions(
                        data, usd_currency_data, average_salary_data, 'Comparison', show_normilized_value=data_type != "Середні ціни споживчих товарів")


def st_show_buckets_prices():
    def visualize_predictions(bucket_counts_data, bucket_price_data, title=''):
        p = figure(title=title, x_axis_label='Час', x_axis_type='datetime',
                   y_axis_label='Значення', width=800, height=400)

        p.line(x=bucket_counts_data['date'], y=bucket_counts_data['counts'], line_width=2,
               color='orange', legend_label='Bucket Counts Data')

        p.extra_y_ranges = {
            "bucket_price": Range1d(start=bucket_price_data['price'].min()*0.9, end=bucket_price_data['price'].max()*1.1)
        }

        p.line(x=bucket_price_data['date'], y=bucket_price_data['price'], line_width=2,
               color='blue', legend_label='Bucket Price Data', y_range_name="bucket_price")

        p.add_layout(LinearAxis(y_range_name="bucket_price"), 'right')
        p.y_range = Range1d(bucket_counts_data['counts'].min()*0.9,
                            bucket_counts_data['counts'].max()*1.1)

        p.x_range = Range1d(
            bucket_price_data['date'].iloc[0], bucket_price_data['date'].iloc[-1])

        p.legend.location = "top_left"
        p.legend.title = "Дані"
        p.legend.click_policy = "hide"

        bokeh_chart(p, use_container_width=True)

    df_spark = load_data(DATA_LOADERS["Середні ціни споживчих товарів"])
    avarage_salary_df = load_average_salary_data()

    df = df_spark.toPandas()

    st.title("Візуалізація вартості кошика товарів")

    # Step 1: Create a basket of goods
    products = df[UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES].unique()
    basket = {}

    st.header("Формуйте кошик товарів")
    st.write("Оберіть товари та їх кількість для формування кошика:")

    for product in sorted(products):

        product_info = df[df[UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES] == product]
        unit_of_measurement = product_info[UKRAINE_PRICE_COLUMNS.UNIT_OF_MEASUREMENT].iloc[0]
        scaling = product_info[UKRAINE_PRICE_COLUMNS.SCALING].iloc[0]

        # Add this information to the product name
        label = f"{product} ({unit_of_measurement}, масштаб: {scaling})"
        quantity = st.number_input(
            label, min_value=0, step=1, key=product)
        if quantity > 0:
            basket[product] = quantity

    if basket:
        st.success(f"Ваш кошик: {basket}")

        regions = df[UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN].unique()
        region = st.selectbox(
            "Оберіть регіон для аналізу:", regions, index=None)

        if region:
            st.success(f"Ви обрали регіон: {region}")
            df_region = df[df[UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN] == region]

            basket_costs = []

            unique_dates = df_region[UKRAINE_PRICE_COLUMNS.PERIOD].unique()
            for date in unique_dates:
                date_data = df_region[df_region[UKRAINE_PRICE_COLUMNS.PERIOD] == date]

                total_cost = 0
                for product, quantity in basket.items():
                    product_data = date_data[date_data[UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES] == product]
                    if not product_data.empty:
                        product_price = product_data[UKRAINE_PRICE_COLUMNS.OBSERVATION_VALUE].iloc[0]
                        total_cost += product_price * quantity

                basket_costs.append({"date": date, "Basket Cost": total_cost})

            basket_costs_df = pd.DataFrame(basket_costs)
            basket_costs_df['date'] = pd.to_datetime(
                basket_costs_df['date'], format='%Y-M%m')  # Ensure proper date formatting
            basket_costs_df.sort_values('date', inplace=True)

            st.write("Вартість кошика для кожної дати:")

            average_salary_data = select_data_from_average_salary_df(
                avarage_salary_df, AVERAGE_SALARY_COLUMNS.SALARY)

            combined = basket_costs_df.join(
                average_salary_data.set_index('date'), on='date').dropna()
            combined['counts'] = combined['salary'] / combined['Basket Cost']

            basket_costs_df.columns = ['date', 'price']

            visualize_predictions(
                combined, basket_costs_df, 'Comparison')
    else:
        st.warning("Будь ласка, додайте товари до кошика.")


def st_show_goods_prices_predictions():
    def visualize_predictions(real_data, train_predictions, test_predictions, title='Predictions'):
        p = figure(title=title, x_axis_label='Час', x_axis_type='datetime',
                   y_axis_label='Значення', width=800, height=400)

        p.line(x=real_data['date'], y=real_data['price'], line_width=2,
               color='red', legend_label='Real Data')

        p.line(x=train_predictions['date'], y=train_predictions['mean'], line_width=2,
               color='blue', legend_label='Реальні дані')
        train_columns = train_predictions.columns.to_list()
        if ('upper' in train_columns and 'lower' in train_columns):
            p.varea(x=train_predictions['date'], y1=train_predictions['lower'],
                    y2=train_predictions['upper'], color='blue', alpha=0.2)

        p.line(x=test_predictions['date'], y=test_predictions['mean'], line_width=2,
               color='orange', legend_label='Передбачення')
        test_columns = test_predictions.columns.to_list()
        if ('upper' in test_columns and 'lower' in test_columns):
            p.varea(x=test_predictions['date'], y1=test_predictions['lower'],
                    y2=test_predictions['upper'], color='orange', alpha=0.2)

        # Додавання вертикальних ліній для розмежування тренувального і тестового наборів
        train_separator = Span(location=train_predictions['date'].max(), dimension='height',
                               line_color='green', line_dash='dashed', line_width=2)
        test_separator = Span(location=test_predictions['date'].max(), dimension='height',
                              line_color='red', line_dash='dashed', line_width=2)
        p.add_layout(train_separator)
        p.add_layout(test_separator)

        p.legend.location = "top_left"
        p.legend.title = "Дані"

        bokeh_chart(p, use_container_width=True)

    # Initialize Spark Session
    st.title("Прогнозування споживчих цін України")

    # Step 1: Select data type
    data_type = st.selectbox("Оберіть тип даних:", list(
        DATA_LOADERS.keys()), index=None)
    if data_type:
        st.success(f"Ви обрали: {data_type}")

        # Step 2: Load and select product
        df = load_data(DATA_LOADERS[data_type])
        products = df.select(
            UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES).distinct().toPandas()
        product_name = st.selectbox(
            "Оберіть товар:", products[UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES], index=None)
        if product_name:
            st.success(f"Ви обрали: {product_name}")
            df = filter_data(
                df, UKRAINE_PRICE_COLUMNS.TYPE_OF_GOODS_AND_SERVICES, product_name)

            # Step 3: Select base period
            base_periods = df.select(
                UKRAINE_PRICE_COLUMNS.BASE_PERIOD).distinct().toPandas()
            base_period = st.selectbox(
                "Оберіть базисний період:", base_periods[UKRAINE_PRICE_COLUMNS.BASE_PERIOD], index=None)
            if base_period:
                st.success(f"Ви обрали: {base_period}")
                df = filter_data(
                    df, UKRAINE_PRICE_COLUMNS.BASE_PERIOD, base_period)

                # Step 4: Select region
                regions = df.select(
                    UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN).distinct().toPandas()
                region = st.selectbox(
                    "Оберіть регіон:", regions[UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN], index=None)
                if region:
                    st.success(f"Ви обрали: {region}")
                    df = filter_data(
                        df, UKRAINE_PRICE_COLUMNS.TERRITORIAL_BREAKDOWN, region)

                    # Step 5: Train model
                    data = select_training_data_from_df(df)
                    model_type = st.selectbox(
                        "Оберіть модель:", ["SARIMAX", 'OPENAI', "amazon/chronos-t5-large", "amazon/chronos-t5-small", "amazon/chronos-t5-tiny"], index=None)
                    if model_type == "SARIMAX":
                        sarimax = initialize_sarimax_model(data)
                        train_predictions = get_trained_sarimax_predictions(
                            data, sarimax, range=(
                                data['date'].min() + pd.DateOffset(years=2, month=6), data['date'].max())
                        )
                        test_predictions = get_future_sarimax_predicitons(
                            data, sarimax, steps=36)

                        # Step 6: Visualize
                        visualize_predictions(
                            data, train_predictions, test_predictions)
                    if model_type in ["amazon/chronos-t5-large", "amazon/chronos-t5-small", "amazon/chronos-t5-tiny"]:
                        test_predictions = get_chronos_future_predicitons(
                            data, model_name=model_type, months=36)
                        train_predictions = data.copy()
                        train_predictions.columns = ['date', 'mean']

                        # Step 6: Visualize
                        visualize_predictions(
                            data, train_predictions, test_predictions)
                    if model_type == "OPENAI":
                        result_df, explanation = get_openai_future_predicitons(
                            data, data_type, region, product_name, 36)

                        train_predictions = data.copy()
                        train_predictions.columns = ['date', 'mean']

                        test_predictions = result_df

                        with st.chat_message(name='assistant'):
                            visualize_predictions(
                                data, train_predictions, test_predictions)
                            st.write(explanation)


page_names_to_funcs = {
    "Relative Prices": st_show_relative_prices,
    "Buckets Calculating": st_show_buckets_prices,
    "Goods Prices Predictions": st_show_goods_prices_predictions
}

st.set_page_config(layout="wide")  # Streamlit UI
demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
