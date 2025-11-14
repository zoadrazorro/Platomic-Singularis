# Quick Start Guide

## Step 1: Enable PowerShell Scripts

**Open PowerShell as Administrator** (Right-click PowerShell → Run as Administrator)

Run this command:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Type `Y` and press Enter when prompted.

Close the Administrator PowerShell window.

---

## Step 2: Install Dependencies

Open a **new** PowerShell window (normal, not admin) and run:

```powershell
cd d:\Projects\Singularis\zoadra-docs
npm install
```

This will install all required packages (~200MB, takes 2-3 minutes).

---

## Step 3: Start Development Server

```powershell
npm run dev
```

You should see:

```
  VITE v5.3.5  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Open your browser to:** http://localhost:5173

---

## Step 4: Make Changes

The dev server has **hot reload** - any changes you make to files will instantly appear in the browser!

Try editing:
- `src/pages/Home.jsx` - Change the homepage
- `src/index.css` - Modify styles
- `src/components/Layout.jsx` - Update navigation

---

## Step 5: Build for Production

When ready to deploy:

```powershell
npm run build
```

This creates a `dist/` folder with optimized files.

---

## Step 6: Preview Production Build

Test the production build locally:

```powershell
npm run preview
```

Opens at: http://localhost:4173

---

## Alternative: Use the Setup Script

Instead of manual steps, you can use the automated setup script:

```powershell
cd d:\Projects\Singularis\zoadra-docs
.\setup.ps1
```

This will:
1. Check Node.js installation
2. Install dependencies
3. Start the dev server automatically

---

## Troubleshooting

### "Scripts are disabled" error

Run PowerShell as Administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "npm: command not found"

Install Node.js from: https://nodejs.org/

Download the LTS version (18.x or 20.x).

### Port 5173 already in use

Kill the process:

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process -Force
```

Or use a different port:

```powershell
npm run dev -- --port 3000
```

### "Cannot find module" errors

Delete and reinstall:

```powershell
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server (http://localhost:5173) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `Ctrl+C` | Stop the dev server |

---

## What You'll See

### Home Page
- Hero section with "Singularis" gradient text
- Stats: 50+ subsystems, 8 theories
- Feature cards
- Infinity Engine highlight
- Philosophy quotes

### Navigation
- Home
- Architecture
- Infinity Engine
- Philosophy
- Getting Started
- API Reference

### Features
- Dark theme
- Responsive design
- Smooth animations
- Glass-morphism effects
- Mobile menu

---

## Next Steps

1. ✅ Run `npm install`
2. ✅ Run `npm run dev`
3. ✅ Open http://localhost:5173
4. ✅ Explore the site
5. ✅ Make changes and see them live!
6. ✅ Build with `npm run build`
7. ✅ Deploy to zoadra.com (see CPANEL_DEPLOYMENT.md)

---

**Need help?** Check the full README.md or CPANEL_DEPLOYMENT.md
