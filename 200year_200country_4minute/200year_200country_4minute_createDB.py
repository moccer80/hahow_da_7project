# 整理成class 完整結構化 一鍵搞定

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn

class creategapminderDB:
    def __init__(self):
        self.name_list = ["gdp_pcap","life","pop","geo"]

    def import_as_dataframe(self):
        import pandas as pd
        dict_gpmDB = {}
        for name in self.name_list:
            temp_data = pd.read_csv(f"{name}.csv")
            dict_gpmDB[name] = temp_data
        return dict_gpmDB
    
    def create_database(self):
        import sqlite3
        # 建立資料庫連結
        connection = sqlite3.connect("data_sql/gapminder.db")       # gapminder.db是名稱
        dict_gpmDB = self.import_as_dataframe()
        # 把資料轉到SQL裡面
        for name,data in dict_gpmDB.items():
            # index = False代表不要放入index,不要放入index,if_exists = "replace"代表如果原本資料庫裡有一樣的就直接取代
            data.to_sql(name = name,con = connection, index = False, if_exists = "replace")
        drop_view_sql = """
        DROP VIEW IF EXISTS plotting;
        """  

        create_view_sql = """
        CREATE VIEW plotting AS
        SELECT geo.name AS country_name,
            geo.world_4region AS continent,
            gdp_pcap.time AS dt_year,
            gdp_pcap.gdp_pcap AS gdp_per_capita,
            life.lex AS life_expectancy,
            pop.pop AS population
        FROM gdp_pcap 
        JOIN geo ON gdp_pcap.country = geo.country
        JOIN life ON gdp_pcap.country = life.country AND gdp_pcap.time = life.time
        JOIN pop ON gdp_pcap.country = pop.country AND gdp_pcap.time = pop.time
        WHERE gdp_pcap.time < 2024;
        """
        cur = connection.cursor()
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)

        connection.close()

create_gapminder_DB = creategapminderDB()
create_gapminder_DB.create_database()