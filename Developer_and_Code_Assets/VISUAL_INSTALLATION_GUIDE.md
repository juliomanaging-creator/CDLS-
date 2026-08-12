# 🚀 CA Dealer Logistics Platform
## Visual Installation Guide for Windows

**Time Required:** 15 minutes  
**Difficulty:** Beginner-Friendly  
**Prerequisites:** Windows 10/11 computer

---

## 📋 What You'll Need

```
┌─────────────────────────────────────────────┐
│  ✓ Windows 10 or 11                         │
│  ✓ Internet connection                      │
│  ✓ 500 MB free disk space                   │
│  ✓ The downloaded ev-cost-platform.zip      │
└─────────────────────────────────────────────┘
```

---

## 🎯 Installation Overview

```
Step 1: Install Node.js  →  Step 2: Extract Files  →  Step 3: Setup Environment
       (5 min)                     (2 min)                   (3 min)
                                                                ↓
                         Step 5: Open Website  ←  Step 4: Install & Start
                               (1 min)                   (5 min)
```

---

## STEP 1: Install Node.js (The Engine) ⚙️

### 1.1 Download Node.js

```
┌──────────────────────────────────────────────────────────┐
│  Browser Address Bar:                                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │  https://nodejs.org                                │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  You'll see a page like this:                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │                                                     │  │
│  │           Node.js®                                  │  │
│  │                                                     │  │
│  │   ┌─────────────────┐  ┌─────────────────┐        │  │
│  │   │  20.11.0 LTS    │  │  21.5.0 Current │        │  │
│  │   │  Recommended    │  │                 │        │  │
│  │   │   [Download] ← CLICK THIS ONE!       │        │  │
│  │   └─────────────────┘  └─────────────────┘        │  │
│  │                                                     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Why Node.js?**  
Think of it as the engine that makes the application run (like Chrome runs websites, Node.js runs our server).

### 1.2 Run the Installer

```
┌──────────────────────────────────────────────────┐
│  Your Downloads Folder:                          │
│  ┌────────────────────────────────────────────┐  │
│  │  📁 node-v20.11.0-x64.msi                  │  │
│  │     ↑                                       │  │
│  │     Double-click this file                 │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘

         Windows will show:
         ┌────────────────────────────────────┐
         │  Do you want to allow this app to  │
         │  make changes to your device?      │
         │                                    │
         │    [Yes] ← Click    [No]           │
         └────────────────────────────────────┘
```

### 1.3 Installation Wizard

```
Screen 1:                        Screen 2:
┌─────────────────────────┐      ┌─────────────────────────┐
│ Welcome to Node.js      │      │ License Agreement       │
│ Setup Wizard            │      │                         │
│                         │      │ ☑ I accept the terms   │
│                         │      │                         │
│    [Next >] ← Click     │      │    [Next >] ← Click     │
└─────────────────────────┘      └─────────────────────────┘

Screen 3:                        Screen 4:
┌─────────────────────────┐      ┌─────────────────────────┐
│ Destination Folder      │      │ Ready to Install        │
│                         │      │                         │
│ C:\Program Files\nodejs │      │ Click Install to begin  │
│                         │      │                         │
│    [Next >] ← Click     │      │    [Install] ← Click    │
└─────────────────────────┘      └─────────────────────────┘

⏳ Installation Progress:
┌─────────────────────────────────────┐
│ Installing Node.js...               │
│ ████████████████░░░░░░░░░░ 65%     │
│                                     │
│ Please wait...                      │
└─────────────────────────────────────┘

✓ Complete!
┌─────────────────────────────────────┐
│ Setup Wizard Completed              │
│                                     │
│ Node.js has been successfully       │
│ installed on your computer.         │
│                                     │
│    [Finish]                         │
└─────────────────────────────────────┘
```

### 1.4 Verify Installation

Press **Windows Key + R**, type `cmd`, press Enter.

```
┌────────────────────────────────────────────────────┐
│  Command Prompt                              [_][□][X] │
├────────────────────────────────────────────────────┤
│ Microsoft Windows [Version 10.0.19045.0693]        │
│ (c) Microsoft Corporation. All rights reserved.    │
│                                                    │
│ C:\Users\YourName> node --version                 │
│ v20.11.0                          ← You should see this!
│                                                    │
│ C:\Users\YourName> npm --version                  │
│ 10.2.4                            ← And this!     │
│                                                    │
│ C:\Users\YourName> _                              │
└────────────────────────────────────────────────────┘
```

✅ **If you see version numbers, Node.js is installed correctly!**  
❌ **If you see "not recognized", restart your computer and try again.**

---

## STEP 2: Extract Your Files 📦

### 2.1 Create a Simple Project Folder

```
Open File Explorer:
┌────────────────────────────────────────────────────────────┐
│  This PC                                            [_][□][X]│
├────────────────────────────────────────────────────────────┤
│  ← → ↑  📁 This PC                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📁 Local Disk (C:)  ← Click here                         │
│      └─ 💾 500 GB free of 1 TB                            │
│                                                            │
│  📁 OneDrive                                               │
│  📁 Desktop                                                │
│  📁 Documents                                              │
│  📁 Downloads                                              │
└────────────────────────────────────────────────────────────┘

Now in C:\ drive:
┌────────────────────────────────────────────────────────────┐
│  Local Disk (C:)                                    [_][□][X]│
├────────────────────────────────────────────────────────────┤
│  Home  Share  View                                         │
│  [New folder] ← Click this                                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📁 Program Files                                          │
│  📁 Program Files (x86)                                    │
│  📁 Users                                                  │
│  📁 Windows                                                │
│  📁 New folder  ← Rename this to "Projects"               │
│                                                            │
└────────────────────────────────────────────────────────────┘

Result:
  C:\Projects\  ✓ Created!
```

### 2.2 Extract the ZIP File

```
Step 1: Find Your Downloaded ZIP
┌────────────────────────────────────────────────────────────┐
│  Downloads                                          [_][□][X]│
├────────────────────────────────────────────────────────────┤
│  Name                     Date modified        Type        │
├────────────────────────────────────────────────────────────┤
│  📦 ev-cost-platform.zip  12/16/2024 10:30 PM  ZIP (45 KB)│
│      ↑                                                     │
│      Right-click here                                     │
└────────────────────────────────────────────────────────────┘

Step 2: Right-Click Menu Appears
┌─────────────────────────┐
│  Open                   │
│  Extract All...    ← Click this!
│  Extract to ev-cost...  │
│  ──────────────────     │
│  Cut                    │
│  Copy                   │
│  Delete                 │
└─────────────────────────┘

Step 3: Choose Destination
┌──────────────────────────────────────────────┐
│  Extract Compressed (Zipped) Folders         │
├──────────────────────────────────────────────┤
│  Files will be extracted to this folder:     │
│  ┌────────────────────────────────────────┐  │
│  │ C:\Projects\ev-cost-platform           │  │
│  └────────────────────────────────────────┘  │
│                            [Browse...]        │
│                                              │
│  ☑ Show extracted files when complete       │
│                                              │
│           [Extract] ← Click                  │
└──────────────────────────────────────────────┘

✓ Extraction Complete!
┌────────────────────────────────────────────────────────────┐
│  ev-cost-platform                                   [_][□][X]│
├────────────────────────────────────────────────────────────┤
│  Name                     Type                              │
├────────────────────────────────────────────────────────────┤
│  📁 controllers           File folder                       │
│  📁 middleware            File folder                       │
│  📁 public                File folder                       │
│  📁 routes                File folder                       │
│  📄 .env.example          ENV File                          │
│  📄 package.json          JSON File                         │
│  📄 README.md             MD File                           │
│  📄 server.js             JS File                           │
└────────────────────────────────────────────────────────────┘
```

---

## STEP 3: Setup Environment (Config File) ⚙️

### 3.1 Open Command Prompt in Project Folder

```
In File Explorer (at C:\Projects\ev-cost-platform):
┌────────────────────────────────────────────────────────────┐
│  ev-cost-platform                                   [_][□][X]│
├────────────────────────────────────────────────────────────┤
│  📁 C:\Projects\ev-cost-platform     [🔍 Search]           │
├────────────────────────────────────────────────────────────┤
│              ↓ Click in this address bar                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  C:\Projects\ev-cost-platform                        │  │
│  └──────────────────────────────────────────────────────┘  │
│  Type "cmd" and press Enter                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  cmd                                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘

This opens Command Prompt in the right folder!
┌────────────────────────────────────────────────────┐
│  Command Prompt                              [_][□][X] │
├────────────────────────────────────────────────────┤
│ C:\Projects\ev-cost-platform> _                   │
│                                                    │
│ ✓ You're in the right place!                      │
└────────────────────────────────────────────────────┘
```

### 3.2 Create .env File

Type this command:
```cmd
copy .env.example .env
```

```
┌────────────────────────────────────────────────────┐
│ C:\Projects\ev-cost-platform> copy .env.example .env
│         1 file(s) copied.                          │
│                                                    │
│ C:\Projects\ev-cost-platform> _                   │
└────────────────────────────────────────────────────┘

✓ .env file created!
```

### 3.3 Edit .env File

Type:
```cmd
notepad .env
```

```
Notepad Opens:
┌──────────────────────────────────────────────────────────┐
│  .env - Notepad                                   [_][□][X]│
├──────────────────────────────────────────────────────────┤
│  File  Edit  Format  View  Help                          │
├──────────────────────────────────────────────────────────┤
│  # Server Configuration                                  │
│  NODE_ENV=development                                    │
│  PORT=3000                                               │
│  HOST=localhost                                          │
│                                                          │
│  # Database Configuration                                │
│  DB_HOST=localhost                                       │
│  DB_PORT=5432                                            │
│  DB_NAME=ca_dealer_logistics                             │
│  DB_USER=your_db_user                                    │
│  DB_PASSWORD=your_secure_password                        │
│  DB_SSL=true                                             │
│                                                          │
│  # Security                                              │
│  JWT_SECRET=your_super_secret_jwt_key_change_this       │
│  JWT_EXPIRE=7d                                           │
│                                                          │
│  # Session Secret                                        │
│  SESSION_SECRET=your_super_secret_session_key_change    │
│                                                          │
│  # CORS                                                  │
│  CORS_ORIGIN=http://localhost:3000                       │
└──────────────────────────────────────────────────────────┘
```

### 3.4 Change These Lines (IMPORTANT!)

```
BEFORE (example):                   AFTER (your settings):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JWT_SECRET=your_super_secret...  →  JWT_SECRET=julio-sacramento-2025-secret-key-min-32-chars
SESSION_SECRET=your_super_secret →  SESSION_SECRET=another-random-secret-session-2025-change

Keep these as-is:
✓ NODE_ENV=development
✓ PORT=3000
✓ CORS_ORIGIN=http://localhost:3000

Database settings (we'll use mock data for now, so these can stay):
✓ DB_HOST=localhost
✓ DB_USER=your_db_user
✓ DB_PASSWORD=your_secure_password
```

**Save:** Press `Ctrl + S`  
**Close:** Press `Alt + F4` or click X

---

## STEP 4: Install Packages & Start Server 🚀

### 4.1 Install All Required Packages

In Command Prompt, type:
```cmd
npm install
```

```
┌────────────────────────────────────────────────────────────┐
│ C:\Projects\ev-cost-platform> npm install                 │
│                                                            │
│ npm notice New minor version of npm available! 11.0.2...  │
│                                                            │
│ added 1 package in 2s                                     │
│ added 15 packages in 5s                                   │
│ added 47 packages in 12s                                  │
│ added 123 packages in 28s                                 │
│ added 198 packages in 54s                                 │
│ added 245 packages in 1m 47s                              │
│                                                            │
│ 15 packages are looking for funding                       │
│   run `npm fund` for details                              │
│                                                            │
│ found 0 vulnerabilities                    ← Great!       │
│                                                            │
│ C:\Projects\ev-cost-platform> _                           │
└────────────────────────────────────────────────────────────┘

This downloads all 245 packages we discussed!
Progress bar visualization:
[████████████████████████████████] 100% - Complete!
```

**⏰ This takes 2-3 minutes. Be patient!**

### 4.2 Start the Server!

Type:
```cmd
npm start
```

```
┌────────────────────────────────────────────────────────────┐
│ C:\Projects\ev-cost-platform> npm start                   │
│                                                            │
│ > ca-dealer-logistics-platform@1.0.0 start                │
│ > node server.js                                          │
│                                                            │
│ ╔═══════════════════════════════════════════════════════╗ │
│ ║   CA Dealer Logistics Platform - Server Running      ║ │
│ ║   Environment: development                            ║ │
│ ║   Port: 3000                                          ║ │
│ ║   URL: http://localhost:3000                          ║ │
│ ╚═══════════════════════════════════════════════════════╝ │
│                                                            │
│ ✓ Server ready!                                           │
│ ⚡ Keep this window open while using the website         │
└────────────────────────────────────────────────────────────┘

🎉 SUCCESS! Your server is running!
```

**⚠️ IMPORTANT: Keep this Command Prompt window open!**  
If you close it, the website stops working.

---

## STEP 5: Open Your Website! 🌐

### 5.1 Open Your Browser

```
Click any browser icon:
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│ Edge │  │Chrome│  │Firefox│ │Brave │
│  🌐  │  │  🌐  │  │  🦊  │  │  🦁  │
└──────┘  └──────┘  └──────┘  └──────┘
   ↑ Click any of these
```

### 5.2 Type the Address

```
┌──────────────────────────────────────────────────────────┐
│  Browser                                          [_][□][X]│
├──────────────────────────────────────────────────────────┤
│  ← → ⟳  [🔒] localhost:3000                    [⭐] [☰]  │
│          ↑ Type this and press Enter                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Loading...                                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 5.3 See Your Dashboard! 🎉

```
┌──────────────────────────────────────────────────────────────────┐
│  CA Dealer Logistics - localhost:3000                    [_][□][X]│
├──────────────────────────────────────────────────────────────────┤
│  ══════════════════════════════════════════════════════════      │
│  🚗 CA Dealer Logistics    Dashboard | Cost Calculator | Cities  │
│  ══════════════════════════════════════════════════════════      │
│                                                                  │
│  Fleet Cost Dashboard                                            │
│  Real-time comparison of diesel vs. electric vehicle costs      │
│                                                                  │
│  ┌───────────────────┐  ┌───────────────────┐                   │
│  │ ⚡ Avg EV Savings │  │ ⛽ Avg Diesel     │                   │
│  │    $29.83         │  │    $5.01/gal     │                   │
│  │    +35.7%         │  │    per gallon    │                   │
│  └───────────────────┘  └───────────────────┘                   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Cost Comparison Trend                                  │    │
│  │  📊 [Chart showing diesel vs EV costs over time]        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Recent Calculations                                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Date       Route              Diesel   EV      Savings   │   │
│  │ 12/16/24   Sacramento-Modesto $83.63   $53.80  $29.83   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

✓ IT WORKS! 🎊
```

---

## 🎮 What You Can Do Now

### Navigate Around

```
Top Menu:
┌─────────────────────────────────────────────────────────┐
│  Dashboard | Cost Calculator | City Pricing | Routes   │
│      ↑          ↑                  ↑            ↑       │
│   Click any of these to explore                        │
└─────────────────────────────────────────────────────────┘
```

### Try the Cost Calculator

```
1. Click "Cost Calculator"
2. Fill in the form:
   ┌─────────────────────────────────────────┐
   │ Origin:      [Sacramento       ▼]       │
   │ Destination: [Modesto          ▼]       │
   │ Distance:    [127.4 miles        ]      │
   │ Vehicles:    [7 vehicles         ]      │
   │                                         │
   │ Diesel Vehicle:  [Ford F-550    ▼]      │
   │ EV Vehicle:      [BrightDrop    ▼]      │
   │                                         │
   │        [Calculate Cost Comparison]      │
   └─────────────────────────────────────────┘

3. See the results:
   ┌─────────────────────────────────────────┐
   │  DIESEL: $83.63  |  EV: $53.80         │
   │  💰 EV SAVES: $29.83 (35.7%)           │
   └─────────────────────────────────────────┘
```

---

## 🛑 How to Stop the Server

When you're done for the day:

```
Go to the Command Prompt window:
┌────────────────────────────────────────────────────┐
│  Command Prompt                              [_][□][X] │
├────────────────────────────────────────────────────┤
│ ╔═══════════════════════════════════════════════╗ │
│ ║   CA Dealer Logistics Platform - Running     ║ │
│ ╚═══════════════════════════════════════════════╝ │
│                                                    │
│ Press Ctrl + C to stop...                         │
└────────────────────────────────────────────────────┘

Press: Ctrl + C

You'll see:
┌────────────────────────────────────────────────────┐
│ ^C                                                 │
│ Terminate batch job (Y/N)? Y                      │
│                                                    │
│ C:\Projects\ev-cost-platform> _                   │
└────────────────────────────────────────────────────┘

✓ Server stopped! Website no longer accessible.
```

---

## 🔄 How to Start Again Later

Next time you want to use the platform:

```
Step 1: Open Command Prompt
  Press Windows Key + R
  Type: cmd
  Press Enter

Step 2: Navigate to project
  cd C:\Projects\ev-cost-platform

Step 3: Start server
  npm start

Step 4: Open browser
  Go to localhost:3000

That's it! No need to reinstall anything.
```

---

## ❓ Troubleshooting Common Issues

### Issue 1: "npm is not recognized"

```
Problem:
C:\Projects\ev-cost-platform> npm install
'npm' is not recognized as an internal or external command...

Solution:
1. Node.js not installed correctly
2. Restart your computer
3. Reinstall Node.js from nodejs.org
4. Try again
```

### Issue 2: Port 3000 Already in Use

```
Problem:
Error: listen EADDRINUSE: address already in use :::3000

Solution:
Something else is using port 3000.

Option A: Use different port
  Edit .env file:
  PORT=3001
  
  Then access at: localhost:3001

Option B: Stop the other program
  Task Manager → Find node.exe → End Task
```

### Issue 3: Website Won't Load

```
Problem:
Browser shows: "This site can't be reached"

Checklist:
□ Is Command Prompt still open?
□ Does it show the "Server Running" message?
□ Did you type localhost:3000 correctly? (no spaces, no www)
□ Try: 127.0.0.1:3000 instead
```

### Issue 4: Files Not Found During npm install

```
Problem:
npm ERR! ENOENT: no such file or directory

Solution:
You're in the wrong folder!

Check your location:
C:\Projects\ev-cost-platform> _  ← Should look like this

If it says something else:
cd C:\Projects\ev-cost-platform
npm install
```

---

## 📊 Installation Success Checklist

Before you consider installation complete:

```
□ Node.js installed (node --version shows v20.x.x)
□ Files extracted to C:\Projects\ev-cost-platform
□ .env file created and edited
□ npm install completed (245 packages, 0 vulnerabilities)
□ npm start shows "Server Running" message
□ Browser shows dashboard at localhost:3000
□ Can click around and see different pages
□ Cost calculator works (shows results)
```

If all checkboxes are ✓, congratulations! 🎉

---

## 📚 Next Steps After Installation

### Learn the Platform

1. **Explore the Dashboard** - See overview metrics
2. **Try Cost Calculator** - Compare diesel vs EV costs
3. **Browse City Pricing** - Check rates in different cities
4. **Review Documentation** - Open README.md file

### Customize for Your Business

1. **Add Your Dealer Locations** - In future updates
2. **Create Routes** - Your actual delivery routes
3. **Track Calculations** - Build history over time

### For Production Use

When ready to deploy for real:
1. Set up PostgreSQL database
2. Configure external API keys (GasBuddy, PlugShare)
3. Get SSL certificate for HTTPS
4. Deploy to cloud server (AWS, Heroku, etc.)

---

## 💡 Pro Tips

### Keyboard Shortcuts

```
Command Prompt:
  Ctrl + C          Stop the server
  Ctrl + V          Paste (right-click also works)
  ↑ Arrow Key       Previous command
  Tab              Auto-complete folder names

Browser:
  Ctrl + R          Refresh page
  Ctrl + Shift + R  Hard refresh (clear cache)
  F12              Developer tools
```

### Quick Commands Reference

```
# Navigate to project
cd C:\Projects\ev-cost-platform

# Install packages
npm install

# Start server
npm start

# Stop server
Ctrl + C

# Update packages
npm update

# Check for security issues
npm audit
```

---

## 🆘 Getting Help

### If You're Stuck

1. **Check this guide** - Search for your error message
2. **Read README.md** - In your project folder
3. **Check Command Prompt** - Errors show there first
4. **Try Browser Console** - Press F12 → Console tab

### Error Messages to Look For

```
✓ Good Messages:
  "Server Running" - Perfect!
  "found 0 vulnerabilities" - Secure!
  "added 245 packages" - Complete!

⚠ Warning (Usually OK):
  "npm notice" - Just informational
  "npm warn" - Not critical
  "deprecated" - Old package (still works)

❌ Errors (Need Fixing):
  "npm ERR!" - Something failed
  "ENOENT" - File not found
  "EADDRINUSE" - Port already used
  "not recognized" - Program not installed
```

---

## 🎯 Summary

```
Installation Flow:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Install Node.js  →  Provides the engine            │
│         ↓                                               │
│  2. Extract Files  →  Get the application code         │
│         ↓                                               │
│  3. Setup .env  →  Configure settings                  │
│         ↓                                               │
│  4. npm install  →  Download 245 packages              │
│         ↓                                               │
│  5. npm start  →  Launch the server                    │
│         ↓                                               │
│  6. localhost:3000  →  Use the website! 🎉            │
│                                                         │
└─────────────────────────────────────────────────────────┘

Total Time: ~15 minutes
Difficulty: ★★☆☆☆ (Easy-Moderate)
```

---

## 🎊 Congratulations!

If you've made it this far and see your dashboard, you've successfully:

✓ Installed a professional Node.js application  
✓ Set up enterprise-level security  
✓ Configured a full-stack web platform  
✓ Deployed a local development server  

**You're now running a production-ready cost analysis platform!**

---

**Document Version:** 1.0  
**Created:** December 2025  
**Platform:** Windows 10/11  
**For:** CA Dealer Logistics Platform

---

Need more help? Take a screenshot and share what you see!
