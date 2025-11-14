# Quick Start - Zoadra.com Documentation Site

> **5-minute setup guide** for the Singularis documentation website

---

## Prerequisites

- **Node.js 18+** - https://nodejs.org/
- **npm 9+** (comes with Node.js)

Check versions:
```bash
node --version && npm --version
```

---

## Local Development (3 steps)

### 1. Install Dependencies
```bash
cd d:\Projects\Singularis\zoadra-docs
npm install
```

### 2. Start Dev Server
```bash
npm run dev
```

### 3. Open Browser
Navigate to **http://localhost:5173/**

✅ Done! The site is running locally.

---

## Production Build

```bash
npm run build
```

Output: `dist/` folder with optimized static files

---

## Deploy to cPanel (6 steps)

### 1. Build
```bash
npm run build
```

### 2. Login to cPanel
- Go to Namecheap → Hosting → cPanel

### 3. Open File Manager
- Navigate to `public_html`

### 4. Upload Files
- Upload all files from `dist/` folder

### 5. Create `.htaccess`
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

### 6. Test
Visit **https://zoadra.com**

---

## Deploy to Netlify (Alternative)

### Drag & Drop Method
1. Build: `npm run build`
2. Go to https://netlify.com
3. Drag `dist/` folder
4. Done!

### Git Method
1. Push code to GitHub
2. Connect Netlify to repo
3. Set build command: `npm run build`
4. Set publish directory: `dist`
5. Deploy!

---

## Common Commands

```bash
npm run dev      # Development server (http://localhost:5173)
npm run build    # Production build → dist/
npm run preview  # Preview production build
npm install      # Install dependencies
```

---

## Troubleshooting

### Port already in use?
```bash
npm run dev -- --port 3000
```

### CSS not working?
```bash
npm install -D tailwindcss postcss autoprefixer
npm run dev
```

### Routes return 404 after deploy?
Make sure `.htaccess` is uploaded to server root.

### Blank page after build?
Check browser console (F12) for errors.

---

## File Structure

```
zoadra-docs/
├── src/
│   ├── pages/          # Page components
│   ├── components/     # Shared components
│   ├── App.jsx         # Routes
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles
├── public/             # Static assets
├── dist/               # Build output (after npm run build)
├── index.html          # HTML template
├── package.json        # Dependencies
├── vite.config.js      # Vite config
└── tailwind.config.js  # Tailwind config
```

---

## What's Included

✅ **Pages:**
- Home (with Skyrim flagship feature)
- Architecture (complete system docs)
- Infinity Engine (Phase 2A/2B)
- Philosophy (ETHICA UNIVERSALIS + MATHEMATICA SINGULARIS)
- Getting Started (placeholder)
- API Reference (placeholder)

✅ **Features:**
- React 18 + Vite 5
- Tailwind CSS styling
- React Router navigation
- Dark theme
- Responsive design
- Hot reload in dev
- Optimized production build

---

## Next Steps

1. ✅ Run locally: `npm run dev`
2. ✅ Make your edits
3. ✅ Build: `npm run build`
4. ✅ Deploy to cPanel or Netlify
5. 🎉 Your site is live!

---

**Need more details?** See `INSTALLATION.md` for the comprehensive guide.

**Site running?** Visit http://localhost:5173/ 🚀
