Running instructions:

Backend API:
on powershell:
cd into flask_api folder

// upgrade pip to its latest version  
python -m pip install --upgrade pip
// install virtualenv
pip install virtualenv
// Create venv
py -m venv venv
// activate venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

go into app.py
https://openexchangerates.org/signup/free
Create your account here,
copy you api key, and paste it at line line 63 app.py (Replace api_key variable with your api key)
flask --app app.py --debug run


Front End:
on powershell
cd into startbootstrap-sb-admin-2 folder
// upgrade pip to its latest version  
python -m pip install --upgrade pip
// install virtualenv
pip install virtualenv
// Create venv
py -m venv venv
// activate venv
.\venv\Scripts\Activate.ps1
npm install
npm start