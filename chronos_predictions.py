from chronos import ChronosPipeline
import numpy as np
import pandas as pd
import torch


def get_chronos_future_predicitons(data, months=36, model_name="amazon/chronos-t5-large"):
    pipeline = ChronosPipeline.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
    )

    forecast = pipeline.predict(
        context=torch.tensor(data['price']),
        prediction_length=36,
        num_samples=48
    )

    low, median, high = np.quantile(
        forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)

    df = pd.DataFrame({
        'date': pd.date_range(start=data['date'].max(), periods=months, freq='ME'),
        'mean': median,
        'lower': low,
        'upper': high
    })

    return df
