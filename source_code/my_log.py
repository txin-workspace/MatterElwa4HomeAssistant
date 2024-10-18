import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s\t%(message)s')

# logging.getLogger('websockets').setLevel(logging.ERROR)

def error(msg):
    logging.error('\033[91m' + msg + '\033[0m')

def warning(msg):
    logging.warning('\033[93m' + msg + '\033[0m')

def info(msg):
    logging.info('\033[92m' + msg + '\033[0m')

def debug(msg):
    logging.debug(msg)

# def print_response(resp):
#     logging.debug('\tresponse_code: {}\
#         \n\tresponse_head: {}\
#         \n\tresponse_text: {}'.format(resp.status_code,resp.headers,resp.text))