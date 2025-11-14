# Zoadra.com Documentation Site - Installation & Deployment Guide

Complete guide for installing, running, and deploying the Singularis documentation website.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Building for Production](#building-for-production)
4. [Deployment to Namecheap cPanel](#deployment-to-namecheap-cpanel)
5. [Deployment to Netlify](#deployment-to-netlify-alternative)
6. [Troubleshooting](#troubleshooting)
7. [Customization](#customization)

---

## Prerequisites

### Required Software

- **Node.js 18+** and **npm 9+**
  - Download: https://nodejs.org/
  - Check versions:
    ```bash
    node --version   # Should be v18.0.0 or higher
    npm --version    # Should be 9.0.0 or higher
    ```

- **Git** (optional, for cloning)
  - Download: https://git-scm.com/

### Windows-Specific: Enable PowerShell Scripts

If you're on Windows, you may need to enable script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Local Development Setup

### Step 1: Navigate to Project

```bash
cd d:\Projects\Singularis\zoadra-docs
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install:
- React 18
- Vite 5
- React Router DOM
- Tailwind CSS
- Lucide React (icons)
- PostCSS & Autoprefixer

**Expected output:**
```
added 245 packages in 15s
```

### Step 3: Start Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.4.21  ready in 551 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Step 4: Open in Browser

Navigate to **http://localhost:5173/**

You should see the Singularis documentation site running locally! 🎉

### Step 5: Making Changes

The dev server has **hot reload** - any changes you make will automatically refresh in the browser.

**Try editing:**
- `src/pages/Home.jsx` - Home page content
- `src/pages/Architecture.jsx` - Architecture documentation
- `src/pages/Philosophy.jsx` - Philosophical foundations
- `src/index.css` - Global styles

---

## Building for Production

### Step 1: Create Production Build

```bash
npm run build
```

**This will:**
1. Optimize React code
2. Minify JavaScript and CSS
3. Generate static HTML files
4. Output everything to `dist/` folder

**Expected output:**
```
vite v5.4.21 building for production...
✓ 245 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.30 kB
dist/assets/index-a1b2c3d4.css   15.23 kB │ gzip:  4.12 kB
dist/assets/index-e5f6g7h8.js   142.68 kB │ gzip: 45.89 kB
✓ built in 3.45s
```

### Step 2: Preview Production Build (Optional)

```bash
npm run preview
```

This runs a local server serving the production build:
```
  ➜  Local:   http://localhost:4173/
```

Test the production build before deploying!

---

## Deployment to Namecheap cPanel

### Overview

We'll deploy the static files from the `dist/` folder to your Namecheap hosting via cPanel File Manager.

### Prerequisites

- Namecheap hosting account
- Domain (zoadra.com) pointed to your hosting
- cPanel login credentials

### Step 1: Build Production Files

```bash
npm run build
```

### Step 2: Prepare Files

The `dist/` folder now contains:
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].css
│   ├── index-[hash].js
│   └── [other hashed assets]
└── [other files]
```

### Step 3: Login to cPanel

1. Go to your Namecheap hosting account
2. Click **"Manage"** next to your hosting plan
3. Click **"Go to cPanel"**
4. Login with your credentials

### Step 4: Open File Manager

1. In cPanel, find **"Files"** section
2. Click **"File Manager"**
3. Navigate to **`public_html`** (or your domain's document root)

### Step 5: Clean Document Root (First-time deployment)

If this is your first deployment:
1. Select all files in `public_html`
2. Click **"Delete"**
3. Confirm deletion

### Step 6: Upload Files

**Option A: Upload ZIP (Recommended)**

1. On your local machine, compress the `dist/` folder contents into `dist.zip`
2. In File Manager, click **"Upload"**
3. Upload `dist.zip`
4. Right-click `dist.zip` → **"Extract"**
5. Move all extracted files to `public_html` root
6. Delete `dist.zip`

**Option B: Upload Files Directly**

1. In File Manager, click **"Upload"**
2. Select ALL files from your local `dist/` folder
3. Wait for upload to complete (progress bar)

### Step 7: Create .htaccess for React Router

Create a new file named `.htaccess` in `public_html`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  
  # Redirect all requests to index.html for React Router
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME} !-l
  RewriteRule . /index.html [L]
</IfModule>

# Security Headers
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set X-XSS-Protection "1; mode=block"
</IfModule>

# Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Cache Control
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType application/json "access plus 0 seconds"
  ExpiresByType text/html "access plus 0 seconds"
</IfModule>
```

### Step 8: Set Permissions

1. Select all files in `public_html`
2. Click **"Permissions"** (or **"Change Permissions"**)
3. Set:
   - **Files:** 644 (rw-r--r--)
   - **Folders:** 755 (rwxr-xr-x)
4. Check **"Recurse into subdirectories"**
5. Click **"Change Permissions"**

### Step 9: Enable SSL (HTTPS)

1. In cPanel, go to **"Security"** section
2. Click **"SSL/TLS Status"**
3. Find **zoadra.com**
4. Click **"Run AutoSSL"**
5. Wait for certificate installation (2-5 minutes)

### Step 10: Test Your Site!

1. Visit **https://zoadra.com**
2. Test all pages:
   - Home
   - Architecture
   - Infinity Engine
   - Philosophy
   - Getting Started
   - API Reference
3. Test navigation (React Router should work)
4. Check on mobile devices

### Step 11: Future Updates

When you make changes:

1. Make your edits locally
2. Test with `npm run dev`
3. Build: `npm run build`
4. Upload only changed files to cPanel
5. Clear browser cache: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)

---

## Deployment to Netlify (Alternative)

Netlify is a great alternative with automatic deployments from Git.

### Step 1: Sign Up for Netlify

1. Go to https://netlify.com
2. Sign up (free plan is sufficient)

### Step 2: Connect Repository (If using Git)

1. Click **"Add new site"** → **"Import an existing project"**
2. Connect to your Git provider (GitHub, GitLab, Bitbucket)
3. Select your repository
4. Configure:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
5. Click **"Deploy site"**

### Step 3: Manual Deploy (No Git)

1. Click **"Add new site"** → **"Deploy manually"**
2. Drag and drop your `dist/` folder
3. Wait for deployment
4. Your site is live at `https://random-name-12345.netlify.app`

### Step 4: Custom Domain

1. Go to **"Site settings"** → **"Domain management"**
2. Click **"Add custom domain"**
3. Enter `zoadra.com`
4. Follow DNS configuration instructions
5. Netlify will automatically provision SSL

### Step 5: Automatic Deployments

Netlify automatically redeploys when you:
- Push to your Git repository (if connected)
- Make changes in their UI
- Deploy via CLI

---

## Troubleshooting

### Problem: `npm install` fails

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Problem: Port 5173 already in use

**Solution:**
```bash
# Kill the process on port 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5173 | xargs kill -9

# Or use a different port:
npm run dev -- --port 3000
```

### Problem: CSS/Tailwind not working

**Solution:**
```bash
# Ensure PostCSS and Tailwind are installed
npm install -D tailwindcss postcss autoprefixer

# Restart dev server
npm run dev
```

### Problem: Routes not working after deployment (404 errors)

**Solution:**

Make sure `.htaccess` file exists in your server root with the rewrite rules (see Step 7 above).

For Netlify, create `public/_redirects`:
```
/*    /index.html   200
```

### Problem: Build fails with memory error

**Solution:**
```bash
# Increase Node.js memory limit
$env:NODE_OPTIONS="--max-old-space-size=4096"  # Windows PowerShell
export NODE_OPTIONS="--max-old-space-size=4096"  # Mac/Linux

npm run build
```

### Problem: Blank page after deployment

**Solution:**

1. Check browser console for errors (F12)
2. Verify `vite.config.js` base path:
   ```javascript
   export default defineConfig({
     base: '/',  // Should be '/' for root domain
   })
   ```
3. Rebuild: `npm run build`

### Problem: Images/assets not loading

**Solution:**

1. Make sure assets are in `public/` folder or imported in components
2. Check file paths (case-sensitive on Linux servers)
3. Verify `.htaccess` cache rules aren't blocking assets

---

## Customization

### Change Site Title

Edit `index.html`:
```html
<title>Your Site Title</title>
```

### Change Colors

Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        400: '#your-color',
        500: '#your-color',
        // ...
      },
    },
  },
},
```

### Add New Page

1. Create `src/pages/YourPage.jsx`:
```javascript
export default function YourPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-20">
      <h1>Your Page Title</h1>
      {/* Your content */}
    </div>
  )
}
```

2. Add route in `src/App.jsx`:
```javascript
import YourPage from './pages/YourPage'

// In Routes:
<Route path="/your-page" element={<YourPage />} />
```

3. Add navigation link in `src/components/Layout.jsx`

### Change Font

Edit `src/index.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=Your+Font&display=swap');
```

Then update `tailwind.config.js`:
```javascript
fontFamily: {
  sans: ['Your Font', 'sans-serif'],
},
```

---

## Performance Optimization

### Enable Gzip Compression

Already included in `.htaccess` above.

### Optimize Images

```bash
# Install image optimization
npm install -D vite-plugin-imagemin

# Add to vite.config.js
import viteImagemin from 'vite-plugin-imagemin'

plugins: [
  react(),
  viteImagemin({
    gifsicle: { optimizationLevel: 7 },
    mozjpeg: { quality: 80 },
    pngquant: { quality: [0.8, 0.9] },
    svgo: { plugins: [{ name: 'removeViewBox', active: false }] },
  }),
],
```

### Code Splitting

Already handled by Vite automatically!

---

## Maintenance

### Regular Updates

```bash
# Update dependencies
npm update

# Check for outdated packages
npm outdated

# Update specific package
npm install package-name@latest
```

### Backup

Before major updates, backup:
1. Your `src/` folder (source code)
2. `package.json` and `package-lock.json`
3. Your `dist/` folder (last known good build)

---

## Support

### Official Documentation

- **Vite:** https://vitejs.dev/
- **React:** https://react.dev/
- **Tailwind CSS:** https://tailwindcss.com/
- **React Router:** https://reactrouter.com/

### Useful Commands

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm install      # Install dependencies
npm update       # Update dependencies
```

---

## Success Checklist

- [ ] Node.js 18+ installed
- [ ] Dependencies installed (`npm install`)
- [ ] Dev server works (`npm run dev`)
- [ ] Production build works (`npm run build`)
- [ ] Files uploaded to cPanel
- [ ] `.htaccess` configured
- [ ] SSL certificate installed
- [ ] All pages load correctly
- [ ] Navigation works (no 404s)
- [ ] Mobile responsive
- [ ] Fast load times (<3 seconds)

---

## Next Steps

1. ✅ Install and run locally
2. ✅ Test all pages
3. ✅ Build for production
4. ✅ Deploy to cPanel or Netlify
5. ✅ Configure SSL
6. ✅ Test live site
7. 🎉 Share your documentation site!

---

**Congratulations!** Your Singularis documentation site is now live! 🚀

For questions or issues, consult the troubleshooting section above or check the official Vite/React documentation.
