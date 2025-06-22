## Prerequisites
Make sure you have the following installed
- Python 3.10+
- Nodejs + npm
- Git
> React app runs on http://localhost:3000  
> Django runs on http://localhost:8000  
> Verify nothing else is using these ports before running

## Django Setup Instructions

1. Clone the Repository
```bash
git clone https://github.com/lcai62/producthub
cd producthub
```

2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/active # .venv\Scripts\activate on Windows

pip install -r requirements.txt
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Seed data
```bash
python manage.py loaddata sampledata.json
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run the backend
```bash
python manage.py runserver
```

## React Setup Instructions
```bash
cd frontend
npm install
npm start
```

## AI disclosure
ChatGPT was used to generate the tag names, category names, and product names, descriptions, prices, stock, along with associated tags and categories
