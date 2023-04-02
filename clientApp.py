from flask import Flask, request, jsonify,render_template,flash
import os
from flask_cors import CORS, cross_origin
from utils.utils import decodeImage,encodeImageIntoBase64
from predict import ocr
import re

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)


#@cross_origin()
class ClientApp:
    def __init__(self):
        self.filename = os.path.join('static','images',"inputImage.jpg")
        #modelPath = 'research/ssd_mobilenet_v1_coco_2017_11_17'
        self.objectDetection = ocr(self.filename)

@app.route("/", methods=["GET", "POST"])
def homepage():
    """Render homepage."""
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    # try:
        if request.method == 'POST':  
            f = request.files['file']
            filepath=os.path.join('static','images',f.filename)
            f.save(filepath)
            image=encodeImageIntoBase64(filepath)
            decodeImage(image, clApp.filename)
            result = clApp.objectDetection.getPrediction()
            Licence_no =" ".join(re.findall("[A-Z]{2}[0-9]{2} [0-9]{11}",result))
            x=result.strip().split("\n")
            x=[i for i in x if re.search("[a-zA-Z]",i)]
            State=Licence_no[:2]
            Name=''
            Address=''
            if("DL No" not in result):
                enum=enumerate(x)
                info=dict((i,j) for i,j in enum)
            else:
                for i in range(len(x)):
                    if 'STATE' in x[i]:
                        State=x[i][:-3]
                    if "Valid" in x[i]:
                        Validity=re.findall("[0-9]{2}\-[0-9]{2}\-[0-9]{4}",x[i])[0]
                    if "Name" in x[i]:
                        Name=" ".join(re.findall("[A-Z]+",x[i])[1:])
                    if 'Add' in x[i]:
                        Address=",".join([x[i],x[i+1],x[i+2]])[6:]
                info={"Name":Name,"Address":Address,"State":State,"Licence_no":Licence_no,"Validity":Validity}
            
            return render_template("prediction.html",info=info,len=len(info),img=filepath)
    # except FileNotFoundError as e:  
    #     flash("please upload a file " )
    #     return render_template("index.html")
    # except Exception as e:
    #     flash("something went wrong :- " +str(e)[0:30])
    #     return render_template("index.html")
    # image = request.json['image']
    # decodeImage(image, clApp.filename)
    # result = clApp.objectDetection.getPrediction()
    # return jsonify({"result" : result})


#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='127.0.0.1', port=7000, debug=True)
