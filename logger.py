import logging, requests, json
from datetime import datetime, date

# Logs the results of the POST. If fails
def log(text, imgname, response):
    logging.basicConfig(filename='logs/' + str(date.today()), level=logging.DEBUG)
    logging.info("Time: " + str(datetime.now()))
    logging.info("Text: " + text)
    logging.info("Image name: " + imgname)
    logging.info("HTTP response code: " + str(response.status_code))
    if response.status_code != requests.codes.ok:
        logging.error("POST didn't go through successfully")
        try:
            logging.info("JSON response: \n" + json.dumps(response.json(), indent=4))
        except(ValueError):
            logging.info("Json response: None")
    logging.info("=========================================================================================")
