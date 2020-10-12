import pandas as pd
import os
import datetime

def _dataframe_to_csv(df, file_name, path_or_directory):
    if not os.path.exists(path_or_directory):
        os.makedirs(path_or_directory)

    full_name = os.path.join(file_name, path_or_directory)

    df.to_csv(full_name, index=False, sep=',')


def _read_csv_into_dataframe(file_path, data_types, **kwargs):
    '''
     Reads a csv file into a dataframe
    :param file_path:
    :param kwargs:
    :return:
    '''
    data_df = pd.read_csv(
        file_path,
        sep=kwargs.get('sep') or ',',
        dtype=data_types,
        index_col=kwargs['index_col'] or False
    )
    return data_df


def _extract_file_name(path_or_url):
    if not path_or_url:
        raise TypeError('path_or_url is empty')
    return path_or_url.split('/')[-1]
