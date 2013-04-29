# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2012 BigML
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import json
import requests

HTTP_OK = 200

TWITTER_URL = "http://search.twitter.com/search.json"

def main(text='', output=sys.stdout):
    tweets = []
    payload = {
        'q': text,
        'rpp': 50,
        'include_entities': 'true'}

    url = TWITTER_URL
    response = requests.get(url, params=payload)
    if response.status_code == HTTP_OK:
        content = json.loads(response.content)
        tweets = tweets + content['results']
        while 'next_page' in content:
            response = requests.get(url + content['next_page'])
            if response.status_code == HTTP_OK:
                content = json.loads(response.content)
                tweets = tweets + content['results']
            else:
                break
    output.write(json.dumps({"results": tweets}))
    output.flush()


if __name__ == '__main__':
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped: break
        main(line)
