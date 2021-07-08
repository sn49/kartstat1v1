def WriteData(resultStr, cur):
    plus = 0
    for i in range(2):
        if i == 0:
            plus = 3
        elif i == 1:
            plus = -3

        myinfo = [resultStr[i * 3], resultStr[i * 3 + 1], resultStr[i * 3 + 2]]
        otherinfo = [
            resultStr[i * 3 + plus],
            resultStr[i * 3 + 1 + plus],
            resultStr[i * 3 + 2 + plus],
        ]

        sql = f"SELECT count(*) FROM Information_schema.tables WHERE table_schema = 'kart1v1' AND table_name = '{myinfo[0]}'"
        cur.execute(sql)
        result = cur.fetchone()[0]

        if result == 0:
            sql = f"create table {myinfo[0]} (nickname varchar(20) primary key not null,gamewin int default 0, gamelose int default 0, setwin int default 0, setlose int default 0, trackwin int default 0, tracklose int default 0)"
            cur.execute(sql)

        sql = f"select count(*) from {myinfo[0]} where nickname='{otherinfo[0]}'"
        cur.execute(sql)

        if cur.fetchone()[0] == 0:
            sql = f"insert into {myinfo[0]}(nickname,setwin,setlose,trackwin,tracklose) values ('{otherinfo[0]}',{myinfo[1]},{otherinfo[1]},{myinfo[2]},{otherinfo[2]})"
        else:
            sql = f"update {myinfo[0]} set setwin=setwin+{myinfo[1]},setlose=setlose+{otherinfo[1]},trackwin=trackwin+{myinfo[2]},tracklose=tracklose+{otherinfo[2]} where nickname='{otherinfo[0]}'"
        cur.execute(sql)

        if myinfo[1] > otherinfo[1]:
            sql = f"update {myinfo[0]} set gamewin=gamewin+1 where nickname='{otherinfo[0]}'"
        else:
            sql = f"update {myinfo[0]} set gamelose=gamelose+1 where nickname='{otherinfo[0]}'"
        print(sql)
        cur.execute(sql)
