import configparser
config = configparser.ConfigParser()
config.read('config.ini')


class MarketingEvent(object):
    column_patterns = [
        {
            'name': 'event_id',
            'pattern': '^[a-zA-Z0-9]{32}$'},
        {
            'name': 'ip_address',
            'pattern': '[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+'},
        {
            'name': 'email',
            'pattern': '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[\-_]?\w+[.]\w{2,3}$'}
    ]

    data_types = {
        'timestamp': 'int64',
        'event_id': 'object',
        'email': 'object',
        'action': 'object',
        'campaign_id': 'int64',
        'ip_address': 'object',
        'url': 'object',
        'user_agent': 'object'
    }

    action_column_categories = [
        'delivered', 'open', 'click'
    ]

    new_metrics = [
        'total_delivered', 'total_opened', 'total_clicked', 'open_rate', 'click_rate'
    ]

    summary_columns = [

    ]