# Deploying Zoadra.com to Namecheap via cPanel

## Prerequisites

- Namecheap hosting account with cPanel access
- Domain `zoadra.com` pointed to your hosting
- Node.js installed locally (to build the site)

---

## Step 1: Build the Static Site Locally

Open PowerShell and navigate to the project:

```powershell
cd d:\Projects\Singularis\zoadra-docs

# Install dependencies (if not already done)
npm install

# Build the production site
npm run build
```

This creates a `dist/` folder with all static files.

---

## Step 2: Prepare Files for Upload

The `dist/` folder contains:
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── [other assets]
└── favicon.svg (if you add one)
```

**Important:** You'll upload the **contents** of the `dist/` folder, not the folder itself.

---

## Step 3: Access cPanel File Manager

1. Log in to your Namecheap hosting account
2. Go to cPanel
3. Click **File Manager** under the Files section
4. Navigate to `public_html/` (or your domain's root directory)

---

## Step 4: Clean the Public Directory

If `public_html/` has existing files:

1. Select all files/folders in `public_html/`
2. Click **Delete** (backup first if needed)
3. Confirm deletion

---

## Step 5: Upload Built Files

### Option A: Using File Manager (Recommended for small sites)

1. In File Manager, navigate to `public_html/`
2. Click **Upload** button
3. Select all files from your local `dist/` folder:
   - `index.html`
   - `assets/` folder
   - Any other files in `dist/`
4. Wait for upload to complete
5. Click "Go Back" when done

### Option B: Using Compress/Extract (Faster for many files)

1. On your local machine, compress the `dist/` folder contents:
   ```powershell
   # In PowerShell
   cd d:\Projects\Singularis\zoadra-docs\dist
   Compress-Archive -Path * -DestinationPath ..\zoadra-site.zip
   ```

2. In cPanel File Manager:
   - Navigate to `public_html/`
   - Click **Upload**
   - Upload `zoadra-site.zip`
   - Right-click the uploaded zip file
   - Select **Extract**
   - Delete the zip file after extraction

---

## Step 6: Configure .htaccess for React Router

React Router needs all routes to redirect to `index.html`. Create a `.htaccess` file:

1. In File Manager, navigate to `public_html/`
2. Click **+ File** button
3. Name it `.htaccess`
4. Right-click → **Edit**
5. Add this content:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  
  # Don't rewrite files or directories
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  
  # Rewrite everything else to index.html
  RewriteRule ^ index.html [L]
</IfModule>

# Enable GZIP compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Browser caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>

# Security headers
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set X-XSS-Protection "1; mode=block"
</IfModule>
```

6. Click **Save Changes**

---

## Step 7: Set Correct Permissions

1. In File Manager, select `public_html/`
2. Click **Permissions** button
3. Set permissions:
   - Folders: `755` (rwxr-xr-x)
   - Files: `644` (rw-r--r--)
4. Check "Recurse into subdirectories"
5. Click **Change Permissions**

---

## Step 8: Verify Domain Configuration

### Check DNS Settings:

1. Go to Namecheap Dashboard
2. Select your domain `zoadra.com`
3. Click **Manage** → **Advanced DNS**
4. Ensure you have:

```
Type: A Record
Host: @
Value: [Your hosting IP]
TTL: Automatic

Type: CNAME Record
Host: www
Value: zoadra.com
TTL: Automatic
```

### Get Your Hosting IP:

In cPanel, look for "Server Information" or "Shared IP Address"

---

## Step 9: Test Your Site

1. Visit `https://zoadra.com` (or `http://zoadra.com`)
2. Test navigation:
   - Click "Architecture" → URL should be `/architecture`
   - Refresh page → Should still work (not 404)
   - Click "Infinity Engine" → Should load correctly
3. Test on mobile device
4. Check browser console for errors (F12)

---

## Step 10: Enable SSL (HTTPS)

### Option A: Free SSL via cPanel (Let's Encrypt)

1. In cPanel, find **SSL/TLS Status** or **Let's Encrypt SSL**
2. Select `zoadra.com` and `www.zoadra.com`
3. Click **Install SSL Certificate**
4. Wait for installation (usually 1-5 minutes)

### Option B: Force HTTPS

Add to the top of your `.htaccess` file:

```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## Updating the Site

When you make changes:

1. Build locally:
   ```powershell
   cd d:\Projects\Singularis\zoadra-docs
   npm run build
   ```

2. Upload new files to `public_html/` (overwrite existing)

3. Clear browser cache or use Ctrl+F5 to see changes

---

## Troubleshooting

### Issue: 404 on page refresh

**Solution:** Check `.htaccess` file exists and has correct rewrite rules.

### Issue: Styles not loading

**Solution:** 
1. Check `assets/` folder uploaded correctly
2. Clear browser cache
3. Check file permissions (644 for files)

### Issue: Blank page

**Solution:**
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify `index.html` is in `public_html/` root
4. Check file permissions

### Issue: "Index of /" directory listing

**Solution:**
1. Ensure `index.html` is in the root of `public_html/`
2. Check cPanel → **Indexes** → Set to "No Indexing"

### Issue: Mixed content warnings (HTTP/HTTPS)

**Solution:**
1. Ensure SSL is installed
2. Add HTTPS redirect to `.htaccess`
3. Clear browser cache

---

## Performance Optimization

### Enable Gzip Compression

Already included in the `.htaccess` above, but verify in cPanel:
1. Go to **Optimize Website**
2. Select "Compress All Content"

### Enable Browser Caching

Already included in the `.htaccess` above.

### Check Page Speed

Test your site:
- Google PageSpeed Insights: https://pagespeed.web.dev/
- GTmetrix: https://gtmetrix.com/

Expected scores:
- Performance: 90+
- Accessibility: 95+
- Best Practices: 90+
- SEO: 90+

---

## File Structure on Server

After deployment, your `public_html/` should look like:

```
public_html/
├── .htaccess
├── index.html
├── assets/
│   ├── index-abc123.js
│   ├── index-def456.css
│   └── [other hashed assets]
└── favicon.svg (optional)
```

---

## Quick Reference Commands

### Build site:
```powershell
npm run build
```

### Create zip for upload:
```powershell
cd dist
Compress-Archive -Path * -DestinationPath ..\zoadra-site.zip
```

### Test locally before upload:
```powershell
npm run preview
```

---

## Support

If you encounter issues:
1. Check cPanel error logs: **Errors** section
2. Check browser console (F12)
3. Verify file permissions
4. Contact Namecheap support if server-related

---

## Checklist

- [ ] Built site locally (`npm run build`)
- [ ] Uploaded all files from `dist/` to `public_html/`
- [ ] Created `.htaccess` with rewrite rules
- [ ] Set correct file permissions (755/644)
- [ ] Configured DNS (A record + CNAME)
- [ ] Installed SSL certificate
- [ ] Tested all routes
- [ ] Verified mobile responsiveness
- [ ] Checked page speed

---

**Your site should now be live at https://zoadra.com!** 🚀
