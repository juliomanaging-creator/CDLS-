# CDLS Platform - Next Steps & Setup Guide

## 📋 What You Have

The platform codebase is complete with:

| Component | Status | Files |
|-----------|--------|-------|
| **Backend API** | ✅ Complete | 5 modules, security middleware, database utils |
| **Frontend UI** | ✅ Complete | 5 React components, API service, auth hooks |
| **Database** | ✅ Complete | Full schema with 20+ tables |
| **Security** | ✅ Complete | JWT, RBAC, rate limiting, input validation |
| **Documentation** | ✅ Complete | README, SECURITY.md, this guide |

---

## 🚀 Step 1: Download the Project

### Option A: Download as ZIP
1. I'll create a downloadable package for you
2. Extract to your local development folder

### Option B: Copy Files Manually
Copy the `/home/claude/cdls-platform` directory structure to your machine.

---

## 🛠️ Step 2: Set Up Your Local Environment

### Prerequisites

```bash
# Check Node.js (need v18+)
node --version

# Check npm
npm --version

# Check PostgreSQL (need v14+)
psql --version
```

### Install PostgreSQL (if needed)

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

---

## 🗄️ Step 3: Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE cdls_platform;
CREATE USER cdls_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE cdls_platform TO cdls_user;

# Exit
\q
```

---

## ⚙️ Step 4: Configure Environment

### Backend (.env file)

Create `backend/.env`:

```bash
# Server
NODE_ENV=development
PORT=3001

# Database
DATABASE_URL=postgresql://cdls_user:your_secure_password@localhost:5432/cdls_platform
DB_SSL=false

# Authentication (generate secure random strings)
JWT_SECRET=your-super-secret-jwt-key-at-least-32-characters
JWT_EXPIRES_IN=24h
REFRESH_TOKEN_EXPIRES_IN=7d

# Encryption (exactly 32 characters)
ENCRYPTION_KEY=12345678901234567890123456789012

# AWS S3 (for document storage)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=cdls-documents-dev
AWS_REGION=us-west-2

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env file)

Create `frontend/.env`:

```bash
VITE_API_URL=http://localhost:3001/api/v1
```

---

## 📦 Step 5: Install Dependencies

```bash
# Backend
cd backend
npm install

# Frontend
cd ../frontend
npm install
```

---

## 🗃️ Step 6: Run Database Migrations

```bash
cd backend

# Run the migration SQL file
psql -U cdls_user -d cdls_platform -f ../database/migrations/001_initial_schema.sql

# Or if using node-pg-migrate
npm run migrate
```

---

## 🏃 Step 7: Start the Application

### Terminal 1 - Backend:
```bash
cd backend
npm run dev

# Should see:
# ╔════════════════════════════════════════════════════════════╗
# ║           CDLS Platform API Server Started                 ║
# ╚════════════════════════════════════════════════════════════╝
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev

# Should see:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:5173/
```

### Access the Application:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:3001
- **Health Check:** http://localhost:3001/health

---

## 🔄 Step 8: Integrate with Your Existing Files

### If you have an existing CDLS document (Word/PDF):

The unified vision document we created earlier (`CDLS_Unified_Platform_Vision.docx`) contains the business context. To integrate:

1. **Keep the business document** for stakeholder presentations
2. **Use this codebase** for the actual platform implementation
3. **Update contacts/values** in the seed data to match your document

### Update Seed Data:

Edit `database/seeds/001_initial_data.sql` to include your specific:
- Organization details
- Key contacts (Brian Maas, Tony Callaway, etc.)
- Initial deal room templates
- Calculator default values

---

## 🧪 Step 9: Test the System

### API Health Check:
```bash
curl http://localhost:3001/health
# Should return: {"status":"healthy",...}
```

### Create Test User (via API):
```bash
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "firstName": "Test",
    "lastName": "User"
  }'
```

### Run Automated Tests:
```bash
cd backend
npm test
```

---

## 🚢 Step 10: Production Deployment

### Option A: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# This starts:
# - PostgreSQL database
# - Backend API (port 3001)
# - Frontend (port 80)
```

### Option B: Cloud Deployment

**AWS (Recommended for S3 integration):**
1. RDS for PostgreSQL
2. ECS or Elastic Beanstalk for Node.js
3. S3 for documents (already configured)
4. CloudFront for frontend CDN

**Heroku (Quick start):**
```bash
# Backend
heroku create cdls-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main

# Frontend (Vercel/Netlify recommended)
vercel deploy
```

---

## 📁 File Structure Reference

```
cdls-platform/
├── backend/
│   ├── src/
│   │   ├── app.js                    # Main Express app
│   │   ├── config/index.js           # Environment config
│   │   ├── middleware/security.js    # Auth, rate limiting
│   │   ├── modules/
│   │   │   ├── dealRooms.js          # Deal room CRUD + documents
│   │   │   ├── engagementAnalytics.js # Event tracking
│   │   │   ├── roiCalculators.js     # Calculation engine
│   │   │   ├── stakeholderMapping.js # Org charts
│   │   │   └── mutualActionPlans.js  # Task management
│   │   └── utils/database.js         # Secure DB queries
│   ├── package.json
│   └── .env                          # YOUR CONFIG HERE
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DealRoom.jsx
│   │   │   ├── EngagementDashboard.jsx
│   │   │   ├── ROICalculator.jsx
│   │   │   ├── StakeholderMap.jsx
│   │   │   └── MutualActionPlan.jsx
│   │   ├── services/api.js           # API client
│   │   └── hooks/useAuth.jsx         # Auth state
│   ├── package.json
│   └── .env                          # YOUR CONFIG HERE
│
├── database/
│   ├── migrations/
│   │   └── 001_initial_schema.sql    # Full database schema
│   └── seeds/
│       └── 001_initial_data.sql      # Sample data
│
├── docker-compose.yml                # Container orchestration
├── README.md                         # Project overview
├── SECURITY.md                       # Security documentation
└── SETUP_GUIDE.md                    # This file
```

---

## ❓ Common Issues & Solutions

### Issue: "Cannot connect to database"
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection string in .env
psql $DATABASE_URL
```

### Issue: "JWT secret too short"
Your `JWT_SECRET` must be at least 32 characters.

### Issue: "S3 upload fails"
1. Check AWS credentials in .env
2. Verify bucket exists and permissions are correct
3. For local dev, you can use MinIO as S3 alternative

### Issue: "CORS error in browser"
Add your frontend URL to `CORS_ORIGINS` in backend .env.

---

## 📞 What To Do Next

1. **Set up local environment** (Steps 2-7)
2. **Test the API** (Step 9)
3. **Customize seed data** with your contacts and templates
4. **Build frontend pages** using the provided components
5. **Deploy to staging** for stakeholder demo

---

## 🎯 Quick Commands Reference

```bash
# Start everything (development)
cd backend && npm run dev &
cd frontend && npm run dev &

# Run tests
cd backend && npm test

# Database operations
npm run migrate        # Run migrations
npm run migrate:down   # Rollback
npm run seed          # Load sample data

# Production build
cd frontend && npm run build

# Docker
docker-compose up -d   # Start containers
docker-compose logs -f # View logs
docker-compose down    # Stop containers
```

---

*Need help? Check the README.md and SECURITY.md for additional documentation.*
