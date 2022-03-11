# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:28:52 2022

@author: nick
"""
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .master("local") \
    .appName("dataframe_split") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

sc = spark.sparkContext
df1 = spark.read.csv('lvr_landcsv/a_lvr_land_a.csv', inferSchema=True, header=True)
df2 = spark.read.csv('lvr_landcsv/a_lvr_land_a.csv', inferSchema=True, header=True)
df3 = spark.read.csv('lvr_landcsv/a_lvr_land_a.csv', inferSchema=True, header=True)
df4 = spark.read.csv('lvr_landcsv/a_lvr_land_a.csv', inferSchema=True, header=True)
df5 = spark.read.csv('lvr_landcsv/a_lvr_land_a.csv', inferSchema=True, header=True)

df1.unionAll(df2)
df1.unionAll(df3)
df1.unionAll(df4)
df1.unionAll(df5)

#df2.fliter(df1["主要用途"] == "住家用" & df1["建物型態"].contains("住宅大樓")).collect()

data = [('James',3000),('Anna',4001),('Robert',6200)]
df = spark.createDataFrame(data,["name","salary"])
df.show()     