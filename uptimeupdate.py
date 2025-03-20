uptime_dir = "/Users/devssh/EventServer/Event/"
uptime_folder = "Aggregate/uptimedays/"
aggregate_folder = "Aggregate/"
import json

def get_uptime():
    with open(uptime_dir + "uptime.txt") as file:
        return "".join(file.readlines()).split("\n")

def parse_datetime(datestr):
    datetime = datestr.split(" ")
    date = datetime[0]
    time = datetime[1]
    datearr = date.split("-")
    timearr = time.split(":")
    year = int(datearr[0])
    month = int(datearr[1])
    day = int(datearr[2])
    hour = int(timearr[0])
    minute = int(timearr[1])
    second = int(timearr[2])
    timeformat = ":".join([timearr[0], timearr[1]])
    return {"year": year, "month": month, "day": day, "hour": hour, "minute": minute, "second": second, 
            "date": date, "time": timeformat, "datetime": date + " " + timeformat
            }

def is_contiguous_time(datetime1, datetime2):
    minute_check = ((datetime1["minute"]+1)%60) == datetime2["minute"]
    hour_equality_check = datetime1["hour"]==datetime2["hour"]
    last_minute_check = datetime1["minute"]==59
    first_minute_check = datetime2["minute"]==0
    hour_plus_one_check = datetime1["hour"] + 1 == datetime2["hour"]
    if minute_check and hour_equality_check:
        return True
    if last_minute_check and first_minute_check and hour_plus_one_check:
        return True
    return False

def join_contiguous(datetime_data, date):
    relevant_data = list(sorted([x for x in datetime_data if x["date"] == date], key=lambda datetime: datetime["datetime"]))
    count = len(relevant_data)
    if count == 0:
        return []
    if count == 1:
        return [ [relevant_data[0], relevant_data[0], {"count": 0}] ]
    contiguous_data = [ [relevant_data[0], relevant_data[0], {"count": 1}] ]
    for i in range(1, len(relevant_data)):
        prev = relevant_data[i-1]
        curr = relevant_data[i]
        contiguous_check = is_contiguous_time(prev, curr)
        if contiguous_check:
            data_index = len(contiguous_data) - 1
            data = contiguous_data[data_index]
            contiguous_data[data_index] = [data[0], curr, {"count":data[2]["count"] + 1}]
        else:
            contiguous_data = [*contiguous_data, [curr, curr, {"count": 1}]]
    return contiguous_data

def convert_to_datetime(contiguous_data):
    return [[x[0]["datetime"], x[1]["datetime"], x[2]] for x in contiguous_data]

def calculate_count(day_data):
    return sum([x[2]["count"] for x in day_data["data"]])

data = [x.strip() for x in get_uptime() if len(x.strip()) > 0]
datetime_data = [parse_datetime(datetime) for datetime in data]
date_list = list(sorted(list(set([x["date"] for x in datetime_data]))))

output_data = {date: join_contiguous(datetime_data, date) for date in date_list}
output_data = {k:{"data":convert_to_datetime(v)} for (k,v) in output_data.items()}
output_data = {k: {**v, "daycount": calculate_count(v)} for (k,v) in output_data.items()}

#print(json.dumps(output_data, indent=3))
for (k,v) in output_data.items():
    with open(uptime_dir + uptime_folder + k, "w") as file:
        file.write(json.dumps(v))
        file.flush()
        file.close()

with open(uptime_dir + aggregate_folder + "uptime.json", "w") as file:
    file.write(json.dumps(output_data))
    file.flush()
    file.close()



