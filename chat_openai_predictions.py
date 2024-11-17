import pandas as pd
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI


class PricePrediction(BaseModel):
    future_prices: List[float] = Field(
        ..., description="List of forecasted future prices."
    )
    lower_confidence_intervals: List[float] = Field(
        ..., description="List of lower bounds for the confidence intervals of each forecasted price."
    )
    upper_confidence_intervals: List[float] = Field(
        ..., description="List of upper bounds for the confidence intervals of each forecasted price."
    )
    explanation: str = Field(
        ..., description="Textual explanation justifying the forecast."
    )


prompt = HumanMessagePromptTemplate.from_template("""
You are an advanced data analysis and forecasting assistant. You are tasked with analyzing historical data and producing insightful forecasts, considering complex patterns and historical events.

### Provided Information:

1. **Historical Product Prices:**

{dataframe}

2. **Significant Events in Ukraine (Historical Context):**

1992-1994: Economic Turbulence and Hyperinflation  
After gaining independence from the Soviet Union in 1991, Ukraine faced an economic crisis. High inflation, currency devaluation, and unemployment created challenges for the new economy. Hyperinflation reached over 10,000% annually in 1993.

1996: Introduction of the Hryvnia  
The adoption of the hryvnia as the national currency in 1996 stabilized the economy, reducing inflation and fostering investor confidence.

1998: Russian Financial Crisis  
The financial crisis in Russia in 1998 significantly impacted Ukraine's economy due to strong economic ties, decreasing industrial production and slowing growth.

2004: Orange Revolution  
The political shift caused by the Orange Revolution led to temporary economic instability due to reduced foreign investment.

2008-2009: Global Financial Crisis  
The global financial crisis severely impacted Ukraine, reducing GDP by 15% in 2009, devaluing the currency, and requiring an IMF bailout.

2013-2014: Euromaidan Protests and Annexation of Crimea  
The 2014 revolution, the annexation of Crimea, and the conflict in Eastern Ukraine caused significant economic contractions.

2015-2019: Economic Reforms and Recovery  
Under IMF guidance, Ukraine implemented reforms in banking, energy, and anti-corruption, leading to gradual recovery.

2020: COVID-19 Pandemic  
The pandemic caused widespread economic losses, particularly in tourism, retail, and export sectors.

2022: Russian Invasion  
The full-scale invasion in 2022 caused severe economic disruptions, including infrastructure damage, industrial losses, and increased inflation.

2022-2024: Reconstruction and Western Integration  
Despite the ongoing conflict, Ukraine has focused on reconstruction and EU integration, which has increased investor confidence.

---

### Your Task:
- Analyze the historical product price data to identify trends, cycles, anomalies, and patterns. 
- Use the historical context and significant events to provide a nuanced analysis of how they may have influenced price trends.
- Forecast future values for this product considering both historical patterns and potential future scenarios.
- For each forecasted value, provide **lower** and **upper confidence intervals** to indicate the level of uncertainty in your prediction.
- **IMPORTANT:** Avoid generating simple linear forecasts. Instead, analyze the data for seasonality, volatility, and the influence of key events. Use advanced reasoning to provide a complex, realistic projection.
- Predict possible future events or scenarios (e.g., economic shifts, geopolitical changes) and analyze how they could influence the product's future prices.

---

### Output Format:
1. **Forecasted Values:** A list of future product prices based on your analysis.
2. **Confidence Intervals:** Lower and upper bounds for each forecasted value. Confidense interval shoud be 90%.
3. **Reasoning:** Detailed reasoning behind the forecast, explicitly referencing historical data and events, and explaining how they influenced your prediction.
4. **Event Analysis:** Insights into potential future events and their impact on the product's price trends.

Ensure that:
- The forecast reflects realistic and complex patterns rather than straightforward predictions.

Array sizes for future_prices, lower_confidence_intervals, and upper_confidence_intervals should be equal.

**User Query**:
{query}
""")


def get_openai_future_predicitons(data, data_type, region, product_name, months=36):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)
    chain = llm.with_structured_output(PricePrediction)

    query = f"You are working with a dataframe containing '{data_type}' data for {product_name} collected in the {region} region. If 'region' is 'Україна', consider this as data for the entire country.  Forecast the values for the next {months} months."
    response = chain.invoke(
        [prompt.format(dataframe=data.to_string(index=False), query=query)])

    df = pd.DataFrame({
        'date': pd.date_range(start=data['date'].max(), periods=months, freq='ME'),
        'mean': response.future_prices,
        'lower': response.lower_confidence_intervals,
        'upper': response.upper_confidence_intervals
    })

    del llm, chain,  query

    return df, response.explanation
