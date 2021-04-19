import json

from utilities.db_helper import execute_sql_query


def get_case_receipts():
    sql_query = """
    SELECT CASE counts.region
               WHEN 'E' THEN 'England'
               WHEN 'W' THEN 'Wales'
               WHEN 'N' THEN 'Northern Ireland'
               ELSE 'Unknown Region: ' || counts.region END,
           counts.region_count
    FROM (SELECT LEFT(region, 1) AS region, COUNT(*) AS region_count
          FROM casev2.cases
          WHERE receipt_received = true
          AND action_plan_id = 'c4415287-0e37-447b-9c3d-1a011c9fa3db'
          GROUP BY LEFT(region, 1)) AS counts
        """

    db_result = execute_sql_query(sql_query)

    regional_counts = dict(db_result)
    regional_counts['Total'] = sum(regional_counts.values())
    print(json.dumps(regional_counts))


def get_response_events():
    sql_query = """
    SELECT CASE counts.region
               WHEN 'E' THEN 'England Responses'
               WHEN 'W' THEN 'Wales Responses'
               WHEN 'N' THEN 'Northern Ireland Responses'
               ELSE 'Unknown Region Responses' || counts.region END,
           counts.region_count
    FROM (SELECT LEFT(c.region,1) as region, COUNT(*) AS region_count
          FROM casev2.uac_qid_link q, casev2.cases c
          WHERE q.active = 'f' AND q.caze_case_id = c.case_id
          AND c.action_plan_id = 'c4415287-0e37-447b-9c3d-1a011c9fa3db' GROUP BY LEFT(c.region,1)) AS counts
    """

    db_result = execute_sql_query(sql_query)

    regional_counts = dict(db_result)
    regional_counts['Total Responses'] = sum(regional_counts.values())
    print(json.dumps(regional_counts))


def get_ccs_case_receipts():
    sql_query = """
    SELECT CASE counts.region
               WHEN 'E' THEN 'CCS England'
               WHEN 'W' THEN 'CCS Wales'
               WHEN 'N' THEN 'CCS Northern Ireland'
               ELSE 'CCS Unknown Region: ' || counts.region END,
           counts.region_count
    FROM (SELECT LEFT(region, 1) AS region, COUNT(*) AS region_count
          FROM casev2.cases
          WHERE receipt_received = true
          AND action_plan_id = '38a48608-1c2a-4c2b-b7bc-cb52fcbb4927'
          GROUP BY LEFT(region, 1)) AS counts
        """

    db_result = execute_sql_query(sql_query)

    regional_counts = dict(db_result)
    regional_counts['CCS Total'] = sum(regional_counts.values())
    print(json.dumps(regional_counts))


def get_ccs_response_events():
    sql_query = """
    SELECT CASE counts.region
               WHEN 'E' THEN 'CCS England Responses'
               WHEN 'W' THEN 'CCS Wales Responses'
               WHEN 'N' THEN 'CCS Northern Ireland Responses'
               ELSE 'CCS Unknown Region Responses' || counts.region END,
           counts.region_count
    FROM (SELECT LEFT(c.region,1) as region, COUNT(*) AS region_count
          FROM casev2.uac_qid_link q, casev2.cases c
          WHERE q.active = 'f' AND q.caze_case_id = c.case_id
          AND c.action_plan_id = '38a48608-1c2a-4c2b-b7bc-cb52fcbb4927' GROUP BY LEFT(c.region,1)) AS counts
    """

    db_result = execute_sql_query(sql_query)

    regional_counts = dict(db_result)
    regional_counts['CCS Total Responses'] = sum(regional_counts.values())
    print(json.dumps(regional_counts))


if __name__ == "__main__":
    get_case_receipts()
    get_response_events()
    get_ccs_case_receipts()
    get_ccs_response_events()
