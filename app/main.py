from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from databases import db, raceInfo
from datetime import datetime

# trail run大会の一覧を表示するアプリ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

with app.app_context():
    db.create_all()


def add_race(name,date,week,prefecture,city,distance,gain,url):
    new_race = raceInfo(name=name,date=date,week=week,prefecture=prefecture,city=city,distance=distance,gain=gain,url=url)

    db.session.add(new_race)
    db.session.commit()
    print(f"Added Race!: {name}")

def delete_race(id):
    with app.app_context():
        race = raceInfo.query.get(id)
        if race:
        # データベースから削除
            db.session.delete(race)
            db.session.commit()
            print(f"{id} has been deleted.")
        
def get_weekday(date_str):
    # 文字列を日付に変換
    print(date_str)
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return ""
    # 曜日を取得（0=月曜日, 6=日曜日）
    weekday_number = date_obj.weekday()
    # 曜日名リスト
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    # 対応する曜日名を返す
    return weekdays[weekday_number]


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        race_info = db.session.query(raceInfo).all()
        return render_template("index.html",races=race_info)

@app.route('/add_race', methods=['GET','POST'])
def add_race_page():
    if request.method == 'GET':
        return render_template("add_race.html")
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        week = get_weekday(date)
        prefecture = request.form.get('prefecture')
        city = request.form.get('city')
        distance = request.form.get('distance')
        gain = request.form.get('gain')
        url = request.form.get('url')
        add_race(name,date,week,prefecture,city,distance,gain,url)
        print(date)
        return redirect('/')

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template("search.html")

@app.route("/search_filter", methods=['POST'])
def search_filter():
    query = raceInfo.query
    name = request.form.get('name')
    week = request.form.get('week')
    prefecture = request.form.get('prefecture')
    min_distance = request.form.get('min_distance')
    max_distance = request.form.get('max_distance')
    min_gain = request.form.get('min_gain')
    max_gain = request.form.get('max_gain')
    if name:
        query = query.filter(raceInfo.name.like(f'%{name}%'))
    if week:
        query = query.filter(raceInfo.week == week)
        week=f'曜日：{week}' 
    if prefecture:
        query = query.filter(raceInfo.prefecture.like(f'%{prefecture}%'))
        prefecture=f'都道府県：{prefecture}'
        
    if min_distance:
        query = query.filter(raceInfo.distance >= min_distance)
        min_distance=f'最低距離：{min_distance}'
    if max_distance:
        query = query.filter(raceInfo.distance <= max_distance)
        max_distance=f'最大距離：{max_distance}'
    if min_gain:
        query = query.filter(raceInfo.gain >= min_gain)
        min_gain=f'最低累積標高：{min_gain}'
    if max_gain:
        query = query.filter(raceInfo.gain <= max_gain)
        max_gain=f'最大累積標高：{max_gain}'
    
    races = query.all()
    print(query)
    return render_template("search.html",races=races, name=name,
    week=week, 
    prefecture=prefecture,
    min_distance=min_distance,max_distance=max_distance, 
    min_gain=min_gain, 
    max_gain=max_gain)

@app.route("/search_sort", methods=['POST'])
def search_sort():
    query = raceInfo.query
    category = request.form.get('category')
    order = request.form.get('order')
    print(category, order)
    if category == 'date':
        if order == 'asc':
            query = query.order_by(raceInfo.date)
        if order == 'desc':
            query = query.order_by(raceInfo.date.desc())

    if category == 'distance':
        if order == 'asc':
            query = query.order_by(raceInfo.distance)
        if order == 'desc':
            query = query.order_by(raceInfo.distance.desc())
    if category == 'gain':
        if order == 'asc':
            query = query.order_by(raceInfo.gain)
        if order == 'desc':
            query = query.order_by(raceInfo.gain.desc())
    return render_template("search.html",races=query.all())

# error handling
@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html"), 400

@app.errorhandler(Exception)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8111)