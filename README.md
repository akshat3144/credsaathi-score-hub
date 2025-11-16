# CredSaathi - AI-Powered Credit Scoring Platform

CredSaathi is a full-stack web application for credit scoring gig economy workers using AI/ML models with alternative data sources (financial, social, and gig signals).

## Tech Stack

### Backend
- **FastAPI** (Python 3.11+) - Async REST API
- **MongoDB** - Document database with Motor (async driver)
- **Google OAuth 2.0** - Authentication using Authlib
- **JWT** - Stateless session management
- **Pydantic** - Data validation and settings management

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Axios** - HTTP client with interceptors
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **shadcn/ui** - Component library

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Pydantic settings
│   │   ├── db.py                # MongoDB connection
│   │   ├── models/              # DB schema documentation
│   │   ├── schemas/             # Pydantic request/response models
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic (OAuth, ML)
│   │   └── utils/               # Security, dependencies
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── src/                         # React frontend
├── scripts/
│   └── seed_db.py              # Database seeding script
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** and npm ([Download](https://nodejs.org/))
- **MongoDB 7.0+** ([Download](https://www.mongodb.com/try/download/community))
- **Google OAuth credentials** ([Get credentials](https://console.cloud.google.com/apis/credentials))

### 1. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google+ API**
4. Go to **Credentials** → **Create Credentials** → **OAuth Client ID**
5. Choose **Web application**
6. Add authorized JavaScript origins:
   - `http://localhost:8080`
   - `http://localhost:5173`
7. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback`
8. Copy the **Client ID** and **Client Secret**

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your credentials:
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - MONGODB_URI
# - GOOGLE_CLIENT_ID
# - GOOGLE_CLIENT_SECRET
```

**Example `.env`:**
```env
APP_HOST=127.0.0.1
APP_PORT=8000
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=credsaathi_db

GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8000/auth/google/callback

FRONTEND_URL=http://localhost:8080
```

### 3. Start MongoDB

```bash
# Using Docker
docker run -d -p 27017:27017 --name credsaathi_mongo mongo:7.0

# OR install MongoDB locally and start it
# (MongoDB runs on port 27017 by default)
```

### 4. Run Backend

```bash
# From backend directory with virtual environment activated
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: **http://localhost:8000**
API docs: **http://localhost:8000/docs**

### 5. Frontend Setup

```bash
# Open new terminal in project root
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:8080** (or 5173)

### 6. Seed Database (Optional)

```bash
# From project root
python scripts/seed_db.py
```

This will create 30 sample gig worker profiles for testing.

## Using Docker Compose (Alternative)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This starts:
- MongoDB on port 27017
- Backend on port 8000
- Frontend needs to be run separately: `npm run dev`

## Usage

1. **Login**
   - Navigate to `http://localhost:8080`
   - Click "Get Started" or "Sign In"
   - Authenticate with Google

2. **Dashboard**
   - View all applicants
   - Filter by risk tier
   - View statistics and score distribution

3. **Add Applicant**
   - Click "Add Applicant"
   - Fill in basic info, financial, social, and gig economy data
   - Submit to save

4. **Calculate Credit Score**
   - Click "Calculate Score" on any applicant card
   - View detailed results with feature importances
   - See risk assessment and recommendations

## API Endpoints

### Authentication
- `GET /auth/google/login` - Initiate OAuth flow
- `GET /auth/google/callback` - OAuth callback
- `POST /auth/google/exchange` - Exchange ID token for JWT
- `POST /auth/logout` - Logout

### Users
- `GET /users/me` - Get current user info
- `PATCH /users/me` - Update current user

### Data Ingestion
- `POST /ingest/applicant` - Create applicant
- `GET /ingest/applicants` - List applicants
- `POST /ingest/financial` - Update financial data
- `POST /ingest/social` - Update social data
- `POST /ingest/gig` - Update gig data

### Prediction
- `POST /predict/score` - Calculate credit score
- `GET /predict/history/{applicant_id}` - Get prediction history

### Health
- `GET /health` - Health check

## Integrating Your ML Model

The current implementation uses a stub ML model in `backend/app/services/ml_stub.py`. To integrate your actual model:

1. **Save your trained model:**
   ```python
   import joblib
   joblib.dump(model, 'models/credit_model.pkl')
   ```

2. **Load in `ml_stub.py`:**
   ```python
   import joblib
   import numpy as np
   
   MODEL_PATH = "models/credit_model.pkl"
   model = joblib.load(MODEL_PATH)
   
   def predict_credit_score(data: Dict[str, Any]) -> Dict[str, Any]:
       features = normalize_features(data)
       feature_vector = np.array(list(features.values())).reshape(1, -1)
       
       score = int(model.predict(feature_vector)[0])
       # ... rest of implementation
   ```

3. **Match feature engineering** - Ensure `normalize_features()` matches your training pipeline

4. **Update feature importances** - Use SHAP values or model's native feature importances

## Environment Variables

### Backend (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key (32+ chars) | `openssl rand -hex 32` |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `GOOGLE_CLIENT_ID` | OAuth client ID | `xxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret | `GOCSPX-xxx` |
| `GOOGLE_OAUTH_REDIRECT_URI` | OAuth callback URL | `http://localhost:8000/auth/google/callback` |
| `FRONTEND_URL` | Frontend origin for CORS | `http://localhost:8080` |

### Frontend (.env)
| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

## Troubleshooting

### OAuth Issues

**Error: "redirect_uri_mismatch"**
- Ensure redirect URI in Google Console exactly matches `GOOGLE_OAUTH_REDIRECT_URI` in `.env`
- Check for trailing slashes

**Error: "invalid_client"**
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct
- Ensure OAuth consent screen is configured

### MongoDB Connection

**Error: "ServerSelectionTimeoutError"**
- Check MongoDB is running: `docker ps` or `mongosh`
- Verify `MONGODB_URI` in `.env`

### CORS Errors

- Ensure `FRONTEND_URL` in backend `.env` matches your frontend URL
- Clear browser cache
- Check browser console for specific error

### JWT Issues

**Error: "Could not validate credentials"**
- Token expired - login again
- Check `SECRET_KEY` hasn't changed
- Verify `ACCESS_TOKEN_EXPIRE_MINUTES` is reasonable

## Testing

### Manual API Testing

Use the interactive docs at `http://localhost:8000/docs` or test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Get applicants (requires auth)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/ingest/applicants
```

### Seed Data Testing

After seeding the database, these applicants will have `user_id: "seed_user"`. To use them:

1. Login via Google OAuth
2. Get your real user_id from `/users/me`
3. Update seed data:
   ```javascript
   // In MongoDB shell or Compass
   db.applicants.updateMany(
     { user_id: "seed_user" },
     { $set: { user_id: "your-real-user-id" } }
   )
   ```

## Production Deployment

### Security Checklist

- [ ] Use strong `SECRET_KEY` (minimum 32 characters)
- [ ] Set `HTTPS` redirect URIs in Google OAuth
- [ ] Enable MongoDB authentication
- [ ] Use environment-specific `.env` files
- [ ] Set `CORS` to specific origins (not `*`)
- [ ] Enable rate limiting on API
- [ ] Use secure cookies for JWT (HttpOnly, Secure, SameSite)
- [ ] Implement proper logging (avoid logging secrets)

### Deployment Options

**Backend:**
- Railway, Render, or AWS EC2
- Use MongoDB Atlas for managed database
- Set environment variables in platform settings

**Frontend:**
- Vercel, Netlify, or AWS S3 + CloudFront
- Update `VITE_API_BASE_URL` to production backend URL
- Build: `npm run build`

## License

MIT

## Support

For issues and questions:
- Create an issue on GitHub
- Check API documentation at `/docs`
- Review logs: backend console and browser DevTools

---

Built with ❤️ for financial inclusion in the gig economy
