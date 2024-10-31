# csvからデータを自動入力

import csv
from app import add_race,get_weekday,app,delete_race

def import_csv(filename):
    # csvファイルを読み込む
    """ 
    大会名，日付，都道府県，市町村，距離，累積標高，URL
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            name = row[0]
            date = row[1]
            week = get_weekday(date)
            prefecture = row[2]
            city = row[3]
            distance = int(row[4])
            gain = int(row[5])
            url = row[6]
            with app.app_context():
                add_race(name,date,week,prefecture,city,distance,gain,url)
            #print(name,date,week,prefecture,city,distance,gain,url)


if __name__ == '__main__':
    #filename = "../test.csv"
    #import_csv(filename)

    delete_race(4)
