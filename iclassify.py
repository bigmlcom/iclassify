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

import os
import sys
import operator
import json
import requests

HTTP_OK = 200

try:
   UCLASSIFY_READKEY = os.environ['UCLASSIFY_READKEY']
except KeyError:
   sys.exit("Cannot find UCLASSIFY_READKEY in your environment")

UCLASSIFY_URL = 'http://uclassify.com/browse/'

UCLASSIFY_CLASSIFIERS = [
    {'name': 'gender',
     'service': 'uClassify/GenderAnalyzer_v5/ClassifyText',
     'version': '1.01'},
    {'name': 'language',
     'service': 'uClassify/Text%20Language/ClassifyText',
     'version': '1.01'},
    {'name': 'sentiment',
     'service': 'uClassify/Sentiment/ClassifyText',
     'version': '1.01'},
    {'name': 'topic',
     'service': 'uClassify/Topics/ClassifyText',
     'version': '1.01'},
    {'name': 'mood',
     'service': 'prfekt/Mood/ClassifyText',
     'version': '1.01'},
    {'name': 'age',
     'service': 'uClassify/Ageanalyzer/ClassifyText',
     'version': '1.01'},
    {'name': 'tonality',
     'service': 'prfekt/Tonality/ClassifyText',
     'version': '1.01'},
    ]

def main(text='', output=sys.stdout):
    top_classes = []
    for classifier in UCLASSIFY_CLASSIFIERS:
        payload = {
            'readkey': UCLASSIFY_READKEY,
            'text': text,
            'version': classifier['version'],
            'output': 'json'}
        url = UCLASSIFY_URL + classifier['service']
        response = requests.get(url, params=payload)
        top_class = '-'
        if response.status_code == HTTP_OK:
            content = json.loads(response.content)
            if content['success']:
                top_class = max(content['cls1'].iteritems(), key=operator.itemgetter(1))[0]
        top_classes.append(top_class)
    output.write("%s,%s\n" % (text.strip(), ','.join(top_classes).encode("utf-8")))
    output.flush()

if __name__ == '__main__':
    for line in sys.stdin:
        stripped = line.strip()
        if not stripped: break
        main(line)
