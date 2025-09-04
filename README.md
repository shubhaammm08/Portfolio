# Portfolio Website

A modern, responsive portfolio website built with React frontend and FastAPI backend, featuring a contact form with file upload capabilities and MongoDB integration.

## 🚀 Features

### Frontend
- **Modern React UI** with Tailwind CSS
- **Responsive Design** for all device sizes
- **Interactive Contact Form** with file upload support
- **Dark/Light Theme** toggle
- **Smooth Animations** with Framer Motion
- **Component Library** with Radix UI primitives

### Backend
- **FastAPI** REST API with automatic documentation
- **MongoDB** integration for data persistence
- **File Upload** handling with validation
- **Email Service** integration for notifications
- **CORS** enabled for frontend communication
- **Comprehensive Testing** suite

## 🛠️ Tech Stack

### Frontend
- React 19.0.0
- Tailwind CSS 3.4.17
- Radix UI components
- Framer Motion
- React Router DOM
- Axios for API calls

### Backend
- FastAPI 0.110.1
- Uvicorn ASGI server
- MongoDB with Motor (async driver)
- Python 3.13+
- Pydantic for data validation
- Email validation and file handling

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.13+
- MongoDB (local or cloud)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd app/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in `app/backend/`:
   ```env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=portfolio_db
   ```

5. **Start the backend server:**
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd app/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8001`.

## 🧪 Testing

### Backend Tests
Run the comprehensive test suite:
```bash
cd app
python backend_test.py
```

The test suite includes:
- Health endpoint validation
- Contact form submission testing
- File upload validation
- Database persistence tests
- Email service integration tests

## 📁 Project Structure

```
portfolio/
├── app/
│   ├── backend/
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utility functions
│   │   ├── uploads/         # File uploads directory
│   │   ├── database.py      # MongoDB connection
│   │   ├── server.py        # FastAPI application
│   │   └── requirements.txt # Python dependencies
│   ├── frontend/
│   │   ├── public/          # Static assets
│   │   ├── src/
│   │   │   ├── components/  # React components
│   │   │   ├── pages/       # Page components
│   │   │   ├── contexts/    # React contexts
│   │   │   └── lib/         # Utility functions
│   │   └── package.json     # Node dependencies
│   └── backend_test.py      # Test suite
├── data_dump/               # MongoDB data exports
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 API Endpoints

### Health Check
- `GET /api/` - Root endpoint
- `GET /api/health` - Health status

### Contact Form
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get all messages (admin)
- `PATCH /api/contact/{id}/status` - Update message status
- `DELETE /api/contact/{id}` - Delete message

## 🚀 Deployment

### Backend Deployment
1. Set up MongoDB Atlas or local MongoDB
2. Configure environment variables
3. Deploy to your preferred platform (Heroku, Railway, etc.)

### Frontend Deployment
1. Build the production version:
   ```bash
   npm run build
   ```
2. Deploy to Vercel, Netlify, or your preferred platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Shubham Kadam**
- GitHub: [@shubhaammm08](https://github.com/shubhaammm08)
- Portfolio: [https://github.com/shubhaammm08/Portfolio](https://github.com/shubhaammm08/Portfolio)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python web framework
- [React](https://reactjs.org/) for the frontend library
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Radix UI](https://www.radix-ui.com/) for accessible components
