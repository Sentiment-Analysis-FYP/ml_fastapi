from joblib import load


def load_model():
    model = load('logisticregression.joblib')
    return model
