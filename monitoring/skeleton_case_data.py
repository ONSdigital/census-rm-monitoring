import json

from utilities.db_helper import execute_sql_query


def get_skeleton_case_data():
    sql_query = """
        SELECT COUNT(*) As TotalCases,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               LEFT(region, 1) AS region, case_type
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL
        GROUP BY  LEFT(region, 1), case_type

        UNION ALL

        SELECT COUNT(*) As TotalCases ,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               'All Regions', case_type
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL
        GROUP BY case_type

        UNION ALL

        SELECT COUNT(*) As TotalCases ,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               LEFT(region, 1), 'All Cases'
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL
        GROUP BY LEFT(region, 1)

        UNION ALL

        SELECT COUNT(*) As TotalCases ,
               AVG(DATE_PART('day', NOW()::timestamp - created_date_time::timestamp))::integer As average_days_old,
               'All regions', 'All Cases'
        FROM casev2.cases
        WHERE skeleton = 't'
        AND address_invalid = 'f'
        AND receipt_received = 'f'
        AND refusal_received IS NULL;
        """

    db_result = execute_sql_query(sql_query)

    for result in db_result:
        count, average_case_age, region, case_type = result
        print(json.dumps({'skeleton_case_count': count, 'average_case_age': average_case_age, 'region': region,
                          'case_type': case_type}))


if __name__ == "__main__":
    get_skeleton_case_data()
