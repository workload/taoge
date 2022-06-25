# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
from hashlib import md5


def get_result(query,appid,appkey):
    # Set your own appid/appkey.

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'en'
    to_lang =  'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path


    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    # Show response
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    str_all = ''
    for i in result['trans_result']:
        str_all = str_all + i['dst']

    return str_all

if __name__ == '__main__':
    query = 'The need to improve the sustainability of daily mobility in urban areas has been high on the political agenda worldwide. One major concern has been that of the growing car dependency. The growing distance between the activities human carry out has naturally been at the root of such phenomena. Efficient transport systems and high travel speeds have enabled access to ever distant opportunities. On the flip side, such conditions have reduced the need for proximity, which in turn has led to a distancing between human activities and to greater car dependency. For this paper we built a theoretical framework that hypothesises the existence of a negative feedback loop between local and regional accessibility (illustrated above). We then provide initial empirical research into the feedback loop. We explore how high regional accessibility has contributed to losses in local accessibility by enabling concentration of population in local low accessibility environments (one of the two explanatory phenomena behind the negative feedback). Our research uses a 2-step approach to, first, reveal the spatial relationship between local and regional accessibility levels, and then to explore the influence of urban development periods on such relationship. We use a European metropolitan context for this exploratory research (the metropolitan area of Porto), making use of a cross-sectional database on local and regional accessibility levels, supported by longitudinal data on population distribution and building age, both at a high spatial detail level. Local and regional accessibility levels are assessed for 15-min travel distance by foot and by car, respectively. In the absence of longitudinal data on accessibility levels, it was not possible to directly observe the hypothesised feedback cycle. Nevertheless, we found evidence of two necessary, though insufficient, conditions of said cycle. In line with the hypotheses, we found significant amounts of the population living in high regional and low local accessibility contexts (around 17%). We also found evidence of higher concentration of recent urban development in areas offering low local and high regional accessibility levels, in comparison to their high local accessibility counterparts. Indeed, these areas show significant population growth, growing at a faster rate than their high local accessibility counterparts. These findings encourage further research into the hypothesised feedback loop.'
    vl = get_result(query)
    print(vl)