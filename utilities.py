import streamlit as st
import numpy as np

# Define the logistic regression model coefficients for Graduasi
coefficients_graduasi = {
    '(Intercept)': -1.48335383,
    'P60.1.grouped': 0.227968,
    'P56.1.grouped': -0.220847,
    'P54.grouped': 1.119103,
    'P50': 0.064132,
    'P49': 0.205027,
    'P48': -0.278749,
    'P37_rasio2': -0.06346,
    'P37': 0.0026,
    'P17': 0.29341,
    'P03.grouped': 0.289041,
    'P44_rasio1': -0.173606
}

# Define the logistic regression model coefficients for NPL
coefficients_npl = {
    '(Intercept)': -10.203,
    'dummy.wilayah.1': 0.198,
    'dummy.wilayah.3': 0.265,
    'dummy.wilayah.4': 0.231,
    'dummy.wilayah.5': -0.173,
    'dummy.wilayah.6': -1.929,
    'P05.coded': -0.494,
    'P08': 0.023,
    'P20': 0.152,
    'P26.coded': 0.616,
    'P30': -0.023,
    'P32.1.coded': -0.102,
    'P33.coded': 0.083,
    'P37': -0.000,
    'P48': 0.013,
    'P49': 0.051,
    'P51.coded': 3.395,
    'P54.coded': -1.114,
    'P56.1.coded': 3.790,
    'P56.2': 0.061,
    'P58.1.coded': 0.277,
    'P60.1.coded': 0.047,
    'P68.1.coded': -0.087
}

# Define the logistic and prediction function
def logistic_function(x):
    return 1 / (1 + np.exp(-x))

def predict(features, coefficients):
    intercept = coefficients['(Intercept)']
    logit = intercept
    for feature_name, feature_value in features.items():
        logit += coefficients[feature_name] * feature_value
    probability = logistic_function(logit)
    return probability