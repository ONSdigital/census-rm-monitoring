import json

from config import Config
from utilities.db_helper import execute_sql_query

if __name__ == "__main__":
    long_running_query_check = """SELECT pid, age(clock_timestamp(), query_start), usename, query, state 
                               FROM pg_stat_activity
                               WHERE query != '<IDLE>' AND query NOT ILIKE '%pg_stat_activity%'
                               AND query not like 'SET application_name%' AND state != 'idle' 
                               ORDER BY query_start desc;"""
    case_result = execute_sql_query(long_running_query_check)

    action_result = execute_sql_query(long_running_query_check, Config.DB_HOST_ACTION,
                                      Config.DB_ACTION_CERTIFICATES)

    for pid, age, usename, query, state in case_result:
        if age:
            print(json.dumps(
                {'pid': pid, 'age': age.seconds, 'usename': usename, 'query': query, 'DB': 'Case', 'state': state},
                default=str))
        else:
            print(json.dumps({'pid': pid, 'age': age, 'usename': usename, 'query': query, 'DB': 'Case', 'state': state},
                             default=str))

    for pid, age, usename, query, state in action_result:
        if age:
            print(json.dumps(
                {'pid': pid, 'age': age.seconds, 'usename': usename, 'query': query, 'DB': 'Action', 'state': state},
                default=str))
        else:
            print(
                json.dumps({'pid': pid, 'age': age, 'usename': usename, 'query': query, 'DB': 'Action', 'state': state},
                           default=str))
