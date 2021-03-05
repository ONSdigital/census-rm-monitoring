import json

from config import Config
from utilities.db_helper import execute_sql_query

if __name__ == "__main__":
    case_to_process_count = 'SELECT COUNT(*) FROM actionv2.case_to_process;'
    case_to_process_count_result = execute_sql_query(case_to_process_count,
                                                     Config.DB_HOST_ACTION, Config.DB_ACTION_CERTIFICATES)
    print(json.dumps({'case_to_process_count': case_to_process_count_result[0][0]}))

    fulfilment_to_process_count = 'SELECT fulfilment_code, COUNT(*) FROM actionv2.fulfilment_to_process ' \
                                  'group by fulfilment_code;'
    fulfilment_to_process_count_result = execute_sql_query(fulfilment_to_process_count,
                                                           Config.DB_HOST_ACTION, Config.DB_ACTION_CERTIFICATES)
    fulfilment_dict = dict(fulfilment_to_process_count_result)
    total_count = sum(fulfilment_dict.values())
    print(json.dumps({'fulfilment_to_process_count': total_count}))
    for fulfilment, count in fulfilment_dict.items():
        print(json.dumps({'fulfilment': fulfilment, 'fulfilment_count': count}))
