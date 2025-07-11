import re
from datetime import datetime
from datemysql import get_db

#导入数据
LOG_FILE = "termux_heartbeat.log"
MACHINE = "我的平板"
#从日志里面导入数据
pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ✅ Termux 在线 - 当前电量: (\d+)%$")

def parse_and_import():
    success_count = 0
    fail_count = 0

    with open(LOG_FILE, "r",encoding='utf-8') as f:
        lines = f.readlines()
    with get_db() as conn:
        with conn.cursor() as cursor:
            for i,line in enumerate(lines, start = 1):
                try:
                    match = pattern.match(line.strip())
                    if not match:
                        continue

                    ts = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                    power = int(match.group(2))

                    #避免重复插入
                    cursor.execute("SELECT id FROM machinepower WHERE time = %s AND machine = %s", (ts,MACHINE))
                    if cursor.fetchone():
                        continue

                    cursor.execute("INSERT INTO machinepower(time, machine,power) VALUES (%s, %s,%s)", (ts,MACHINE,power))
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    print(f"第{i}行处理失败 {line.strip()}-> 错误：{e}")
            print(f"导入完成，成功导入{success_count}条")

        print("日志数据导入成功")

if __name__ == "__main__":
    parse_and_import()