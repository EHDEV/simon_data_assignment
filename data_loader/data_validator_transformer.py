import re
import datetime

class Validator(object):

    invalid_row_indexes = list()

    def __init__(self, data_object):
        self.data_object = data_object

    def _validate_col_values_regex(self, val, pattern):
        return True if re.match(pattern, str(val)) else False

    def _check_categories(self, val, categories):
        return val in categories

    def _check_for_null_rows(self, raw_df, column):
        null_idxs = raw_df[raw_df[column].isnull()].index.tolist()
        return null_idxs

    def _split_data_to_valid_invalid(self, df):
        invalid_row_idxs = list(set(self.invalid_row_indexes))
        invalid_df = df.iloc[invalid_row_idxs]
        valid_df = df.drop(index=invalid_row_idxs)
        return valid_df, invalid_df

    def _dedup(self, df):
        return df.drop_duplicates()

    def validate(self, raw_df):
        """
         Performs validation on data frame and columns using the methods above
        :param raw_df:
        :return: valid and invalid data
        """
        raw_df = self._dedup(raw_df)

        for col_pat in self.data_object.column_patterns:
            raw_df['is_valid'] = raw_df[col_pat['name']].apply(
                self._validate_col_values_regex,
                pattern=col_pat['pattern']
            )

            invalid_rows = raw_df.where(raw_df.is_valid).dropna().astype('int64').values.tolist()
            self.invalid_row_indexes += invalid_rows

            valid_df, invalid_df = self._split_data_to_valid_invalid(raw_df)

        return valid_df, invalid_df

class DataTransformer(object):
    def __init__(self, data_object):
        self.data_object = data_object

    def extract_domain(self, s):
        return s.split('@')[-1]

    def timestamp_to_datetime(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp)

    def transform(self, data_df):
        pass
