import os
import sys
import math
import matplotlib

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime
from typing import Dict, List, Optional, Tuple
if sys.version_info[0] == 3 and sys.version_info[1] >= 8: from typing import TypedDict
else: from typing_extensions import TypedDict

EXPORT_DIRECTORY = '../results/'
EXECUTION_TIMESTAMP = datetime.now()
EXPORT_CSV_EXTENSION = '.csv'
EXPORT_IMAGE_EXTENSION = '.png'

CURRENT_DIRECTORIES = []

matplotlib.use('Agg')

# =================================== PRIVATE FUNCTIONS ===================================

def compute_path(filename: str, extension: str) -> str:

    timestampStr = EXECUTION_TIMESTAMP.strftime("%Y.%m.%d %H.%M.%S")
    directory_path = os.path.join(EXPORT_DIRECTORY, timestampStr, *CURRENT_DIRECTORIES)
    filename_full = filename + extension

    if not os.path.exists(directory_path): os.makedirs(directory_path)
    return os.path.join(directory_path, filename_full)

def optimal_grid(number: int) -> Tuple[int, int]:

    square_root = math.sqrt(number)
    square_root_floor = math.floor(square_root)

    rows = square_root_floor - 1
    if rows <= 0: rows = 1

    columns = math.ceil(number / rows)
    return (rows, columns)

# =================================== PUBLIC FUNCTIONS - CHANGE GLOBAL PARAMETERS ===================================

def change_current_directory(current_directories: List[str] = []):
    global CURRENT_DIRECTORIES
    CURRENT_DIRECTORIES = current_directories

# =================================== PUBLIC FUNCTIONS - SPECIFIC PARAMETERS ===================================

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
def export_metrics_bar_graph(metrics: List[ExportMetric], filename: str = 'temp') -> None:

    x_values = []
    y_values = []
    for stat in metrics:
        x_values.append(stat['name'])
        y_values.append(stat['score'])

    bar_chart(filename, x_values, y_values, x_label='Metrics', y_label='Score', y_lim=(0, 1))

# =================================== PUBLIC FUNCTIONS - GENERAL METHODS ===================================

def bar_chart(filename: str, x_values: List[str], y_values: List[int], figsize: Tuple[int] = (10, 4),
    label_bars: bool = True, x_label: Optional[str] = None, y_label: Optional[str] = None,
    x_rot: Optional[float] = None, y_rot: Optional[float] = None, margins: Optional[Dict[str, Optional[float]]] = None,
    x_lim: Optional[Tuple[float, float]] = None, y_lim: Optional[Tuple[float, float]] = None) -> None:

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)

    plt.figure(figsize=figsize)
    bars = sns.barplot(x=x_values, y=y_values)
    
    # FIXME: Find backwards compatible way of calling this (python 3.6)
    #if label_bars: bars.bar_label(bars.containers[0], fmt='%.2f')

    if x_label: plt.xlabel(x_label)
    if y_label: plt.ylabel(y_label)
    
    if x_lim: plt.xlim(x_lim[0], x_lim[1])
    if y_lim: plt.ylim(y_lim[0], y_lim[1])

    if x_rot: plt.xticks(rotation=x_rot)
    if y_rot: plt.yticks(rotation=y_rot)

    if margins: plt.subplots_adjust(bottom=margins['bottom'], left=margins['left'],
        top=margins['top'], right=margins['right'])

    plt.savefig(complete_path)
    plt.close('all')

def boxplot_for_each(filename: str, dataframe: pd.DataFrame, variables: List[str], hue: Optional[str] = None) -> None:

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)

    rows, cols = optimal_grid(len(variables))
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5), squeeze=False)

    for variable_index, variable_key in enumerate(variables):

        col_index = variable_index % cols
        row_index = variable_index // cols

        sns.boxplot(data=dataframe, x=hue, y=variable_key, ax=axs[row_index, col_index])

    plt.savefig(complete_path)
    plt.close('all')

def histogram_for_each_numeric(filename: str, dataframe: pd.DataFrame, variables: List[str], hue: Optional[str] = None, kde: bool = True) -> None:

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)

    rows, cols = optimal_grid(len(variables))
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5), squeeze=False)

    for variable_index, variable_key in enumerate(variables):

        col_index = variable_index % cols
        row_index = variable_index // cols

        sns.histplot(data=dataframe, x=variable_key, hue=hue, kde=kde, ax=axs[row_index, col_index])

    plt.savefig(complete_path)
    plt.close('all')

def histogram_for_each_symbolic(filename: str, dataframe: pd.DataFrame, variables: List[str], hue: Optional[str] = None, kde: bool = True) -> None:

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)

    rows, cols = optimal_grid(len(variables))
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 5, rows * 5), squeeze=False)

    for variable_index, variable_key in enumerate(variables):

        row_index = variable_index // cols
        col_index = variable_index % cols

        sns.countplot(data=dataframe, x=variable_key, hue=hue, ax=axs[row_index, col_index])
        axs[row_index, col_index].set_title("'{0}'".format(variable_key))

    plt.savefig(complete_path)
    plt.close('all')

def dataframe_all_variables_sparsity(filename: str, dataframe: pd.DataFrame, variables: List[str], hue: Optional[str] = None) -> None:

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)
    
    number_variables = len(variables)
    rows, cols = number_variables - 1, number_variables - 1
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2.6, rows * 2.6))

    for var1_index in range(number_variables):
        var1 = variables[var1_index]

        for var2_index in range(var1_index + 1, number_variables):
            var2 = variables[var2_index]

            sns.scatterplot(data=dataframe, x=var1, y=var2, hue=hue, ax=axs[var1_index, var2_index])
            axs[var1_index, var2_index].set_title("%s x %s"%(var1, var2))
            axs[var1_index, var2_index].set_xlabel(var1)
            axs[var1_index, var2_index].set_ylabel(var2)

    plt.tight_layout()
    plt.savefig(complete_path)
    plt.close('all')

def heatmap(filename: str, dataframe: pd.DataFrame, figsize: Tuple[int] = (6, 6),
    annot: bool = True, cmap: str = 'Blues', margins: Optional[Dict[str, Optional[float]]] = None,
    x_ticklabels: Optional[List[str]] = False, y_ticklabels: Optional[List[str]] = False) -> None:

    complete_path = compute_path(filename, EXPORT_IMAGE_EXTENSION)

    plt.figure(figsize=(figsize[0] + dataframe.shape[0] * 0.5, figsize[1] + dataframe.shape[1] * 0.5))
    sns.heatmap(abs(dataframe), xticklabels=x_ticklabels, yticklabels=y_ticklabels, annot=annot, cmap=cmap)

    if margins: plt.subplots_adjust(bottom=margins['bottom'], left=margins['left'],
        top=margins['top'], right=margins['right'])
    
    plt.savefig(complete_path)
    plt.close('all')