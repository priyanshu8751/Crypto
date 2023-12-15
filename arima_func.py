from statsmodels.tsa.arima.model import ARIMA

def data_process(data):
    # extra_days = data[:]
    df_for_training = data[:]
    # true = [i for i in extra_days["close"]]
    history = [i for i in df_for_training["close"]]
    return history

def predict(history):
    predictions = []
    for t in range(1):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit()
        output = model_fit.forecast()
        # print(output)
        yhat = output[0]
        print(yhat)
        predictions.append(yhat)
        # obs = true[t]
        # print("obs: ",obs)
        # history.append(obs)
    return predictions[0]