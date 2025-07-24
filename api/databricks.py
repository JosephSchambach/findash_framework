import requests
import time

class DataBricksContext:
    def __init__(self, token, endpoint, logger, database):
        self.logger = logger
        self.database = database
        self.__endpoint = endpoint
        self.__token = token
        self.__url = f"https://{self.__endpoint}/api/2.1"
        self.logger.log("Initialized DataBricksContext")
        
    def _get_run_status(self, run_id):
        headers = {
            "Authorization": f"Bearer {self.__token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.__url}/jobs/runs/get?run_id={run_id}", headers=headers)
        if response.status_code == 200:
            jsn = response.json()
            return jsn.get("state", {}).get("life_cycle_state", "UNKNOWN")
        else:
            self.logger.log(f"Failed to retrieve run {run_id} status: {response.text}")
        return None

    def send_job(self, args, attribute):
        job = getattr(args, attribute)
        self.logger.log(f"Sending job with ID: {job.job_id}")
        headers = {
            "Authorization": f"Bearer {self.__token}",
            "Content-Type": "application/json"
        }
        payload = {
            "job_id": job.job_id
        }
        response = requests.post(f"{self.__url}/jobs/run-now", headers=headers, json=payload)
        if response.status_code == 200:
            self.logger.log(f"Job {job.job_id} sent successfully")
        else:
            self.logger.log(f"Failed to send job {job.job_id}: {response.text}")
        run_id = response.json().get("run_id")
        state = self._get_run_status(run_id)
        while state not in ["TERMINATED", "SKIPPED", "INTERNAL_ERROR"]:
            self.logger.log(f"Waiting for job {job.job_id} to complete. Current state: {state}")
            time.sleep(10)
            state = self._get_run_status(run_id)
        if state == "TERMINATED":
            self.logger.log(f"Job {job.job_id} completed successfully")