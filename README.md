📖 Blog Project
A feature-rich blog application built using Django Rest Framework (DRF) for the backend and React with Redux and Tailwind CSS for the frontend. Users can read, create, edit, and manage blog posts with a seamless interface.

🚀 Features
📝 User authentication with registration and login
🗒️ Create, edit, and delete blog posts
📅 View posts date and time
💬 Commenting and liking system for user interaction
🎨 Responsive design using Tailwind CSS

🛠️ Tech Stack
Frontend: React, Tailwind CSS
Backend: Django, Django Rest Framework
Database: SQLite (for development), PostgreSQL (for production)
Deployment: AWS EC2, Nginx, Gunicorn, S3 Bucket


⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/ayshashfi/CMS-Blog.git
cd CMS-Blog

2️⃣ Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations and create superuser
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

3️⃣ Frontend Setup
cd frontend
npm install
npm start

🧪 Testing
Backend:
python manage.py test

Frontend:
npm test

🚢 Deployment
Deploy backend on AWS EC2 with Nginx and Gunicorn

