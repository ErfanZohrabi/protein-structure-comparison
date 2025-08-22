# 🚀 Deploy to Render.com - Complete Guide

## 📋 Prerequisites

Before deploying to Render.com, make sure you have:
- ✅ A GitHub account
- ✅ Your project code pushed to GitHub
- ✅ A Render.com account (free tier available)

## 🛠️ Deployment Files Created

I've created the following files for Render.com deployment:

### 1. `render.yaml` - Render Configuration
```yaml
services:
  - type: web
    name: protein-structure-comparison
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python backend_server.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_PORT
        value: 5001
      - key: PYTHONPATH
        value: /opt/render/project/src
```

### 2. `Procfile` - Process Definition
```
web: python backend_server.py
```

### 3. `runtime.txt` - Python Version
```
python-3.11.0
```

### 4. Updated `requirements.txt` - Optimized Dependencies
- ✅ Lightweight core dependencies for fast builds
- ⚠️ Heavy ML dependencies commented out (optional)
- 🔧 Can be enabled locally for full features

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub
```bash
# If not already done
git add .
git commit -m "Add Render.com deployment configuration"
git push origin main
```

### Step 2: Create Render Service

1. **Go to [Render.com](https://render.com)**
2. **Sign up or log in**
3. **Click "New +"**
4. **Select "Web Service"**

### Step 3: Connect Repository

1. **Connect your GitHub account**
2. **Select your repository: `protein-structure-comparison`**
3. **Choose branch: `main`**

### Step 4: Configure Service

**Basic Settings:**
- **Name**: `protein-structure-comparison` (or your preferred name)
- **Environment**: `Python`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python backend_server.py`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (deploys on every push)

### Step 5: Environment Variables (Optional)

Add these if needed:
```
FLASK_ENV=production
PYTHONPATH=/opt/render/project/src
```

### Step 6: Deploy!

1. **Click "Create Web Service"**
2. **Wait for build to complete** (5-10 minutes)
3. **Your app will be live at**: `https://your-service-name.onrender.com`

## 🎯 What to Expect

### ✅ What Works Out of the Box
- 🌐 **Web Interface**: Full HTML/CSS/JS frontend
- 🔍 **Protein Search**: UniProt ID lookup
- 📊 **Basic Analysis**: Mock data and visualizations  
- 🧬 **3D Visualization**: Molecular structure viewers
- 💻 **CLI Documentation**: Command examples and help

### ⚠️ Limited Functionality (Free Tier)
- 🤖 **ML Models**: ESMFold/AlphaFold require more resources
- 🔬 **Advanced Analysis**: PyMMseqs needs more memory
- ⏱️ **Processing Time**: Free tier has limited compute

### 🔧 To Enable Full Features
Deploy with a paid plan or run locally for:
- Real ESMFold predictions
- PyMMseqs homology search
- Advanced evolutionary analysis

## 🌐 Your Live URLs

Once deployed, your app will be available at:
- **Main App**: `https://your-service-name.onrender.com`
- **API Endpoints**: `https://your-service-name.onrender.com/api/`

### Example URLs:
```
https://protein-structure-comparison.onrender.com/
https://protein-structure-comparison.onrender.com/api/status
https://protein-structure-comparison.onrender.com/api/protein_info/P01308
```

## 🔧 Troubleshooting

### Build Fails?
- **Check build logs** in Render dashboard
- **Verify requirements.txt** is correct
- **Try deploying with basic dependencies first**

### App Not Loading?
- **Check service logs** for errors
- **Verify PORT environment variable** is set correctly
- **Make sure backend_server.py** is in root directory

### Performance Issues?
- **Free tier limitations**: 512MB RAM, limited CPU
- **Consider upgrading** to paid plan for better performance
- **Optimize dependencies** by removing unused packages

## 💡 Pro Tips

### 1. Custom Domain
- **Upgrade to paid plan** to use custom domain
- **Configure DNS** to point to Render

### 2. Environment Management
- **Use environment variables** for configuration
- **Keep secrets in Render environment vars**, not code

### 3. Monitoring
- **Check logs regularly** in Render dashboard
- **Set up health checks** if needed
- **Monitor resource usage**

### 4. Local Development
```bash
# Install full dependencies locally
pip install torch transformers fair-esm pymmseqs

# Run with full features
python protein_cli.py server --port 5001
```

## 🎉 Success!

Your protein structure comparison tool is now live on the web! 

**Share your deployment URL with others and start analyzing proteins online! 🧬✨**

---

## 📞 Need Help?

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Check Logs**: In your Render dashboard
- **GitHub Issues**: Create an issue in your repository

Happy deploying! 🚀