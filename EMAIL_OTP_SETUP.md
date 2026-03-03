# Email OTP Setup Guide

## ✅ Installation Complete!

Email OTP functionality has been successfully integrated into your application.

---

## 📧 How It Works

### Current Mode: **Development Mode**
- OTP is displayed on screen (no email sent)
- Perfect for testing
- No email configuration needed

### Production Mode: **Email OTP**
- OTP is sent via email
- Requires Gmail account setup
- More secure and professional

---

## 🚀 Quick Start (Development Mode)

**Already working!** The system is in development mode by default.

1. Go to http://localhost:3000
2. Click "Send OTP"
3. OTP appears in the green message box
4. Continue...

Enter your OTP and login!

---

## 📮 Enable Real Email Sending

### Step 1: Get a Gmail App Password

1. **Go to your Google Account**
   - Visit: https://myaccount.google.com/security

2. **Enable 2-Step Verification**
   - Under "Signing in to Google", click "2-Step Verification"
   - Follow the setup process

3. **Create App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" (type "Street Light System")
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 2: Configure Your .env File

Open `.env` file in the project root and update:

```env
# Change this to true to enable email sending
EMAIL_ENABLED=true

# Your Gmail address
SMTP_USER=your-email@gmail.com

# Paste the 16-character App Password here (remove spaces)
SMTP_PASSWORD=abcdefghijklmnop

# Email address to send from (usually same as SMTP_USER)
SMTP_FROM_EMAIL=your-email@gmail.com
```

### Step 3: Restart the Backend

```powershell
# Stop the current backend (Ctrl+C in the terminal)
# Then restart:
python backend/ws_server.py
```

### Step 4: Test It!

1. Register with a **real email address**
2. Click "Send OTP"
3. Check your email inbox
4. Enter the OTP and login!

---

## 📝 Email Configuration Options

### Gmail (Recommended)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Yahoo Mail
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

### Custom SMTP Server
```env
SMTP_HOST=smtp.your-domain.com
SMTP_PORT=587
SMTP_USER=noreply@your-domain.com
SMTP_PASSWORD=your-password
SMTP_FROM_EMAIL=noreply@your-domain.com
```

---

## 🔧 Troubleshooting

### "Failed to send email" error

**Check:**
1. ✅ `EMAIL_ENABLED=true` in .env
2. ✅ App Password is correct (no spaces)
3. ✅ 2-Step Verification is enabled
4. ✅ Internet connection is working

**Gmail Specific:**
- Make sure you're using an **App Password**, not your regular password
- Check "Less secure app access" is NOT needed (App Passwords work without it)

### OTP not received

1. **Check spam/junk folder**
2. **Wait 1-2 minutes** (email can be delayed)
3. **Verify email address** is correct in registration
4. **Check backend logs** for error messages

### "Authentication failed" error

- Double-check SMTP_USER and SMTP_PASSWORD
- Regenerate App Password if needed
- Make sure you're using the correct SMTP_HOST and SMTP_PORT

---

## 🎨 Customize Email Template

Edit the email template in `backend/ws_server.py`:

Find the `send_otp_email()` function and modify the HTML template:

```python
html = f"""
<html>
  <body>
    <!-- Your custom email design here -->
    <h1>OTP: {otp}</h1>
  </body>
</html>
"""
```

---

## 🔒 Security Best Practices

✅ **DO:**
- Use App Passwords (never commit real passwords to Git)
- Keep `.env` file in `.gitignore`
- Use environment variables
- Enable 2-Step Verification

❌ **DON'T:**
- Commit `.env` file to version control
- Share your SMTP_PASSWORD
- Use your regular Gmail password
- Disable 2-Step Verification

---

## 📊 Features

✅ **Beautiful HTML Email Template**
- Professional design
- Responsive layout  
- Clear OTP display

✅ **Security Features**
- 5-minute OTP expiration
- One-time use only
- Secure SMTP with TLS

✅ **Development Mode**
- Test without email setup
- OTP displayed on screen
- Easy debugging

---

## 🆘 Need Help?

**Common Questions:**

**Q: Do I need to pay for email sending?**  
A: No! Gmail's SMTP is free for personal use.

**Q: How many emails can I send?**  
A: Gmail allows ~500 emails per day (more than enough for testing).

**Q: Can I use other email providers?**  
A: Yes! Update SMTP_HOST and SMTP_PORT for your provider.

**Q: Is my password safe?**  
A: Yes! It's stored in `.env` which is not committed to Git.

---

## ✨ You're All Set!

The email OTP system is ready to use!

- **Development Mode:** Working now (no setup needed)
- **Production Mode:** Follow steps above to enable email sending

**Current Status:**
- ✅ Backend server running with email support
- ✅ Frontend ready for OTP login
- ✅ Configuration files created
- ✅ Security implemented

Happy coding! 🎉
