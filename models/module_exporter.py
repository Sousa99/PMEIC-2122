import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime
from typing import List, TypedDict

EXPORT_DIRECTORY = '../results/'
EXECUTION_TIMESTAMP = datetime.now()
EXPORT_CSV_EXTENSION = '.csv'
EXPORT_IMAGE_EXTENSION = '.png'

MAIN_DIR = False
CURRENT_MODEL_DIRECTORY = 'TEMP MODEL'

# =================================== PRIVATE FUNCTIONS ===================================

def compute_path(filename: str, extension: str) -> str:

    timestampStr = EXECUTION_TIMESTAMP.strftime("%Y.%m.%d %H.%M.%S")
    if MAIN_DIR: directory_path = os.path.join(EXPORT_DIRECTORY, timestampStr)
    else: directory_path = os.path.join(EXPORT_DIRECTORY, timestampStr, CURRENT_MODEL_DIRECTORY)
    filename_full = filename + extension

    if not os.path.exists(directory_path): os.makedirs(directory_path)
    return os.path.join(directory_path, filename_full)

# =================================== PUBLIC FUNCTIONS ===================================

def change_current_model_directory(model_directory: str):
    global CURRENT_MODEL_DIRECTORY, MAIN_DIR
    CURRENT_MODEL_DIRECTORY = model_directory
    MAIN_DIR = False

def change_to_main_directory():
    global MAIN_DIR
    MAIN_DIR = True

def export_csv(dataframe: pd.DataFrame, filename: str = 'temp', index = True):

    complete_path = compute_path(filename, EXPORT_CSV_EXTENSION)
    dataframe.to_csv(complete_path, index=index)

def export_confusion_matrix(confusion_matrix: np.ndarray, categories: List[str], filename: str = 'temp'):

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)
    y_label = 'True Label'
    x_label = 'Predicted Label'

    plt.figure()
    sns.heatmap(confusion_matrix, annot=True, cmap='Blues', xticklabels=categories, yticklabels=categories)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(complete_path)
    plt.close('all')

ExportMetric = TypedDict("ExportMetric", { 'name': str, 'score': float } )
def export_metrics_bar_graph(metrics: List[ExportMetric], filename: str = 'temp'):

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)
    y_label = 'Score'
    x_label = 'Metrics'

    x_values = []
    y_values = []
    for stat in metrics:
        x_values.append(stat['name'])
        y_values.append(stat['score'])

    plt.figure(figsize=(10, 4))
    bars = sns.barplot(x=x_values, y=y_values)
    bars.bar_label(bars.containers[0], fmt='%.2f')
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.ylim(0, 1)
    plt.savefig(complete_path)
    plt.close('all')