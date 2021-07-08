def WriteBanData(sheetvalue, i, mapname, cur, j):
    sql = f"select count(*) from {mapname} where nickname='{sheetvalue[i][2+ 4 * j]}'"
    cur.execute(sql)
    if cur.fetchone()[0] == 0:
        sql = f"insert into {mapname}(nickname,ban) values ('{sheetvalue[i][2+ 4 * j]}',1)"  # 닉네임만 삽입
    else:
        sql = (
            f"update {mapname} set ban=ban+1 where nickname='{sheetvalue[i][2+ 4 * j]}'"
        )
    print(sql)
    cur.execute(sql)


def WritePickData(picker, mapname, cur):
    sql = f"select count(*) from {mapname} where nickname='{picker}'"
    cur.execute(sql)
    result = cur.fetchone()[0]
    if result == 0:
        sql = f"insert into {mapname}(nickname,pick) values ('{picker}',1)"  # 닉네임만 삽입
    else:
        sql = f"update {mapname} set pick=pick+1 where nickname='{picker}'"
    cur.execute(sql)


def WriteWinData(winner, mapname, cur, picker):
    sql = f"select count(*) from {mapname} where nickname='{winner}'"
    cur.execute(sql)
    result = cur.fetchone()[0]

    if result == 0:
        sql = f"insert into {mapname}(nickname,win) values ('{winner}',1)"  # 닉네임만 삽입
    else:
        sql = f"update {mapname} set win=win+1 where nickname='{winner}'"
    cur.execute(sql)

    if picker == winner:
        sql = f"update {mapname} set pickwin=pickwin+1 where nickname='{winner}'"
        cur.execute(sql)


def WriteLoseData(loser, mapname, cur, picker):
    sql = f"select count(*) from {mapname} where nickname='{loser}'"
    cur.execute(sql)

    if cur.fetchone()[0] == 0:
        sql = f"insert into {mapname}(nickname,lose) values ('{loser}',1)"  # 닉네임만 삽입
    else:
        sql = f"update {mapname} set lose=lose+1 where nickname='{loser}'"

    cur.execute(sql)

    if picker == loser:
        sql = f"update {mapname} set picklose=picklose+1 where nickname='{loser}'"
        cur.execute(sql)


def CheckTrackTable(mapname, cur):
    sql = f"SELECT count(*) FROM Information_schema.tables WHERE table_schema = 'kart1v1' AND table_name = '{mapname}'"
    cur.execute(sql)
    result = cur.fetchone()[0]

    if result == 0:
        sql = f"create table {mapname} (nickname varchar(20) primary key not null,pick int default 0,pickwin int default 0,picklose int default 0,ban int default 0,win int default 0 ,lose int default 0)"
        cur.execute(sql)
