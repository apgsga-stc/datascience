from fbprophet import Prophet
import pandas as pd

COMPLETLE_COLUMN_LIST = [
    "ds",
    "trend",
    "yhat_lower",
    "yhat_upper",
    "trend_lower",
    "trend_upper",
    "additive_terms",
    "additive_terms_lower",
    "additive_terms_upper",
    "daily",
    "daily_lower",
    "daily_upper",
    "weekly",
    "weekly_lower",
    "weekly_upper",
    "yearly",
    "yearly_lower",
    "yearly_upper",
    "multiplicative_terms",
    "multiplicative_terms_lower",
    "multiplicative_terms_upper",
    "yhat",
    "y",
    "trend_changepoint",
]


def create_prophet_dataframe(agg_temperatur_df: pd.DataFrame, ds:str, y:str,yearly=True,weekly=True, daily=True)->pd.DataFrame:

    prophet_df = agg_temperatur_df.loc[:, [ds, y]].rename(
        columns={ds: "ds", y: "y"}
    )

    model = Prophet(
        growth="linear",
        changepoints=None,
        n_changepoints=25,
        changepoint_range=0.8,
        yearly_seasonality=yearly,
        weekly_seasonality=weekly,
        daily_seasonality=daily,
        holidays=None,
        seasonality_mode="additive",
        seasonality_prior_scale=10.0,
        holidays_prior_scale=10.0,
        changepoint_prior_scale=0.05,
        mcmc_samples=0,
        interval_width=0.8,
        uncertainty_samples=1000,
        stan_backend=None,
    )
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=14)

    forecast = model.predict(future)

    forecast = pd.merge(forecast, prophet_df, left_on="ds", right_on="ds", how="left")

    change_points_df = forecast.loc[:, ["ds", "trend"]]
    change_points_df.loc[:, "tangent"] = (forecast.trend - forecast.trend.shift(1)).round(5)

    _grp_ = change_points_df.groupby("tangent")

    change_points_df = pd.DataFrame(
        dict(ds_changepoint=_grp_.ds.last(), trend_changepoint=_grp_.trend.last())
    ).reset_index()

    forecast = pd.merge(
        forecast,
        change_points_df.drop(columns="tangent"),
        left_on="ds",
        right_on="ds_changepoint",
        how="left",
    ).drop(columns="ds_changepoint")
    
    for x in COMPLETLE_COLUMN_LIST:
        if x not in forecast.columns:
            forecast[x]= 0
    
    return forecast