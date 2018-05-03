"""
Module to parse timeseries
"""

def endpoints(dataframe, break_label, column=1):
    """Return the timeseries pandas dataframe with parsed endpoints.
       In practice, this allows you to ignore the beginning and end of the day.
       All timeseries from beginning and end which match the given "break_label"
       in the given column are removed.
    """
    vals = dataframe[column].values
    index_begin = 0
    index = 0
    label = break_label
    while (index < len(vals)) and (label == break_label):
        label = vals[index]
        index_begin = index
        index += 1
    index = len(vals) - 1
    label = break_label
    while (index >= 0) and (label == break_label):
        label = vals[index]
        index_end = index
        index -= 1
    return dataframe[index_begin:index_end]
