#
#  Copyright 2020 The KubeFATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#
import json
import os
import tarfile
import requests


class FMLManager:
    def __init__(self, ):

        fateflow_uri = os.getenv('FateFlowServer')
        self.server_url = "http://{}/{}".format(fateflow_uri, "v1")

    def submit_job(self, dsl, config):
        post_data = {'job_dsl': dsl,
                     'job_runtime_conf': config}
        response = requests.post(
            "/".join([self.server_url, "job", "submit"]), json=post_data)

        return self.prettify(response)

    def query_job(self, query_conditions):
        response = requests.post(
            "/".join([self.server_url, "job", "query"]), json=query_conditions)
        return self.prettify(response)

    def stop_job(self, job_id):
        post_data = {
            'job_id': job_id
        }
        response = requests.post(
            "/".join([self.server_url, "job", "stop"]), json=post_data)
        return self.prettify(response)

    def prettify(self, response, verbose=False):
        if verbose:
            if isinstance(response, requests.Response):
                if response.status_code == 200:
                    print("Success!")
                print(json.dumps(response.json(), indent=4, ensure_ascii=False))
            else:
                print(response)

        return response
