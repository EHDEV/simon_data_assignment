
import os
import configparser
from schemas import MarketingEvent
import logging
from .data_validator_transformer import Validator, DataTransformer
import requests
import pandas as pd
import datetime
import utils


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('events_etl.log')

config = configparser.ConfigParser()
config.read('config.ini')

class ExtractTransformCsv(object):

    @property
    def execution_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')

    def __init__(self, event_object, url, destination):
        self.event_object = event_object
        self.url = url
        self.destination = destination

    def download(self):

        file_name = utils._extract_file_name(self.url)
        file_path = os.path.join(self.destination, file_name)

        response = requests.get(self.url)
        with open(file_path, 'w') as file_writer:
            file_writer.write(response.text)

        return file_path

    def validate_and_clean(self, data_df):
        validator = Validator(self.event_object)
        return validator.validate(data_df)


    def enrich_data(self):
        pass

    def summarize(self):
        pass

    def _save_invailid_rows(self, invalid_df):
        if invalid_df.empty:
            logger.debug('No rows were found invalid')
            return

        file_path = os.path.join(
            config['VALIDATION']['invalid_path'],
            config['VALIDATION']['invalid_file_name']
        )
        utils._dataframe_to_csv(invalid_df, file_path)

        logger.debug(f'{invalid_df.shape[0]} invalid rows were found and written to {file_path}')

    

class ValidateFileTask(object):

    @property
    def data_validator(self):
        return Validator(self.data_object)

    def __init__(self, data_object, data_df):
        self.data_object = data_object
        self.data_df = data_df

    def validate(self):
        return self.data_validator.validate(self.data_df)

class EnrichAndSummarizeTask(object):
    pass

class WriteToFileTask(object):
    pass

if __name__ == '__main__':
    data_url = config['CSV_SOURCE']['url']
    event_obj = MarketingEvent()
    pipe = ExtractTransformCsv(event_obj)



    # marketing_obj = Marketing()
    # users_obj = Users()
    # marketing_loader = ExtractCsvLoad(marketing_obj)
    # users_loader = ExtractCsvLoad(users_obj)
    # marketing_loader.load()
    # users_loader.load()

