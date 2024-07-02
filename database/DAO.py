from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getLocalizzazioni():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                from genes_small.classification c """

        cursor.execute(query, )

        for row in cursor:
            if row["Localization"] in result.keys():
                result[row["Localization"]].append(row["GeneID"])
            else:
                result[row["Localization"]] = [row["GeneID"]]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.Localization as loc1, c2.Localization as loc2, c.GeneID as g1, c2.GeneID as g2, count(distinct(i.`Type`)) as num
                from genes_small.classification c, genes_small.classification c2, genes_small.interactions i  
                where ((c2.GeneID = i.GeneID2 and c.GeneID = i.GeneID1) or (c2.GeneID = i.GeneID1 and c.GeneID = i.GeneID2))
                and c.GeneID <> c2.GeneID and c2.Localization < c.Localization
                group by loc1, loc2"""

        cursor.execute(query, )

        for row in cursor:
            result.append((row["loc1"], row["loc2"], row["num"]))

        cursor.close()
        conn.close()
        return result
