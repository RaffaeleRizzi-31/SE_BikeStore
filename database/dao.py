from database.DB_connect import DBConnect
from model.product import Product

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_category():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)

        query = """ SELECT * FROM category """
        cursor.execute(query)

        for row in cursor:
            result[row["id"]] = row["category_name"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(cat):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """ 
                    SELECT 
                        id, product_name, list_price
                    FROM 
                        product
                    WHERE 
                        category_id = %s 
                """
        cursor.execute(query, (cat,))

        for row in cursor:
            result.append(Product(row["id"], row["product_name"], row["list_price"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_pesi(start,end):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)

        query = """ 
                    SELECT 
                        o_i.product_id as id_prod, 
                        COUNT(o_i.product_id) as vendite
                    FROM 
                        `order` as o, 
                        `order_item` as o_i
                    WHERE 
                        o.id = o_i.order_id 
                        AND o.order_date BETWEEN %s AND %s
                    GROUP BY 
                        o_i.product_id
                    ORDER BY 
                        vendite DESC 
                    """
        cursor.execute(query, (start,end,))

        for row in cursor:
            result[row["id_prod"]] = row["vendite"]
        #"2016-01-01 00:00:00"
        #"2018-12-28 00:00:00"
        cursor.close()
        conn.close()
        return result

