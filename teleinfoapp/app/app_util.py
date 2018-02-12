from datetime import datetime, timedelta

'''
return passed date formatted for URL like this '2018-01-28+15%3A17%3A51'
'''
def deltaminute2(min):
    date = datetime.now() - timedelta(minutes=min)
    out = date.strftime("%Y-%m-%d+%H%%3A%M%%3A%S")
    return out

'''
return URL like this 
'/teleinfophaseschartview/chart/0?_flt_1_timestamp=2018-01-28+15%3A17%3A51'
'''
def get_url2(min, klass):
    return '/' + klass + '/chart/0?_flt_1_timestamp=' + deltaminute2(min)

