from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os # ← ★★★ "この行"が、"ある"か？ ★★★

# --- 基本設定 ---
basedir = os.path.abspath(os.path.dirname(__file__)) # ← ★★★ "この行"が、"ある"か？ ★★★

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'reservations.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__)) # ← ★★★ この一行を、追加 ★★★

# --- データベースの設計図（モデル） ---
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    reservation_datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Reservation {self.name}>'



# 【トップページを表示する】
@app.route('/')
def index():
    # データベースから、全ての予約を、取得する
    reservations = Reservation.query.all()
    # index.htmlを、画面に表示する。その際、予約リストを、渡す。
    return render_template('index.html', reservations=reservations)

# 【予約データを受け取り、保存する、魔法】
@app.route('/reserve', methods=['POST'])
def reserve():
    # フォームから、送信された、名前、日付、時間を、受け取る
    name = request.form['name']
    date_str = request.form['date']
    time_str = request.form['time']
    
    # 日付と時間を、結合して、DateTimeオブジェクトに、変換する
    # 時間が入力されていない場合のデフォルト値を設定
    if not time_str:
        time_str = '00:00'
    
    try:
        reservation_dt = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
    except ValueError:
        # 日付や時間のフォーマットが正しくない場合のエラーハンドリング
        return "日付または時間のフォーマットが無効です。やり直してください。", 400

    # 新しい予約データを、作成する
    new_reservation = Reservation(name=name, reservation_datetime=reservation_dt)
    
    # データベースに、追加
    db.session.add(new_reservation)
    # データベースに、変更を、確定
    db.session.commit()
    
    # トップページに、リダイレクト（戻る）
    return redirect(url_for('index'))

# 【サーバーを、起動する、魔法】
if __name__ == '__main__':
    app.run(debug=True)