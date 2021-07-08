import elo
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql
import json
import trackdata
import userdata

sqlinfo = open("mysql.json", "r")
sqlcon = json.load(sqlinfo)

database = pymysql.connect(
    user=sqlcon["user"],
    host=sqlcon["host"],
    db=sqlcon["db"],
    charset=sqlcon["charset"],
    password=sqlcon["password"],
    autocommit=True,
)
cur = database.cursor()


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

json_file_name = "spreadjson.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)

gc = gspread.authorize(credentials)

spreadsheet = gc.open("1대1 카트리그 기록")

worksheet = spreadsheet.worksheet(input("시트 이름 입력 >> "))

sheetvalue = worksheet.get_all_values()
player = []
for i in sheetvalue:
    filt = list(filter(None, i))
    if not len(filt) % 4 == 0:
        print(f"{sheetvalue.index(i)+1}번째 줄 데이터를 완성해주세요")
        exit()


for j in range(int(len(sheetvalue[0]) / 4)):  # 경기수
    for i in range(len(sheetvalue)):  # 줄수
        mapexist = False
        winner = None
        loser = None
        if i == 0:
            resultStr = sheetvalue[i][1 + 4 * j].split("-")
            player = [resultStr[0], resultStr[3]]
            userdata.WriteData(resultStr, cur)
            continue
        else:
            mapname = sheetvalue[i][1 + 4 * j].replace(" ", "_")
            picker = sheetvalue[i][2 + 4 * j]

            if player[0] == sheetvalue[i][3 + 4 * j]:
                winner = player[0]
                loser = player[1]
            else:
                winner = player[1]
                loser = player[0]

            trackdata.CheckTrackTable(mapname, cur)

            if sheetvalue[i][0 + 4 * j] == "ban":
                trackdata.WriteBanData(sheetvalue, i, mapname, cur, j)

                continue

            else:
                if sheetvalue[i][3 + 4 * j] == "X" or sheetvalue[i][3 + 4 * j] == "x":
                    continue
                trackdata.WritePickData(picker, mapname, cur)
                trackdata.WriteWinData(winner, mapname, cur, picker)
                trackdata.WriteLoseData(loser, mapname, cur, picker)
