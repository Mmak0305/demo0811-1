from flask import *
from PIL import Image
import os

# 初始化 Flask 伺服器
app = Flask(
    __name__,
    static_folder="static",  # 靜態檔案的資料名稱
    static_url_path="/static",  # 靜態檔案對應的網址路徑
)

# 處理路由
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    return render_template("member.html")

@app.route("/error")
def error():
    message = request.args.get("msg", "發生錯誤請聯繫客服")
    return render_template("error.html", message=message)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        filename = file.filename

        # 保存圖片到 "static/uploadfile" 資料夾
        save_path = os.path.join("static", "uploadfile", filename)
        file.save(save_path)

        # 轉換 TIFF 到 JPEG
        if filename.endswith('.tif') or filename.endswith('.tiff'):
            img = Image.open(save_path)
            filename = filename.rsplit('.', 1)[0] + '.jpg'
            save_path = os.path.join("static", "uploadfile", filename)
            img.convert('RGB').save(save_path, "JPEG")

        # 創建上傳圖片 URL
        uploaded_image_url = url_for('static', filename="uploadfile/" + filename)

        # 從 "static/DownloadFile" 資料夾中抓取特定名稱的圖片
        predicted_image_filename = "abc.jpg"  # 你需要更改為實際的檔案名稱
        predicted_image_url = url_for('static', filename="DownloadFile/" + predicted_image_filename)

        # 渲染模板
        return render_template("preview.html", uploaded_image_url=uploaded_image_url, another_image_url=predicted_image_url)
    else:
        return "No file uploaded"

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if os.path.exists("DownloadFile/" + filename):
        return send_from_directory('DownloadFile', filename, as_attachment=True)
    else:
        return "No file found"

app.secret_key = "deep-high-resolution"  # 設定 Session的密鑰
app.run(host='0.0.0.0', port=8080, debug=False)
