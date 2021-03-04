import pandas as pd
import datetime
import pmdarima as pm
from statsmodels.tsa.seasonal import seasonal_decompose
from functools import reduce

def increment_wod(x):
    """Increment week of the day"""
    if x < 6:
        x = x + 1
    elif x == 6:
        x = 0
    return x


def count_days(start, n, exclude_wod=[5, 6]):
    """" Count number of days which contains n business days """
    k = 0
    while n > 0:
        start = increment_wod(start)
        if not start in exclude_wod:
            n = n - 1
        k = k + 1
    return k


def extend_wod(xreg, n, col='dow', exclude_wod=None):
    """Return a pd dataframe. Wrapper of pandas date_range. Exclude days with values in the variable exclude_wod"""
    last_val = xreg.index.max()
    if exclude_wod is None:
        k = n
    else:
        k = count_days(last_val.weekday(), n=n, exclude_wod=exclude_wod)

    idx = pd.date_range(last_val + datetime.timedelta(days=1), last_val + datetime.timedelta(days=k))
    res = pd.DataFrame(idx.to_series().dt.dayofweek, columns=[col])

    if not exclude_wod is None:
        res = res[~res[col].isin(exclude_wod)]  # you should extend to multivariate case

    return res


def deco_series(x, period=20, model='additive'):
    """
    Decompose series x in trend season and residual. Return the decomposed series
    :param x: pandas series
    :param period: period in every season
    :param model: how to decompose series. additive by default
    :return: decomposed series
    """
    # check for missing values
    x = x.dropna(axis='index', how='any')

    obj_dec = seasonal_decompose(x, model=model, period=period)
    list_df = [obj_dec.seasonal, obj_dec.trend, obj_dec.resid]
    df_dec = reduce(lambda x, y: pd.merge(x, y, on=['Date']), list_df)
    df_dec = df_dec.dropna(how="any", axis=0)

    # set name attribute
    df_dec.name = x.name

    return df_dec


def compare_seasonality(x, periods=[5], model='additive', save_dec=False):
    """ return a dict of the decomposed series, wrapper of seasonal_decompose
    :param x: pandas series of time series
    :param periods: parameter to seasonal decompose
    :param model: model of time series decomposition
    :param save_dec: if True, will save the plots in a folder named img_dec
    :return: a dictionary, key is the period, value is the corresponding dec series
    """
    dict_dec_series = {}
    for period in periods:
        dec_series = seasonal_decompose(x, model=model, period=period)
        dict_dec_series[period] = dec_series
        if save_dec:
            fname = 'img_dec/' + x.name + str(period) + '.jpeg'
            dec_series.plot().savefig(fname)

    return dict_dec_series


def auto_ARIMA(x, n, m=20):
    """ wrapper of pdmarima auto_arima"""
    # best ARIMA model
    best_fit = pm.auto_arima(x, m=m)

    # prediction nstep ahead
    pred = best_fit.predict(n)

    res = {
        'best_fit': best_fit,
        'pred': pred
    }
    return res


def auto_ARIMAX(x, n, xreg, future_xreg, m=20):
    """wrapper of pdmarima auto_arimaX. Use it with xreg regressors"""
    # best fit
    best_fit = pm.auto_arima(x, m=m, X=pd.DataFrame(xreg))
    # prediction n step ahead
    pred = best_fit.predict(n, future_xreg)

    res = {
        'best_fit': best_fit,
        'pred': pred
    }

    return res


def forecast_stock(x, n, xreg=None):
    """ n period Forecast of series x using autoarima\n Xreg is expected to be a pandas Series """
    # drop rows with NA
    x = x.dropna(axis='index', how='any')

    # modify xreg is x has some NA
    if not xreg is None:
        if xreg.size != x.size:
            df_x = pd.DataFrame(x)
            df_xreg = pd.DataFrame(data=xreg)
            df_xreg = df_x.merge(df_xreg, 'left', on='Date')
            xreg = df_xreg[xreg.name]

    # best ARIMA/ARIMAX fit and prediction prediction
    res = auto_ARIMA(x, n) if xreg is None else auto_ARIMAX(x, n, xreg, future_xreg=extend_wod(xreg, n, exclude_wod=[5, 6]))

    # reconstruct dataframe
    date_col = pd.date_range(x.index.max() + datetime.timedelta(days=1), x.index.max() + datetime.timedelta(days=n))
    pred_df = pd.DataFrame(res['pred'], columns=[x.name])
    pred_df = pred_df.set_index(date_col)

    # distinguish observed vs forecast
    pred_df['type_obs'] = "forecast"

    fcst_x = pd.DataFrame(x)
    fcst_x['type_obs'] = "observed"
    fcst_x = fcst_x.append(pred_df)
    fcst_x.index.names = ['Date']

    res = {
        "df": fcst_x,
        "best_fit": res['best_fit']
    }
    return res
