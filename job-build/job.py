import fml_manager
import json
import time
import os
import argparse

manager = fml_manager.FMLManager()


def run_job(job_dsl, config_data):
    response = manager.submit_job(job_dsl, config_data)
    manager.prettify(response, True)
    stdout = json.loads(response.content)
    print(stdout)
    jobid = stdout["jobId"]
    query_condition = {
        "job_id": jobid
    }
    job_status = manager.query_job(query_condition)
    manager.prettify(job_status, True)

    for i in range(500):
        time.sleep(1)
        job_detail = manager.query_job(query_condition).json()
        final_status = job_detail["data"][0]["f_status"]
        print(final_status)

        if final_status == "failed":
            print("Failed")
            break
        if final_status == "success":
            print("Success")
            break

        # r
        # esponse = manager.fetch_job_log_new(jobid)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("dsl", type=str, help="please input dsl")
    arg_parser.add_argument("config", type=str, help="please input config")
    args = arg_parser.parse_args()
    print(args)
    dsl = json.loads(args.dsl)
    config = json.loads(args.config)

    run_job(args.dsl, args.config)
    exit(0)
