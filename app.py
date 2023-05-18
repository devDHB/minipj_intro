from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://sparta:test@cluster0.snrvzql.mongodb.net/?retryWrites=true&w=majority"
)
db = client.dbsparta


@app.route("/")
def home():
    return render_template("index.html")


# 라우트 추가 - 방두현
@app.route("/방두현")
def doohyeon():
    return render_template("doohyeon.html")


@app.route("/member", methods=["POST"])
def member_post():
    # 멤버 정보 받기
    url_receive = request.form["url_give"]
    name_receive = request.form["name_give"]
    age_receive = request.form["age_give"]
    mbti_receive = request.form["mbti_give"]
    comment_receive = request.form["comment_give"]
    intro_receive = request.form["intro_give"]

    doc = {
        "url": url_receive,
        "name": name_receive,
        "age": age_receive,
        "mbti": mbti_receive,
        "comment": comment_receive,
        "intro": intro_receive,
    }
    db.members.insert_one(doc)

    return jsonify({"msg": "저장 완료!"})


# 멤버 데이터 불러오기
@app.route("/member", methods=["GET"])
def member_get():
    all_members = list(db.members.find({}, {"_id": False}))
    return jsonify(
        {
            "result": all_members,
        }
    )


# 방두현 데이터 불러오기
@app.route("/doohyeon", methods=["GET"])
def doohyeon_get():
    doohyeon = list(db.members.find({"name": "방두현"}, {"_id": False}))
    return jsonify({"result": doohyeon})


# 삭제 기능 추가
@app.route("/delete_member", methods=["POST"])
def delete_member():
    delete_name_receive = request.form["delete_name_give"]
    db.members.delete_one({"name": delete_name_receive})


# 수정 기능 추가
@app.route("/update_intro", methods=["PUT"])
def update_intro():
    name_receive = request.form["name_give"]
    update_intro_receive = request.form["update_text_give"]
    db.members.update_one(
        {"name": name_receive}, {"$set": {"intro": update_intro_receive}}
    )


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
