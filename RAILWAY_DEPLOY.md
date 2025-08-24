# 🚂 Railway Deployment Guide for BR Journal

## Quick Deploy to Railway

### 1. One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/Khalxee/BR-Journal)

### 2. Manual Deploy Steps

1. **Go to [railway.app](https://railway.app)**
2. **"Start a New Project"** → **"Deploy from GitHub repo"**
3. **Select:** `Khalxee/BR-Journal`
4. **Click "Deploy Now"**

### 3. Environment Variables (Optional)

Add these in Railway Dashboard → Your Project → Variables:

```bash
SECRET_KEY=your-super-secret-key-here-make-it-very-long
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
```

### 4. Access Your Application

Your BR Journal will be available at: `https://your-project-name.railway.app`

## 🎯 What Railway Automatically Does

- ✅ Detects Django application
- ✅ Installs Python dependencies
- ✅ Runs database migrations  
- ✅ Creates sample data (first deploy only)
- ✅ Collects static files
- ✅ Starts Django server
- ✅ Provides HTTPS domain

## 📋 Default Login Credentials

After deployment, you can login with these sample accounts:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Team Member Accounts:**
- Username: `john_doe` / Password: `password123`
- Username: `jane_smith` / Password: `password123`  
- Username: `mike_wilson` / Password: `password123`

## 🔧 Post-Deployment Setup

1. **Login as admin** and change the default password
2. **Create your team members** or update existing ones
3. **Configure departments** for your organization
4. **Start creating weekly journal entries**

## 🚀 Features Available

- **Weekly Journal Entries** with status tracking
- **Department Organization**
- **Team Collaboration** with comments
- **Advanced Filtering** and search
- **Top Management Reports**
- **Summary Report Generation**
- **Responsive Design** (mobile-friendly)

## 📞 Support

For deployment issues, check:
- Railway logs in your project dashboard
- [Railway Documentation](https://docs.railway.app)
- [BR Journal Documentation](./README.md)

---

**Railway Deployment Status:** ✅ Ready to Deploy  
**Estimated Deploy Time:** 2-3 minutes  
**Auto-Setup:** Included with sample data