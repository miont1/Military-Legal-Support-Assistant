# Diplom Project

This project is a web application with a Django backend and a React frontend.

## Project Structure

- `backend/`: Django REST Framework API
- `frontend/`: React application (Vite/CRA)

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Features

- User Authentication
- Profile Management
- Chat Interface
- Data Analysis (Faiss integration)
