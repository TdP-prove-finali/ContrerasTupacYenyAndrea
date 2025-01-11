from database.DB_connect import DBConnect
from model.andamentoProdotti import AndamentoProdotti
from model.prodByStore import ProdByStore
from model.prodotti import Prodotti
from model.negozi import Negozi
from model.andamentoNegozio import AndamentoNegozio

class DAO():
    @staticmethod
    def YYeMM():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select YEAR(ss.`Date`) as yy, month(ss.`Date`) as mm
                    from toysales.sales ss
                    group by YEAR(ss.`Date`), month(ss.`Date`) """

        cursor.execute(query)

        for row in cursor:
            result.append((row["yy"], row["mm"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def AllProducts():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM toysales.products p ORDER BY p.Product_Category"

        cursor.execute(query, ())

        for row in cursor:
            result.append(Prodotti(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def AllStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM toysales.stores s ORDER BY s.Store_Location"

        cursor.execute(query, ())

        for row in cursor:
            result.append(Negozi(**row))

        cursor.close()
        conn.close()

        return result


    @staticmethod
    def andamentoProdotti(loc, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select month(ss.`Date`) as mm, p.Product_Name as Pname,  p.Product_Category as category,sum(ss.Units) as qty, (p.Product_Price*sum(ss.Units)) as revenue, (p.Product_Cost*sum(ss.Units)) as cv
                        from toysales.sales ss, toysales.stores s , toysales.products p 
                        where  s.Store_Location=%s and year(ss.`Date`)=%s and ss.Store_ID =s.Store_ID and ss.Product_ID =p.Product_ID 
                        group by month(ss.`Date`), p.Product_Name
                        order by month(ss.`Date`), p.Product_Category """

        cursor.execute(query, (loc, anno,))

        for row in cursor:
            result.append(AndamentoProdotti(row["mm"], row["Pname"], row["category"], row["qty"], row["revenue"], row["cv"]))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def prodByStore(loc, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.Product_Name as Pname, s.Store_Name as Sname, i.Stock_On_Hand as stock, sum(ss.Units) as qty, (p.Product_Price* sum(ss.Units)) as revenue, (p.Product_Cost * sum(ss.Units)) as cv
                    from toysales.stores s, toysales.sales ss, toysales.products p, toysales.inventory i 
                    where s.Store_ID=ss.Store_ID and p.Product_ID=ss.Product_ID and i.Store_ID =s.Store_ID and i.Product_ID =p.Product_ID and s.Store_Location =%s and year(ss.`Date`)=%s
                    group by p.Product_Name, s.Store_Name
                    order by s.Store_Name"""

        cursor.execute(query, (loc, anno,))

        for row in cursor:
            result.append(ProdByStore(row["Pname"], row["Sname"], row["stock"], row["qty"], row["revenue"], row["cv"]))

        cursor.close()
        conn.close()

        return result


    @staticmethod
    def andamentoNegozio(shop, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select month(ss.`Date`) as mm, p.Product_Name as Pname, sum(ss.Units) as qty, (p.Product_Price*sum(ss.Units)) as revenue, (p.Product_Cost*sum(ss.Units)) as cv
                            from toysales.sales ss, toysales.stores s , toysales.products p 
                            where ss.Store_ID =s.Store_ID and ss.Product_ID =p.Product_ID and s.Store_Name=%s and year(ss.`Date`)=%s
                            group by month(ss.`Date`), p.Product_Name
                            order by month(ss.`Date`)"""

        cursor.execute(query, (shop, anno,))

        for row in cursor:
            result.append(AndamentoNegozio(row["mm"], row["Pname"], row["qty"], row["revenue"], row["cv"]))

        cursor.close()
        conn.close()

        return result

