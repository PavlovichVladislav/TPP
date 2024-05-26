from scipy.optimize import curve_fit

from utils.regression_model import model


# Функция для построения модели, которой описывается график ХОП
def calc_boiler_hop_model(boiler_hop, inversion=False):
    # Используем curve_fit для подбора параметров регрессии
    params = None
    covariance = None

    # (if) Иногда нужна модель, когда мы ищем Q через b, например для хоп котельного цеха
    # (else) В других слуаях, нам нужно найти через Q точку b, например в ХОП станции
    if (inversion):
        params, covariance = curve_fit(model, boiler_hop['Q'], boiler_hop['b'])
    else:
        params, covariance = curve_fit(model, boiler_hop['b'], boiler_hop['Q'])

    return params
