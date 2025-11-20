from db import get_db_connection


# Save scan results to the database
def save_scan_results(file_name, results):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            for result in results:
                sql = """
                INSERT INTO scan_results (file_name, result_type, result_value, classification)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    sql,
                    (
                        file_name,
                        result["type"],
                        result["value"],
                        result["classification"],
                    ),
                )
        connection.commit()
    finally:
        connection.close()


# Retrieve all scan results from the database
def get_all_results():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT file_name, result_type, result_value, classification, created_at FROM scan_results ORDER BY created_at DESC"
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    finally:
        connection.close()


# Retrieve scan results for a specific file from the database
def get_results_by_file(file_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT file_name, result_type, result_value, classification, created_at
            FROM scan_results
            WHERE file_name = %s
            ORDER BY created_at DESC
            """
            cursor.execute(sql, (file_name,))
            results = cursor.fetchall()
            return results
    finally:
        connection.close()


# Delete scan results for a specific file from the database
def delete_scan_results(file_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM scan_results WHERE file_name = %s"
            cursor.execute(sql, (file_name,))
        connection.commit()
    finally:
        connection.close()
