from database.DB_connect import DBConnect
from model.andamentoProdotti import AndamentoProdotti
from model.prodByStore import ProdByStore
from model.prodotti import Prodotti
from model.negozi import Negozi
from model.andamentoNegozio import AndamentoNegozio


class DAO:
    @staticmethod
    def date_transiction():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select YEAR(ss.`date`) as yy, month(ss.`date`) as mm
                    from toysales.sales ss
                    group by YEAR(ss.`date`), month(ss.`date`) """

        cursor.execute(query)

        for row in cursor:
            result.append((row["yy"], row["mm"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def all_products():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM toysales.products p ORDER BY p.product_category"

        cursor.execute(query, ())

        for row in cursor:
            result.append(Prodotti(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def all_stores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM toysales.stores s ORDER BY s.store_location"

        cursor.execute(query, ())

        for row in cursor:
            result.append(Negozi(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def andamento_prodotti(loc, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select month(ss.`date`) as mm, p.product_name as Pname,  p.product_category as category,
                sum(ss.units) as qty, (p.product_price*sum(ss.units)) as revenue, (p.product_cost*sum(ss.units)) as cv
            from toysales.sales ss, toysales.stores s , toysales.products p 
            where s.store_location=%s and year(ss.`date`)=%s and ss.store_ID =s.store_ID and ss.product_ID =p.product_ID 
            group by month(ss.`date`), p.product_name
            order by month(ss.`date`), p.product_category """

        cursor.execute(query, (loc, anno,))

        for row in cursor:
            result.append(AndamentoProdotti(row["mm"], row["Pname"], row["category"], row["qty"], row["revenue"], row["cv"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def prod_by_store(loc, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.product_name as Pname, s.store_name as Sname, i.stock_on_hand as stock, 
                sum(ss.units) as qty, (p.product_price* sum(ss.units)) as revenue, (p.product_cost * sum(ss.units)) as cv
            from toysales.stores s, toysales.sales ss, toysales.products p, toysales.inventory i 
            where s.store_ID=ss.store_ID and p.product_ID=ss.product_ID and i.store_ID =s.store_ID 
                and i.product_ID =p.product_ID and s.store_location =%s and year(ss.`date`)=%s
            group by p.product_name, s.store_name
            order by s.store_name"""

        cursor.execute(query, (loc, anno,))

        for row in cursor:
            result.append(ProdByStore(row["Pname"], row["Sname"], row["stock"], row["qty"], row["revenue"], row["cv"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def andamento_negozio(shop, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select month(ss.`date`) as mm, p.product_name as Pname, sum(ss.units) as qty, 
                (p.product_price*sum(ss.units)) as revenue, (p.product_cost*sum(ss.units)) as cv
            from toysales.sales ss, toysales.stores s , toysales.products p 
            where ss.store_ID =s.store_ID and ss.product_ID =p.product_ID and s.store_name=%s and year(ss.`date`)=%s
            group by month(ss.`date`), p.product_name
            order by month(ss.`date`)"""

        cursor.execute(query, (shop, anno,))

        for row in cursor:
            result.append(AndamentoNegozio(row["mm"], row["Pname"], row["qty"], row["revenue"], row["cv"]))

        cursor.close()
        conn.close()

        return result
