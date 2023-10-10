import logging
from state import pair_state

deal_state_log = logging.getLogger('DEAL LOGS')
deal_state_log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler('deal_state_log.log')
handler.setFormatter(formatter)
deal_state_log.addHandler(handler)


def deal_starts_log(pair_info):
    deal_state_log.info(f'DEAL STARTS : {pair_info}')


def deal_finished_log(pair_info):
    deal_state_log.info(f'DEAL STARTS : {pair_info}')

