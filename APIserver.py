# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:28:52 2022

@author: nick
"""
import pandas as pd
import json
from flask import Flask

app = Flask(__name__)

df1 = pd.read_csv("lvr_landcsv/a_lvr_land_a.csv").drop(0) #台北市
df1["縣市"] = "台北市"
df2 = pd.read_csv("lvr_landcsv/b_lvr_land_a.csv").drop(0) #台中市
df2["縣市"] = "台中市"
df3 = pd.read_csv("lvr_landcsv/e_lvr_land_a.csv").drop(0) #高雄市
df3["縣市"] = "高雄市"
df4 = pd.read_csv("lvr_landcsv/f_lvr_land_a.csv").drop(0) #新北市
df4["縣市"] = "新北市"
df5 = pd.read_csv("lvr_landcsv/h_lvr_land_a.csv").drop(0) #桃園市
df5["縣市"] = "桃園市"
frames = [df1, df2, df3, df4, df5]

num_dict= \
{"0":"零",
 "1":"一",
 "2":"二",
 "3":"三",
 "4":"四",
 "5":"五",
 "6":"六",
 "7":"七",
 "8":"八",
 "9":"九",
 "-":"負"}


concat_mid_list = ["", "十", "百", "千", "萬"]


def auth(num):
    if not isinstance(num, int):
        print("error input, should be integer")
        return False
    if abs(num) > 1e8:
        print("error input, abs value should be less than 1e8")
        return False
    return True
    

def num2chinese(num): #轉換數字成中文
    if not auth(num):
        return ""
    temp_chinese = derect_translate(num)
    updated_chinese = update(temp_chinese)
    if num >= 0:
        return updated_chinese
    return num_dict[str(num)[0]] + updated_chinese

    
def derect_translate(num): 
    return [num_dict[x] for x in str(abs(num))]


def update(temp_chinese):
    tmp_inf = []
    for ix, x in enumerate(temp_chinese[::-1]):
        if x == "零":
            # 當前位為0時 特殊處理重複零(上一個為零)問題
            if tmp_inf and (tmp_inf[-1] == "零" or tmp_inf[-1] == "零"):
                pass
            elif tmp_inf or len(temp_chinese) == 1:
                tmp_inf.append(x)
        else:
            tmp_inf.append(x + concat_mid_list[ix % 4])
        # 特殊處理 萬這個單位上的字元
        if ix == 3 and len(temp_chinese) > 4:
            tmp_inf.append("萬")
    # print("tmp_inf is ", tmp_inf)
    tmp_inf.reverse()
    return "".join(tmp_inf)
  

def getData(df, ls):
    #print(df.iloc[0]["縣市"])
    itemList = []
    record = [] 
    for index, row in df.iterrows():
        detail = {"type":row["建物型態"],
                  "district":row["鄉鎮市區"]}
        date = str(int(row["交易年月日"])+19110000)[:4]+"-"+str(row["交易年月日"])[-4:-2]+"-"+str(row["交易年月日"])[-2:] #將日期轉成yyyy-mm-dd格式
        if date in record:
            for item in itemList:
                if item["date"] == date: #如果日期一樣就append進event
                    item["event"].append(detail)
        else:
            dic = {"date":date,
                   "event":[detail]
                    }
            itemList.append(dic)
            record.append(date)
        #print(row["交易年月日"])
    temp = {"city":df.iloc[0]["縣市"], 
            "time_slots":itemList
            }
    ls.append(temp)
    return ls
   
    
@app.route('/search/<query>')
def search(query):
    ls = []
    for df in frames:
        if query.isdigit(): #確認輸入的是否為數字            
            floor = num2chinese(int(query))+"層" #將數字轉成中文
            fliter = (df["總樓層數"] == floor)
            result = df[fliter]
            if len(result) > 0: #如果資料存在
                ls = getData(result, ls)

        else:
            fliter = (df["鄉鎮市區"] == query) #比對鄉鎮市區
            result = df[fliter]
            if len(result)>0:
                ls = getData(result, ls)
            else:
                fliter = (df["建物型態"].str.contains(query)) #比對建物型態
                result = df[fliter]
                if len(result):
                    ls = getData(result, ls)

    return json.dumps(ls, ensure_ascii=False) #轉成json後return



if __name__ == '__main__':
    app.debug = True
    app.run()


        


