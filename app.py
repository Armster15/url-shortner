from flask import *
import pymongo, random, string, validators, os
from flask_xcaptcha import XCaptcha
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("secret_key")

# MongoDB
client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client['url-shortner']
collection = db['url-shortner']

# hCaptcha
app.config['XCAPTCHA_SITE_KEY'] = os.getenv("HCAPTCHA_SITE_KEY")
app.config['XCAPTCHA_SECRET_KEY'] = os.getenv("HCAPTCHA_SECRET_KEY")
app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"
xcaptcha = XCaptcha(app=app)

# These are short link endings that users cannot use on the website
restricted = ['add_link']

def generate_random_string(length=7):
    """Generates random string"""
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))

@app.route("/")
def home():
    return render_template("index.html", host=request.host)

@app.route("/<link>/")
def redirect_route(link):
    exists = collection.find_one({"short_link_ending": link.lower()})
    if exists is None:
        return render_template("index.html", error="This short URL doesn't exist.", host=request.host)

    else:
        return redirect(exists['long_url'])

@app.route("/add_link/", methods=["POST"])
def add_link():
    if not xcaptcha.verify():
        return jsonify({"error": "Please complete the captcha"}), 400
    
    data = dict(request.form)
    data = {"long_url": data["long_url"], "short_link_ending": data["short_link_ending"]} # Gets rid of hCaptcha stuff

    data["short_link_ending"] = data["short_link_ending"].lower()

    if data["long_url"].strip() == "":
        return jsonify({"error": "Please provide a long URL to shorten"}), 400
    
    if len(data["long_url"]) > 32:
        return jsonify({"error": 'Short link endings must be 32 characters or less'}), 400

    if data["short_link_ending"].endswith("/"): 
        data["short_link_ending"] = data["short_link_ending"][:-1] # Strip trailing "/"
    
    if data["short_link_ending"].startswith("/"): 
        return jsonify({"error": 'Short link endings cannot begin with a "/"'}), 400
    
    if " " in data["short_link_ending"]: 
        return jsonify({"error": 'Short link endings cannot have blank spaces'}), 400
    
    if not validators.url(data["long_url"]):
        return jsonify({"error": 'The URL provided is not a valid URL.\nCheck if you have "http://" at the beginning of your URL'}), 400

    if data["short_link_ending"].strip() == "":
        data["short_link_ending"] = generate_random_string()
        exists = collection.find_one({"short_link_ending": data["short_link_ending"]})
        while exists is not None:
            data["short_link_ending"] = generate_random_string()
            exists = collection.find_one({"short_link_ending": data["short_link_ending"]})
            
    exists = collection.find_one({"short_link_ending": data["short_link_ending"]})
    if exists is not None or data["short_link_ending"] in restricted: # If the short link ending already exists
        return jsonify({"error": "This short link ending already exists"}), 400

    else:
        collection.insert_one(data)
        return jsonify({"success": True, "long_url": data["long_url"], "short_link_ending": data["short_link_ending"]})


if __name__ == "__main__":
    app.run(debug=True)