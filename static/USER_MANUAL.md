# FinanceTracker - User Manual

**Version 1.0**
**Last Updated: February 2026**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Requirements](#2-system-requirements)
3. [Getting Started](#3-getting-started)
4. [Dashboard Overview](#4-dashboard-overview)
5. [Managing Transactions](#5-managing-transactions)
6. [Category Management](#6-category-management)
7. [Budget Tracking](#7-budget-tracking)
8. [Bulk Upload](#8-bulk-upload)
9. [Reports & Analytics](#9-reports--analytics)
10. [Troubleshooting](#10-troubleshooting)
11. [FAQs](#11-faqs)
12. [Best Practices](#12-best-practices)
13. [Support Information](#13-support-information)

---

## 1. Introduction

### 1.1 What is FinanceTracker?

FinanceTracker is a personal finance management web application designed to help you track your income and expenses, manage budgets, and gain insights into your spending patterns. With FinanceTracker, you can:

- ✅ **Track Income & Expenses** - Record all your financial transactions
- ✅ **Manage Categories** - Organize transactions with custom categories
- ✅ **Set Budgets** - Create monthly budgets and track spending
- ✅ **Bulk Import** - Upload multiple transactions via Excel/CSV
- ✅ **View Analytics** - Analyze spending patterns with charts and reports
- ✅ **Export Data** - Download your financial data for external use

### 1.2 Who Should Use This Manual?

This manual is designed for:
- New users setting up their account for the first time
- Existing users wanting to explore advanced features
- Finance administrators managing household or personal budgets
- Anyone looking to better understand their financial habits

### 1.3 Document Conventions

Throughout this manual, you'll see:

📌 **NOTE**: Important information to remember
⚠️ **WARNING**: Actions that require caution
💡 **TIP**: Helpful suggestions and best practices
✅ **DO**: Recommended actions
❌ **DON'T**: Actions to avoid

---

## 2. System Requirements

### 2.1 Supported Browsers

FinanceTracker works best on modern web browsers:

**Recommended:**
- Google Chrome (version 90+)
- Microsoft Edge (version 90+)
- Mozilla Firefox (version 88+)
- Safari (version 14+)

**Minimum Requirements:**
- JavaScript enabled
- Cookies enabled
- Minimum screen resolution: 1024x768

### 2.2 Device Compatibility

✅ **Desktop Computers** - Windows, macOS, Linux
✅ **Laptops** - All operating systems
✅ **Tablets** - iPad, Android tablets (landscape mode recommended)
✅ **Smartphones** - iOS, Android (responsive mobile view)

### 2.3 Internet Connection

- **Minimum**: 1 Mbps download speed
- **Recommended**: 5 Mbps or higher for smooth experience
- Stable connection required for file uploads

### 2.4 Software Requirements

For Excel/CSV upload feature:
- Microsoft Excel 2010 or later, OR
- Google Sheets, OR
- LibreOffice Calc, OR
- Any CSV-compatible spreadsheet software

---

## 3. Getting Started

### 3.1 Creating an Account

**Step 1: Access Registration Page**
1. Open your web browser
2. Navigate to the FinanceTracker URL
3. Click **"Register"** or **"Sign Up"** button

**Step 2: Fill Registration Form**
```
Required Information:
├── Full Name (e.g., "John Smith")
├── Mobile Number (e.g., "+1-555-1234")
├── Email Address (must be valid, used for password reset)
├── Username (unique, 4-20 characters)
└── Password (minimum 8 characters, mix of letters and numbers)
```

**Step 3: Submit Registration**
1. Review all entered information
2. Click **"Create Account"** button
3. Wait for confirmation message
4. You'll be redirected to login page

📌 **NOTE**: Your email must be unique and valid. You'll use it for password recovery.

⚠️ **WARNING**: Remember your username and password. Write them down securely.

### 3.2 Logging In

**Step 1: Access Login Page**
1. Navigate to FinanceTracker homepage
2. You'll see the login screen

**Step 2: Enter Credentials**
1. Username: Enter your registered username
2. Password: Enter your password
3. Click **"Login"** button

**Step 3: Access Dashboard**
- Upon successful login, you'll see your Dashboard
- Your username appears in top-right corner
- Navigation menu shows all available features

💡 **TIP**: Bookmark the login page for quick access!

### 3.3 Password Recovery

**If you forgot your password:**

1. Click **"Forgot Password?"** on login page
2. Enter your registered email address
3. Click **"Send Reset Link"**
4. Check your email inbox (and spam folder)
5. Click the reset link in the email
6. Enter new password (twice for confirmation)
7. Click **"Reset Password"**
8. Login with new password

📌 **NOTE**: Password reset links expire after 30 minutes.

---

## 4. Dashboard Overview

### 4.1 Navigation Menu

The top navigation bar provides quick access to all features:

```
┌─────────────────────────────────────────────────────────┐
│  FinanceTracker    Overview | Add | Transactions |      │
│                    Categories | Budgets | Upload | CSV  │
└─────────────────────────────────────────────────────────┘
```

**Menu Items:**
1. **Overview** - Dashboard with summary and charts
2. **Add Transaction** - Quick transaction entry
3. **Transactions** - View and manage all transactions
4. **Categories** - Manage income/expense categories
5. **Budgets** - Set and track monthly budgets
6. **Bulk Upload** - Import multiple transactions
7. **Export CSV** - Download financial reports
8. **Logout** - Sign out securely

### 4.2 Dashboard Sections

#### **Date Range Filter** (Top Section)
- Select custom date ranges for analysis
- Quick presets: Last 7 Days, Last 30 Days, This Month, Last Month, This Year
- Click **"Apply"** to update all dashboard data
- Click **"Reset"** to return to current month view

#### **Financial Summary** (Cards Section)
```
┌──────────────┬──────────────┬──────────────┐
│   Balance    │   Income     │   Expense    │
│   ₹50,000    │   ₹75,000    │   ₹25,000    │
└──────────────┴──────────────┴──────────────┘
```

- **Current Balance**: Total income minus total expenses
- **Income**: Sum of all CREDIT transactions
- **Expense**: Sum of all DEBIT transactions

#### **Category Breakdown** (Pie Chart)
- Visual representation of spending by category
- Hover over slices to see exact amounts
- Shows top spending categories
- Click legend to filter categories

#### **Daily Spending Trend** (Bar Chart)
- Shows daily expenses for selected period
- Helps identify high-spending days
- Useful for spotting patterns

#### **Budget Overview** (If budgets are set)
```
Category: Food
Budget: ₹15,000 | Spent: ₹12,000 | Remaining: ₹3,000
[████████████░░░░] 80%
```

- Green: Under budget (< 80%)
- Orange: Warning (80-100%)
- Red: Over budget (> 100%)

💡 **TIP**: Check your dashboard daily to stay on top of finances!

---

## 5. Managing Transactions

### 5.1 Adding a New Transaction

**Step-by-Step Guide:**

**Step 1: Access Transaction Form**
- Click **"Add Transaction"** in navigation menu
- Transaction entry form appears

**Step 2: Select Transaction Type**
- Choose **"Credit (Income)"** for money received
- Choose **"Debit (Expense)"** for money spent

**Step 3: Fill Transaction Details**
1. **Type**: Credit or Debit (selected above)
2. **Amount**: Enter amount in ₹ (e.g., 1500.50)
3. **Category**: Select from dropdown
   - Categories change based on transaction type
   - Credit shows income categories
   - Debit shows expense categories

**Step 4: Submit Transaction**
- Click **"Add Transaction"** button
- Confirmation message appears
- Redirected to Dashboard

**Example - Recording Salary:**
```
Type: Credit (Income)
Amount: 50000
Category: Salary
Result: ₹50,000 added to balance ✓
```

**Example - Recording Grocery Purchase:**
```
Type: Debit (Expense)
Amount: 2500
Category: Food
Result: ₹2,500 deducted from balance ✓
```

✅ **DO**:
- Enter the exact amount
- Select the correct category
- Add transactions on the same day

❌ **DON'T**:
- Enter negative amounts
- Skip selecting a category
- Use wrong transaction type

### 5.2 Viewing Transaction History

**Step 1: Access Transactions Page**
- Click **"Transactions"** in navigation menu
- All transactions display in table format

**Step 2: Understanding the Table**
```
┌──────┬────────┬──────────┬───────────┬─────────┐
│ Date │  Type  │ Category │  Amount   │ Actions │
├──────┼────────┼──────────┼───────────┼─────────┤
│ Jan 15│ DEBIT │   Food   │ -₹2,500  │ Edit|Del│
│ Jan 10│ CREDIT│  Salary  │ +₹50,000 │ Edit|Del│
└──────┴────────┴──────────┴───────────┴─────────┘
```

**Color Coding:**
- 🟢 Green: CREDIT (Income)
- 🔴 Red: DEBIT (Expense)

**Step 3: Using Search & Filters**

1. **Search by Amount or Category**
   - Enter amount: "1500"
   - Enter category name: "Food"
   - Click **"Apply Filters"**

2. **Filter by Type**
   - Select "Credit" to see only income
   - Select "Debit" to see only expenses
   - Select "All Types" to see everything

3. **Filter by Category**
   - Dropdown shows all your categories
   - Select specific category to filter

4. **Filter by Date Range**
   - From Date: Select start date
   - To Date: Select end date
   - Click **"Apply Filters"**

**Step 4: Reset Filters**
- Click **"Reset"** button to clear all filters
- Returns to showing all transactions

### 5.3 Editing a Transaction

**When to Edit:**
- You entered wrong amount
- Selected wrong category
- Need to change date
- Made a typo

**Steps to Edit:**

**Step 1: Find Transaction**
- Go to Transactions page
- Use filters to locate the transaction
- Click **"Edit"** button next to transaction

**Step 2: Modify Details**
- Transaction form appears with current values
- Change any field:
  - Date (calendar picker)
  - Type (Credit/Debit)
  - Category (dropdown)
  - Amount (numeric input)

**Step 3: Save Changes**
- Click **"Update Transaction"** button
- Confirmation message appears
- Redirected to Transactions page

⚠️ **WARNING**: Editing a transaction recalculates your balance and budget statistics.

💡 **TIP**: Double-check all values before saving to avoid multiple edits.

### 5.4 Deleting a Transaction

**When to Delete:**
- Duplicate entry
- Test transaction
- Wrong transaction entirely

**Steps to Delete:**

**Step 1: Find Transaction**
- Go to Transactions page
- Locate the transaction to delete

**Step 2: Initiate Delete**
- Click **"Delete"** button
- Confirmation dialog appears:
  ```
  ⚠️ Are you sure you want to delete this transaction?
  [Cancel] [Delete]
  ```

**Step 3: Confirm Deletion**
- Click **"Delete"** to confirm
- OR Click **"Cancel"** to keep transaction
- Success message appears if deleted

⚠️ **WARNING**: Deletion is permanent and cannot be undone!

✅ **DO**: Review the transaction details before confirming delete
❌ **DON'T**: Delete transactions without checking

### 5.5 Pagination

**Navigating Large Transaction Lists:**

- Transactions show 20 per page
- Bottom of page shows pagination controls:
  ```
  [← Previous]  Page 1 of 5  [Next →]
  ```
- Click **"Next"** for newer transactions
- Click **"Previous"** for older transactions
- Page number shows current position

💡 **TIP**: Use filters to narrow down results instead of scrolling through pages.

---

## 6. Category Management

### 6.1 Understanding Categories

**What are Categories?**
Categories help organize your transactions into meaningful groups.

**Two Types:**
1. **System Categories** - Pre-defined, cannot be edited/deleted
   - Examples: Salary, Food, Rent, Transport
   - Available to all users
   - Marked with "SYSTEM" badge

2. **Custom Categories** - User-created, fully customizable
   - Create your own categories
   - Add icons and colors
   - Can edit and delete
   - Private to your account

**Category Types:**
- **CREDIT (Income)**: Salary, Freelance, Investment, Gifts
- **DEBIT (Expense)**: Food, Rent, Transport, Entertainment

### 6.2 Viewing All Categories

**Step 1: Access Categories Page**
- Click **"Categories"** in navigation menu
- Categories page displays

**Step 2: Browse Categories**
```
┌─────────────────────────────────────────┐
│  Income Categories (CREDIT)             │
│  ┌──────┐  ┌──────┐  ┌──────┐          │
│  │ 💰   │  │ 💼   │  │ 📈   │          │
│  │Salary│  │Freelance│Investment│       │
│  │SYSTEM│  │CUSTOM│  │CUSTOM│          │
│  └──────┘  └──────┘  └──────┘          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Expense Categories (DEBIT)             │
│  ┌──────┐  ┌──────┐  ┌──────┐          │
│  │ 🍔   │  │ 🏠   │  │ 🚗   │          │
│  │ Food │  │ Rent │  │Transport│        │
│  │SYSTEM│  │SYSTEM│  │CUSTOM│          │
│  └──────┘  └──────┘  └──────┘          │
└─────────────────────────────────────────┘
```

**Categories Show:**
- Icon (emoji)
- Category Name
- Type (System/Custom)
- Parent category (if subcategory)
- Edit/Delete buttons (custom only)

### 6.3 Creating Custom Categories

**Step 1: Click Add Category**
- Click **"+ Add Custom Category"** button
- Add Category form appears

**Step 2: Fill Category Details**

1. **Category Name** (Required)
   - Enter descriptive name (e.g., "Gym Membership")
   - Keep it short and clear
   - Max 50 characters

2. **Category Type** (Required)
   - Credit (Income): For money coming in
   - Debit (Expense): For money going out

3. **Icon** (Optional)
   - Enter emoji: 💰 🏠 🍔 🚗 ✈️ 🎬 📱 💊
   - Click emoji or copy-paste
   - Leave blank for default icon

4. **Color** (Optional)
   - Click color picker
   - Choose category color
   - Used for visual identification
   - Default: Blue for Credit, Red for Debit

5. **Parent Category** (Optional)
   - Select to make this a subcategory
   - Example: "Restaurants" under "Food"
   - Leave "None" for top-level category

**Step 3: Preview & Create**
- Preview box shows how category will look
- Updates as you type
- Click **"Create Category"** button
- Success message appears

**Example - Creating "Online Shopping" Category:**
```
Category Name: Online Shopping
Type: Debit (Expense)
Icon: 🛒
Color: #9b59b6 (Purple)
Parent Category: None
```

💡 **TIP**: Use consistent colors for related categories (all food categories in orange, all transport in blue, etc.)

### 6.4 Creating Subcategories

**What are Subcategories?**
Subcategories help break down broad categories into specific types.

**Example Structure:**
```
Food (Parent)
├── Groceries (Subcategory)
├── Restaurants (Subcategory)
└── Takeout (Subcategory)

Transport (Parent)
├── Fuel (Subcategory)
├── Public Transport (Subcategory)
└── Taxi/Uber (Subcategory)
```

**Creating a Subcategory:**

**Step 1: Plan Your Structure**
- Decide parent category (e.g., "Food")
- Decide subcategory name (e.g., "Restaurants")

**Step 2: Fill Form**
```
Category Name: Restaurants
Type: Debit (Expense)
Icon: 🍽️
Color: #e67e22 (Orange - same as Food)
Parent Category: Food  ← Select parent
```

**Step 3: Create**
- Click **"Create Category"**
- Subcategory appears under parent
- Marked with "Subcategory of: Food"

✅ **DO**:
- Use subcategories for detailed tracking
- Keep consistent naming
- Use similar colors for related categories

❌ **DON'T**:
- Create too many subcategories
- Make subcategories of subcategories
- Use conflicting colors

### 6.5 Editing Categories

**What Can Be Edited:**
- Category name
- Icon
- Color
- Parent relationship
- Type (Credit/Debit)

⚠️ **WARNING**: Can only edit YOUR custom categories, not system categories.

**Steps to Edit:**

**Step 1: Find Category**
- Go to Categories page
- Locate your custom category

**Step 2: Click Edit**
- Click **"Edit"** button on category card
- Edit form appears with current values

**Step 3: Modify Details**
- Change any field
- Preview updates in real-time

**Step 4: Save Changes**
- Click **"Update Category"**
- Changes saved
- Redirected to Categories page

📌 **NOTE**: Editing a category affects all transactions using that category.

### 6.6 Deleting Categories

**When to Delete:**
- No longer needed
- Created by mistake
- Duplicate category

**Steps to Delete:**

**Step 1: Check Usage**
- Before deleting, check if category has transactions
- Cannot delete if transactions exist

**Step 2: Click Delete**
- Click **"Delete"** button
- Confirmation dialog appears

**Step 3: Confirm**
- If no transactions: Deletion succeeds
- If has transactions: Error message shows
  ```
  ❌ Cannot delete 'Food' because it has associated transactions.
  ```

**What to Do if Category Has Transactions:**
1. Don't delete - keep for historical data
2. OR Move transactions to different category first
3. OR Stop using, let it remain for old records

⚠️ **WARNING**: Category deletion is permanent!

---

## 7. Budget Tracking

### 7.1 Understanding Budgets

**What is a Budget?**
A budget is a spending limit you set for a specific category for a month.

**Example:**
```
Food Budget: ₹15,000/month
Spent: ₹12,000
Remaining: ₹3,000
Status: ✅ On Track (80%)
```

**Benefits:**
- Control spending
- Avoid overspending
- Plan monthly expenses
- Get alerts when nearing limit

### 7.2 Setting a Monthly Budget

**Step 1: Access Budgets Page**
- Click **"Budgets"** in navigation menu
- Budgets page displays

**Step 2: Click Add Budget**
- Click **"+ Set New Budget"** button
- Budget form appears

**Step 3: Select Category**
- Dropdown shows expense categories only
- Select category to budget (e.g., "Food")
- Cannot set budgets for income categories

**Step 4: Set Monthly Limit**
- Enter amount in ₹
- This is your spending cap for the month
- Example: 15000 for ₹15,000

**Step 5: Create Budget**
- Click **"Set Budget"** button
- Budget is active for current month
- Appears in dashboard and budget page

**Example - Setting Food Budget:**
```
Category: Food
Monthly Limit: ₹15,000
Month: February 2026 (automatic)
Result: Budget created ✓
```

💡 **TIP**: Start with realistic budgets based on past spending, then adjust monthly.

### 7.3 Viewing Budget Status

**Dashboard View:**
```
Budget vs Actual (Current Month)
┌──────────────────────────────────────────┐
│ Food                                      │
│ ┌────────────────────────────────────┐   │
│ │ Total Budget: ₹15,000              │   │
│ │ Spent: ₹12,000                     │   │
│ │ Remaining: ₹3,000                  │   │
│ │ [████████████░░░░] 80%             │   │
│ └────────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

**Status Indicators:**
- **Green (0-79%)**: ✅ On Track - You're doing well!
- **Orange (80-99%)**: ⚠️ Warning - Getting close to limit
- **Red (100%+)**: ❌ Over Budget - Exceeded limit

**Budgets Page View:**
```
┌──────────┬────────────┬─────────┬───────────┬────────┐
│ Category │   Budget   │  Spent  │ Remaining │ Status │
├──────────┼────────────┼─────────┼───────────┼────────┤
│   Food   │  ₹15,000   │₹12,000  │  ₹3,000   │  80%   │
│   Rent   │  ₹20,000   │₹20,000  │     ₹0    │ 100%   │
│ Transport│  ₹5,000    │₹6,000   │  -₹1,000  │ 120%   │
└──────────┴────────────┴─────────┴───────────┴────────┘
```

### 7.4 Understanding Budget Calculations

**How Budgets Work:**

1. **Budget Set**: ₹15,000 for Food in February 2026

2. **Spending Tracked**: All Food transactions in February

3. **Calculation**:
   ```
   Total Spent = Sum of all DEBIT transactions in Food category
   Remaining = Budget Limit - Total Spent
   Percentage = (Total Spent / Budget Limit) × 100
   ```

4. **Example**:
   ```
   Feb 1: Groceries -₹3,000
   Feb 5: Restaurant -₹2,000
   Feb 10: Groceries -₹4,000
   Feb 15: Takeout -₹1,500
   Feb 20: Groceries -₹1,500

   Total Spent: ₹12,000
   Remaining: ₹15,000 - ₹12,000 = ₹3,000
   Percentage: (12,000 / 15,000) × 100 = 80%
   Status: ⚠️ Warning
   ```

### 7.5 Monthly Budget Rollover

**What Happens at Month End:**

- Budgets are monthly, not cumulative
- Each month starts fresh
- Previous month's budget doesn't carry over
- You must set budgets for each new month

**Example:**
```
January 2026:
- Food Budget: ₹15,000
- Spent: ₹12,000
- Remaining: ₹3,000

February 2026:
- Food Budget: ₹15,000 (set again)
- Spent: ₹0 (starts at zero)
- Remaining: ₹15,000
```

**Setting Budgets for New Month:**

**Step 1**: On 1st of new month
**Step 2**: Go to Budgets page
**Step 3**: Click "Set New Budget"
**Step 4**: Enter same or adjusted amounts
**Step 5**: Create budgets

💡 **TIP**: Copy last month's successful budgets, adjust those that were too high/low.

### 7.6 Editing Budgets

**When to Edit:**
- Income changed
- Life circumstances changed
- Budget was unrealistic
- Mid-month adjustment needed

**Steps:**

**Step 1: Go to Budgets Page**
- Click "Budgets" in navigation

**Step 2: Find Budget to Edit**
- Locate the budget in the table

**Step 3: Click Edit**
- Click **"Edit"** button
- Edit form appears

**Step 4: Modify Limit**
- Change monthly limit amount
- Keep same category
- Click **"Update Budget"**

**Step 5: Changes Apply**
- Budget recalculates immediately
- Percentage updates
- Status color may change

📌 **NOTE**: Editing budget doesn't change past spending, only the limit.

### 7.7 Deleting Budgets

**When to Delete:**
- Category no longer relevant
- Don't want to track that category
- Created by mistake

**Steps:**

**Step 1: Find Budget**
- Go to Budgets page
- Locate budget to delete

**Step 2: Click Delete**
- Click **"Delete"** button
- Confirmation dialog appears

**Step 3: Confirm**
- Click **"Delete"** to remove
- Budget removed from tracking

⚠️ **WARNING**: Deleting a budget removes it only for that month. Transactions remain unchanged.

---

## 8. Bulk Upload

### 8.1 What is Bulk Upload?

Bulk Upload allows you to import multiple transactions at once using Excel or CSV files, perfect for:

- Entering last month's data quickly
- Importing data from other apps
- Recovering from backups
- Initial setup with historical data

**Key Features:**
- Upload 100s of transactions in seconds
- Automatic validation
- Duplicate detection
- Detailed error reporting
- Supports Excel (.xlsx, .xls) and CSV (.csv)

### 8.2 Understanding Date Restrictions

⚠️ **IMPORTANT**: Bulk upload only accepts **previous month's data**.

**Example (Today is February 15, 2026):**
```
✅ Allowed: January 1 to January 31, 2026
❌ Not Allowed: February 2026 (current month)
❌ Not Allowed: December 2025 (two months ago)
```

**Why This Restriction?**
- Prevents data entry errors
- Ensures data consistency
- Current month should be entered manually
- Historical data beyond one month should be entered month-by-month

### 8.3 Step-by-Step Upload Process

#### **STEP 1: Download Template**

**Action**: Click **"Bulk Upload"** in navigation menu

**Result**: Bulk Upload page displays showing:
```
┌──────────────────────────────────────────┐
│ Importing for: January 2026              │
│ Valid date range: 2026-01-01 to 2026-01-31 │
└──────────────────────────────────────────┘
```

**Choose Template Format:**

**Option A: Excel Template (Recommended)**
- Click **"📊 Download Excel Template"**
- File downloads: `transaction_template_2026_01.xlsx`
- **Advantages**:
  - Pre-formatted headers
  - Includes instructions sheet
  - Shows available categories
  - Example transactions included
  - Easy to use

**Option B: CSV Template**
- Click **"📄 Download CSV Template"**
- File downloads: `transaction_template_2026_01.csv`
- **Advantages**:
  - Works in any spreadsheet software
  - Smaller file size
  - Universal compatibility

💡 **TIP**: Use Excel template for first-time users. It has better guidance.

#### **STEP 2: Open and Review Template**

**For Excel Template:**

**Sheet 1: Transactions**
```
┌──────────────────┬─────────────────────┬─────────┬───────────────┐
│ Transaction Date │ Transaction Type    │ Amount  │ Category Name │
│ (YYYY-MM-DD)     │ (CREDIT/DEBIT)      │         │               │
├──────────────────┼─────────────────────┼─────────┼───────────────┤
│ 2026-01-15       │ DEBIT               │ 1000.00 │ Food          │
│                  │                     │         │               │
└──────────────────┴─────────────────────┴─────────┴───────────────┘
```

**Sheet 2: Instructions**
- How to use template
- Data format requirements
- Available categories list
- Examples

**For CSV Template:**
```
# Transaction Upload Template for January 2026
# Date Range: 2026-01-01 to 2026-01-31
# Format: Transaction Date (YYYY-MM-DD), Transaction Type, Amount, Category
# Example: 2026-01-15, DEBIT, 1000.00, Food
Transaction Date (YYYY-MM-DD),Transaction Type (CREDIT/DEBIT),Amount,Category Name
2026-01-15,DEBIT,1000.00,Food
```

#### **STEP 3: Fill in Your Data**

**Column 1: Transaction Date**
```
Format: YYYY-MM-DD
Examples:
✅ 2026-01-15
✅ 2026-01-01
✅ 2026-01-31
❌ 15/01/2026 (wrong format)
❌ 2026-02-01 (outside date range)
❌ Jan 15 (incomplete)
```

**Column 2: Transaction Type**
```
Values: CREDIT or DEBIT
Examples:
✅ CREDIT
✅ DEBIT
✅ credit (case-insensitive)
❌ Income (wrong term)
❌ CR (abbreviation not allowed)
```

**Column 3: Amount**
```
Format: Positive number with up to 2 decimals
Examples:
✅ 1000
✅ 1500.50
✅ 2500.00
❌ -1000 (negative not allowed)
❌ 1,500 (no commas)
❌ 1500.505 (too many decimals)
```

**Column 4: Category Name**
```
Value: Must match existing category exactly
Examples:
✅ Food (if "Food" exists)
✅ Salary (if "Salary" exists)
❌ Groceries (if not in your categories)
❌ food (case-sensitive)
❌ Salary! (extra characters)
```

**Example - Filled Template:**
```
Transaction Date,Transaction Type,Amount,Category Name
2026-01-05,CREDIT,50000,Salary
2026-01-10,DEBIT,20000,Rent
2026-01-12,DEBIT,5000,Food
2026-01-15,DEBIT,2000,Transport
2026-01-18,DEBIT,3000,Entertainment
2026-01-20,DEBIT,1500,Food
2026-01-25,CREDIT,5000,Freelance
2026-01-28,DEBIT,2500,Shopping
```

✅ **DO**:
- Use correct date format
- Match category names exactly
- Check for typos
- Keep amounts positive
- Save file after editing

❌ **DON'T**:
- Add extra columns
- Delete header row
- Use formulas
- Merge cells
- Add colors/formatting (CSV)

💡 **TIP**: Fill a few rows, upload as test, then continue with rest if successful.

#### **STEP 4: Save Your File**

**For Excel:**
- Click **File → Save As**
- Keep .xlsx format
- Choose easy-to-find location
- Example name: "January_2026_Transactions.xlsx"

**For CSV:**
- Click **File → Save As**
- Choose **CSV (Comma delimited)** format
- Save to Downloads or Desktop
- Example name: "January_2026_Transactions.csv"

📌 **NOTE**: Close the file before uploading to avoid file-in-use errors.

#### **STEP 5: Upload File**

**Method 1: Drag and Drop**
1. Locate saved file in file explorer
2. Drag file to upload area on webpage
3. Drop when area highlights
4. File name appears below

**Method 2: Click to Browse**
1. Click **"Choose File"** button
2. File browser opens
3. Navigate to your file
4. Select file and click **"Open"**
5. File name appears

**Verify Selection:**
```
✓ Selected: January_2026_Transactions.xlsx
```

**Upload:**
- Click **"Upload & Import Transactions"** button
- Processing begins
- Wait for results (usually 5-30 seconds)

📌 **NOTE**: Don't refresh page during upload!

#### **STEP 6: Review Results**

**Success Scenario:**
```
┌──────────────────────────────────────────┐
│          ✓ Upload Successful!            │
│ Your transactions have been imported     │
└──────────────────────────────────────────┘

Statistics:
┌────────────┬─────────────────┬───────────────┐
│ Total Rows │ Successfully    │   Duplicates  │
│            │    Imported     │    Skipped    │
├────────────┼─────────────────┼───────────────┤
│     8      │        8        │       0       │
└────────────┴─────────────────┴───────────────┘

Actions:
[View Dashboard] [View Transactions] [Upload More]
```

**What to Do Next:**
1. Click **"View Dashboard"** to see updated balance
2. Or Click **"View Transactions"** to verify entries
3. Or Click **"Upload More"** if you have another file

**Error Scenario:**
```
┌──────────────────────────────────────────┐
│          ⚠ Upload Failed                 │
│ Some records have validation errors      │
└──────────────────────────────────────────┘

Statistics:
┌────────────┬──────────┬─────────────────┐
│ Total Rows │  Valid   │ Records with    │
│            │ Records  │     Errors      │
├────────────┼──────────┼─────────────────┤
│     8      │    5     │        3        │
└────────────┴──────────┴─────────────────┘

Error Details:
┌─────┬────────────┬────────┬────────┬──────────┬─────────────────────────┐
│ Row │    Date    │  Type  │ Amount │ Category │         Errors          │
├─────┼────────────┼────────┼────────┼──────────┼─────────────────────────┤
│  3  │ 2026-02-01 │ DEBIT  │  5000  │   Food   │ Date must be between... │
│  5  │ 2026-01-15 │ EXPENSE│  2000  │ Transport│ Type must be CREDIT...  │
│  7  │ 2026-01-20 │ DEBIT  │ -1500  │   Food   │ Amount must be > 0      │
└─────┴────────────┴────────┴────────┴──────────┴─────────────────────────┘

Actions:
[Fix Errors & Try Again] [Download New Template]
```

### 8.4 Handling Upload Errors

**Common Errors and Solutions:**

**Error 1: Invalid Date Format**
```
Error: "Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-15)"
Solution: Change "15/01/2026" to "2026-01-15"
```

**Error 2: Date Outside Range**
```
Error: "Date must be between 2026-01-01 and 2026-01-31"
Solution: Check month/year, update to valid date
```

**Error 3: Invalid Transaction Type**
```
Error: "Transaction Type must be CREDIT or DEBIT"
Solution: Change "Income" to "CREDIT" or "Expense" to "DEBIT"
```

**Error 4: Invalid Amount**
```
Error: "Amount must be a valid number"
Solution: Remove commas, currency symbols: "1,500₹" → "1500"
```

**Error 5: Amount Must Be Positive**
```
Error: "Amount must be greater than 0"
Solution: Change "-1500" to "1500"
```

**Error 6: Category Not Found**
```
Error: "Category 'Groceries' not found. Please use an existing category."
Solution: Change to exact category name from your list (e.g., "Food")
```

**Error 7: Duplicate Transaction**
```
Error: "Duplicate transaction already exists in database"
Solution: This transaction is already entered. Remove from file or keep if needed.
```

**How to Fix Errors:**

**Step 1: Note Error Rows**
- Error table shows row numbers
- Note which rows have issues

**Step 2: Open Original File**
- Open the file you just uploaded
- Don't download template again

**Step 3: Fix Each Row**
- Go to row number from error table
- Make corrections based on error message
- Double-check fix

**Step 4: Save and Re-Upload**
- Save file
- Go to Bulk Upload page
- Upload corrected file

💡 **TIP**: Fix one type of error at a time, re-upload, see remaining errors.

### 8.5 Duplicate Detection

**How Duplicates Are Detected:**

System checks if transaction already exists with:
- Same user (you)
- Same date
- Same amount
- Same category

**Example:**
```
Existing in Database:
Date: 2026-01-15
Type: DEBIT
Amount: 2500
Category: Food

Uploading:
Date: 2026-01-15
Type: DEBIT
Amount: 2500
Category: Food

Result: ⚠️ Marked as duplicate, skipped
```

**What Happens to Duplicates:**
- Not imported (skipped)
- Counted in statistics
- Original transaction remains
- Not considered an error

**Duplicate Count Example:**
```
Total Rows: 10
Successfully Imported: 7
Duplicates Skipped: 3

→ 7 new transactions added
→ 3 were already in database
```

💡 **TIP**: Duplicates are normal if you're re-uploading corrected data.

### 8.6 File Requirements & Limits

**Supported Formats:**
- ✅ Excel 2007+ (.xlsx)
- ✅ Excel 97-2003 (.xls)
- ✅ CSV - Comma Separated Values (.csv)
- ❌ PDF, Word, Text files not supported

**File Size Limit:**
- Maximum: 10 MB
- Approximately 50,000 rows
- Most users need << 1000 rows

**Data Limits:**
- No maximum rows (within file size)
- Each row = one transaction
- Empty rows are skipped

**Template Structure:**
- Must have header row
- Must have 4 columns
- Column order must match template
- Don't add extra columns

✅ **DO**:
- Keep files under 10 MB
- Use provided template
- Keep original structure

❌ **DON'T**:
- Add extra sheets (Excel)
- Change column order
- Add extra columns
- Delete header row

---

## 9. Reports & Analytics

### 9.1 Exporting Financial Data

**What is CSV Export?**
CSV Export downloads your complete financial data in a CSV file for:
- Backup purposes
- Analysis in Excel/Google Sheets
- Tax preparation
- Sharing with accountant
- Importing to other software

**Step-by-Step Export:**

**Step 1: Click Export**
- Click **"Export CSV"** in navigation menu
- Download begins immediately
- File name: `[username]_financial_report_YYYYMMDD.csv`

**Step 2: Locate Downloaded File**
- Check Downloads folder
- File size depends on transaction count
- Usually < 1 MB

**Step 3: Open in Spreadsheet Software**
- Double-click file
- Opens in Excel, Google Sheets, or default app
- View and analyze data

**What's Included in Export:**

**Section 1: Financial Summary**
```
FINANCIAL SUMMARY REPORT
Generated: 2026-02-15
User: john_smith

OVERALL FINANCIAL HEALTH
Current Balance: 50000
Current Month Income: 75000
Current Month Expense: 25000
Last Month Expense: 28000
Month-over-Month Change: 10.7% DECREASE
```

**Section 2: Budget Analysis**
```
BUDGET vs ACTUAL COMPARISON
Category,Budget Limit,Actual Spent,Remaining,Usage %,Status
Food,15000,12000,3000,80.0%,ON TRACK
Rent,20000,20000,0,100.0%,WARNING
Transport,5000,6000,-1000,120.0%,OVER BUDGET
```

**Section 3: Category Breakdown**
```
SPENDING BY CATEGORY (Current Month)
Category,Amount,% of Total Spending
Food,12000,48.0%
Rent,20000,40.0%
Transport,6000,12.0%
```

**Section 4: Financial Analysis & Insights**
```
FINANCIAL ANALYSIS & INSIGHTS
Spending Trend: Your spending decreased by 3000 compared to last month
Budget Health: 1 category is over budget
Savings Rate: 66.7% (50000 saved this month)
Top Spending Category: Rent (20000)
```

**Section 5: Detailed Transactions**
```
DETAILED TRANSACTION HISTORY
Date,Type,Category,Amount
2026-02-01,CREDIT,Salary,75000
2026-02-05,DEBIT,Food,5000
2026-02-10,DEBIT,Rent,20000
...
```

### 9.2 Understanding Dashboard Analytics

**Balance Trend**
- Shows how your balance changes over time
- Green line = increasing balance ✅
- Red line = decreasing balance ⚠️
- Flat line = stable balance

**Category Breakdown (Pie Chart)**
- Each slice = one expense category
- Size = portion of total spending
- Hover for exact amount and percentage
- Click legend to show/hide categories

**Daily Spending (Bar Chart)**
- Each bar = one day
- Height = total spending that day
- Helps identify spending patterns
- Useful for finding high-expense days

**Top Spending Categories**
- Sorted by highest to lowest
- Shows category name and amount
- Percentage of total expenses
- Quick view of where money goes

### 9.3 Date Range Analysis

**Using Date Filters:**

**Step 1: Select Date Range**
- Click **FROM DATE** calendar
- Pick start date
- Click **TO DATE** calendar
- Pick end date

**Step 2: Apply Filter**
- Click **"Apply"** button
- All dashboard data updates:
  - Balance calculation
  - Category breakdown
  - Spending trends
  - Budget status (if in range)

**Step 3: Reset to Default**
- Click **"Reset"** button
- Returns to current month view

**Quick Preset Filters:**
```
[Last 7 Days]  [Last 30 Days]  [This Month]  [Last Month]  [This Year]
```
- Click any preset for instant filtering
- Faster than manual date selection

**Use Cases:**

**Weekly Review:**
```
Preset: Last 7 Days
Purpose: Quick weekly spending check
```

**Monthly Analysis:**
```
Preset: Last Month
Purpose: Analyze completed month
```

**Quarterly Review:**
```
Custom: Jan 1 to Mar 31
Purpose: 3-month spending patterns
```

**Year-to-Date:**
```
Preset: This Year
Purpose: Annual financial overview
```

💡 **TIP**: Use "Last Month" preset on 1st of month to review previous month's performance.

---

## 10. Troubleshooting

### 10.1 Login Issues

**Problem: "Invalid username or password"**

**Possible Causes & Solutions:**

1. **Wrong Username**
   - Solution: Check capitalization (usernames are case-sensitive)
   - Example: "JohnSmith" ≠ "johnsmith"

2. **Wrong Password**
   - Solution: Re-type carefully
   - Check Caps Lock is OFF
   - Use password reset if forgotten

3. **Account Doesn't Exist**
   - Solution: Click "Register" to create account
   - Check if you registered with different email

**Problem: "Password reset email not received"**

**Solutions:**
1. Check spam/junk folder
2. Wait 5-10 minutes
3. Check email address spelling
4. Try different email if multiple accounts
5. Request new reset link

**Problem: "Reset link expired"**

**Solution:**
- Reset links valid for 30 minutes only
- Request new reset link from forgot password page
- Complete reset process within 30 minutes

### 10.2 Transaction Issues

**Problem: Transaction not showing in list**

**Possible Causes:**
1. **Filters Applied**
   - Solution: Click "Reset" to clear filters
   - Check if transaction matches current filters

2. **Wrong Date**
   - Solution: Expand date range filter
   - Check transaction was saved successfully

3. **Page Not Refreshed**
   - Solution: Refresh browser (F5 or Ctrl+R)

**Problem: "Cannot delete transaction"**

**Cause:** Browser confirmation not clicked
**Solution:** Click "Delete" button, then confirm in popup dialog

**Problem: Balance doesn't match expectations**

**Troubleshooting Steps:**
1. Check all transactions are entered
2. Verify transaction types (CREDIT vs DEBIT)
3. Check for duplicate entries
4. Review date filters (might be hiding transactions)
5. Export CSV to verify in Excel

### 10.3 Budget Issues

**Problem: Budget showing over 100% but spending seems normal**

**Possible Causes:**
1. **Wrong Month Selected**
   - Solution: Check budget is for correct month
   - Create budget for current month if missing

2. **Budget Too Low**
   - Solution: Edit budget to realistic amount
   - Review last month's spending for guidance

3. **Transactions in Wrong Category**
   - Solution: Review transactions
   - Edit and recategorize if needed

**Problem: Budget not updating after transaction**

**Solutions:**
1. Refresh page (F5)
2. Check transaction date matches budget month
3. Verify category matches budget category
4. Wait 30 seconds and refresh again

### 10.4 Category Issues

**Problem: Cannot delete category**

**Error:** "Cannot delete because it has associated transactions"

**Solutions:**
1. **Keep Category**
   - Don't delete - needed for historical data
   - Stop using for new transactions

2. **Move Transactions**
   - Edit all transactions using this category
   - Change to different category
   - Then delete category

**Problem: Category not showing in dropdown**

**Possible Causes:**
1. **Wrong Transaction Type**
   - Credit categories only show for Income
   - Debit categories only show for Expenses
   - Solution: Select correct type first

2. **Category Was Deleted**
   - Solution: Create category again

### 10.5 Bulk Upload Issues

**Problem: "Invalid file format" error**

**Solutions:**
1. Check file extension (.xlsx, .xls, or .csv only)
2. Re-download template
3. Don't change file format when saving
4. If using Google Sheets: File → Download → Excel/CSV

**Problem: "File too large" error**

**Solutions:**
1. Check file size (max 10 MB)
2. Split data into multiple files
3. Upload month-by-month instead of all at once
4. Remove unnecessary columns/data

**Problem: All rows show date errors**

**Common Issue:** Date format wrong
**Solution:**
```
Wrong: 15/01/2026, Jan 15, 2026, 15-Jan
Right: 2026-01-15

Excel: Format cells as "Text" before entering dates
CSV: Use YYYY-MM-DD format exactly
```

**Problem: Categories not found**

**Solution:**
1. Go to Categories page
2. Note exact category names (case-sensitive)
3. Update Excel/CSV to match exactly
4. Example: If category is "Food", use "Food" not "food" or "FOOD"

### 10.6 Browser Issues

**Problem: Page not loading properly**

**Solutions:**
1. **Clear Browser Cache**
   - Chrome: Ctrl+Shift+Delete → Clear cache
   - Firefox: Ctrl+Shift+Delete → Cookies and Cache
   - Safari: Preferences → Privacy → Manage Website Data

2. **Update Browser**
   - Check for browser updates
   - Install latest version
   - Restart browser

3. **Try Different Browser**
   - Chrome (recommended)
   - Firefox
   - Edge

**Problem: Dropdown menus not working**

**Solutions:**
1. Enable JavaScript (required)
2. Disable browser extensions temporarily
3. Try incognito/private mode
4. Clear cache and cookies

**Problem: Charts not displaying**

**Solutions:**
1. Refresh page
2. Check internet connection
3. Enable JavaScript
4. Try different browser

### 10.7 Data Issues

**Problem: Data seems incorrect or missing**

**Steps to Investigate:**
1. **Export CSV Report**
   - Download complete data
   - Review in Excel
   - Look for anomalies

2. **Check Filters**
   - Reset all filters
   - Expand date ranges
   - Clear search terms

3. **Verify Transactions**
   - Go to Transactions page
   - Sort by date
   - Review entries

**Problem: Duplicate transactions appearing**

**Causes:**
1. Uploaded same file twice
2. Manually entered then uploaded
3. Browser double-submit

**Solution:**
- Delete duplicates individually
- Check date + amount + category to identify duplicates
- Use search to find and remove

---

## 11. FAQs

### General Questions

**Q1: Is my financial data secure?**
**A:** Yes. All sensitive personal information (name, email, phone, username) is encrypted in the database using AES encryption. Passwords are hashed with bcrypt. Only you can access your data when logged in.

**Q2: Can I access FinanceTracker from multiple devices?**
**A:** Yes! FinanceTracker is web-based. Log in from any device (computer, tablet, phone) using your username and password.

**Q3: Is there a mobile app?**
**A:** Not currently. However, the website is mobile-responsive and works well on smartphones and tablets through your mobile browser.

**Q4: How much historical data can I store?**
**A:** There's no limit on transaction history. You can store years of financial data.

**Q5: Can multiple people use one account?**
**A:** No. Each account is for one person. However, you can create separate accounts for each family member.

### Account Questions

**Q6: Can I change my username?**
**A:** No, usernames are permanent. Choose carefully during registration.

**Q7: Can I change my email address?**
**A:** Currently not supported. Contact support if you need to change email.

**Q8: What happens if I forget my username?**
**A:** Contact support with your registered email address for assistance.

**Q9: How secure is my password?**
**A:** Passwords are hashed using bcrypt (industry-standard). We never store passwords in plain text.

**Q10: Can I delete my account?**
**A:** Contact support to request account deletion. All data will be permanently removed.

### Transaction Questions

**Q11: Can I edit transaction dates?**
**A:** Yes, when editing a transaction, you can change the date using the calendar picker.

**Q12: What's the difference between CREDIT and DEBIT?**
**A:**
- CREDIT = Money coming in (Income, Salary, Gifts)
- DEBIT = Money going out (Expenses, Bills, Purchases)

**Q13: Can I add transactions for future dates?**
**A:** No. Only current or past dates are allowed to maintain data accuracy.

**Q14: Is there a limit on transaction amount?**
**A:** Maximum amount is 99,999,999.99 (sufficient for most personal use).

**Q15: Can I attach receipts to transactions?**
**A:** Not currently supported. Planned for future updates.

### Category Questions

**Q16: How many categories can I create?**
**A:** No limit. Create as many as needed for detailed tracking.

**Q17: Can I rename system categories?**
**A:** No. System categories are fixed. Create custom categories with your preferred names.

**Q18: What happens to transactions if I delete a category?**
**A:** You cannot delete categories that have transactions. This protects your historical data.

**Q19: Can I merge two categories?**
**A:** Not directly. Edit all transactions from one category to another, then delete the empty category.

**Q20: Can I export my categories list?**
**A:** Category names appear in the CSV export file and Excel template downloads.

### Budget Questions

**Q21: Do budgets carry over to next month?**
**A:** No. Budgets are monthly and must be set each month.

**Q22: Can I set weekly budgets?**
**A:** No, only monthly budgets are supported.

**Q23: Can I set budgets for income categories?**
**A:** No, budgets are only for expense categories (DEBIT).

**Q24: What happens when I exceed a budget?**
**A:** The budget shows red/over budget status. This is a warning only; you can still add transactions.

**Q25: Can I get budget alerts?**
**A:** Dashboard shows visual warnings (orange at 80%, red at 100%). Email alerts planned for future.

### Bulk Upload Questions

**Q26: Can I upload current month's data?**
**A:** No, only previous month. Use manual entry for current month.

**Q27: Can I upload multiple months at once?**
**A:** No. Upload one month at a time, month-by-month.

**Q28: What happens if I upload the same file twice?**
**A:** Duplicate transactions are automatically detected and skipped. Only new transactions are imported.

**Q29: Can I upload data from other finance apps?**
**A:** If you can export to CSV from the other app, yes. Format the data to match our template.

**Q30: Maximum file size for upload?**
**A:** 10 MB maximum (typically holds 50,000+ transactions).

### Export Questions

**Q31: What data is included in CSV export?**
**A:** Complete financial summary, budget analysis, category breakdown, insights, and all transactions.

**Q32: Can I export data for specific date range?**
**A:** CSV export includes all your data. Use date filters in Excel/Sheets after export.

**Q33: Can I schedule automatic exports?**
**A:** Not currently. Manual export only.

**Q34: Can I export as PDF?**
**A:** Currently CSV only. Open CSV in Excel and save as PDF if needed.

**Q35: How do I import exported data back?**
**A:** Use the transaction section from exported CSV to create a bulk upload file.

---

## 12. Best Practices

### 12.1 Daily Habits

✅ **Record Transactions Daily**
- Enter expenses on the same day
- Don't let transactions pile up
- Takes 2 minutes daily vs. 30 minutes weekly

✅ **Check Dashboard Each Morning**
- Review yesterday's spending
- Check budget status
- Spot any unusual transactions

✅ **Use Consistent Categories**
- Don't switch between "Food" and "Groceries"
- Stick to one category per expense type
- Ensures accurate analytics

### 12.2 Weekly Routines

✅ **Weekly Review (Every Sunday)**
1. Review last 7 days spending
2. Compare to previous week
3. Identify overspending areas
4. Plan next week's budget

✅ **Verify All Transactions**
- Check no transactions missed
- Review bank statements
- Add any missing entries

### 12.3 Monthly Workflow

✅ **Month-End Process (Last day of month):**
1. **Verify All Transactions**
   - Cross-check with bank statements
   - Add missing transactions
   - Correct any errors

2. **Review Budget Performance**
   - Note which budgets succeeded
   - Identify budget failures
   - Analyze reasons for overruns

3. **Analyze Spending Patterns**
   - Export monthly CSV
   - Review category breakdown
   - Compare to previous month

4. **Set Next Month's Budgets**
   - Adjust based on this month's performance
   - Account for planned expenses
   - Set realistic targets

5. **Backup Data**
   - Export CSV for backup
   - Save to cloud storage
   - Keep for records

### 12.4 Category Organization

✅ **Create Meaningful Categories**
```
Bad Practice:
- "Misc"
- "Other"
- "Random"

Good Practice:
- "Dining Out"
- "Home Maintenance"
- "Health & Wellness"
```

✅ **Use Subcategories for Detail**
```
Shopping (Parent)
├── Clothing
├── Electronics
└── Home Goods

Food (Parent)
├── Groceries
├── Restaurants
└── Takeout
```

✅ **Limit Number of Categories**
- Too few (5-6): Not detailed enough
- Too many (50+): Overwhelming
- Ideal: 15-25 categories
- Use subcategories for detail

### 12.5 Budget Setting Tips

✅ **Use Historical Data**
1. Review last 3 months' spending
2. Calculate average per category
3. Set budget slightly below average
4. Adjust after first month

✅ **50/30/20 Rule**
```
50% - Needs (Rent, Food, Transport)
30% - Wants (Entertainment, Shopping)
20% - Savings/Debt
```

✅ **Build Emergency Buffer**
- Add 10-15% buffer to budgets
- Accounts for unexpected expenses
- Prevents constant over-budget status

### 12.6 Data Entry Best Practices

✅ **Be Consistent**
- Use same category for same expense
- Don't vary category names
- Maintain category discipline

✅ **Be Specific**
- Instead of "Expense", use actual category
- Add meaningful transaction details
- Future-you will thank you

✅ **Double-Check Before Saving**
- Verify amount (1500 vs. 15000)
- Check transaction type (CREDIT vs. DEBIT)
- Confirm category selection

❌ **Avoid Common Mistakes**
- Don't use negative amounts
- Don't mix up CREDIT/DEBIT
- Don't skip transactions to save time
- Don't use "Other" category excessively

### 12.7 Security Best Practices

✅ **Password Security**
- Use strong password (8+ characters)
- Mix letters, numbers, symbols
- Don't share password
- Change password periodically

✅ **Session Security**
- Logout when done
- Especially on shared computers
- Don't save password on public devices

✅ **Data Privacy**
- Don't share login credentials
- Export data securely
- Delete old export files

### 12.8 Backup Strategy

✅ **Monthly Backups**
1. Export CSV on last day of month
2. Save to cloud storage (Google Drive, Dropbox)
3. Name with date: "Finance_Backup_2026_02.csv"
4. Keep at least 12 months of backups

✅ **Quarterly Deep Backups**
- Export full data
- Save multiple copies
- Test recovery (open in Excel)
- Archive old backups

---

## 13. Support Information

### 13.1 Getting Help

**Before Contacting Support:**

1. **Check This Manual**
   - Use Ctrl+F to search for keywords
   - Review relevant sections
   - Check FAQs

2. **Try Troubleshooting Steps**
   - See Section 10 for common issues
   - Clear cache and try again
   - Test in different browser

3. **Prepare Information**
   - Your username (NOT password)
   - Detailed description of issue
   - Screenshot if applicable
   - Steps to reproduce problem

### 13.2 Contact Information

**Technical Support:**
- **GitHub Issues**: https://github.com/anthropics/finance-tracker/issues
- **Response Time**: 24-48 hours
- **Available**: Monday-Friday, 9 AM - 5 PM

**Account Issues:**
- Forgot password → Use "Forgot Password" link
- Account access → Contact via email
- Data issues → GitHub issues with details

### 13.3 Reporting Bugs

**How to Report:**

1. **Go to GitHub Issues**
2. **Click "New Issue"**
3. **Provide Details:**
   ```
   Title: Brief description

   Description:
   - What were you trying to do?
   - What happened instead?
   - Steps to reproduce
   - Browser and OS
   - Screenshot (if applicable)
   ```

4. **Submit and Monitor**
   - You'll get email notifications
   - Developers may ask for more info
   - Resolution posted on issue thread

### 13.4 Feature Requests

**Suggest New Features:**

1. **Check Existing Requests**
   - Search GitHub issues first
   - Vote/comment on existing requests
   - Don't duplicate requests

2. **Submit New Request**
   - Describe the feature
   - Explain use case
   - Why it's valuable
   - How it should work

**Current Roadmap:**
- Email budget alerts
- Receipt attachments
- Mobile app
- Recurring transactions
- Multi-currency support

### 13.5 Training & Resources

**Video Tutorials:**
- Coming soon on YouTube channel
- Step-by-step walkthroughs
- Feature demonstrations

**Written Guides:**
- This user manual (PDF available)
- Quick start guide
- Feature guides

**Community:**
- User forum (planned)
- Tips and tricks blog
- Best practices articles

### 13.6 Updates & Changelog

**Staying Updated:**
- Check GitHub for release notes
- Review changelog before major updates
- Subscribe to notifications

**Current Version:** 1.0
**Last Updated:** February 2026

**Recent Updates:**
- ✅ Field-level encryption for personal data
- ✅ Category management with icons/colors
- ✅ Bulk upload with validation
- ✅ Subcategory support
- ✅ Enhanced budget tracking

---

## Appendix A: Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Refresh page | F5 or Ctrl+R |
| Clear browser cache | Ctrl+Shift+Delete |
| Find in page | Ctrl+F |
| Select all | Ctrl+A |
| Copy | Ctrl+C |
| Paste | Ctrl+V |

---

## Appendix B: Data Format Reference

### Transaction CSV Format
```csv
Transaction Date (YYYY-MM-DD),Transaction Type (CREDIT/DEBIT),Amount,Category Name
2026-01-15,DEBIT,1500.50,Food
2026-01-20,CREDIT,50000,Salary
```

### Date Formats Accepted
```
YYYY-MM-DD  → 2026-01-15 ✅
YYYY/MM/DD  → 2026/01/15 ✅
DD-MM-YYYY  → 15-01-2026 ✅
DD/MM/YYYY  → 15/01/2026 ✅
```

### Amount Formats
```
Valid:
1000      ✅
1500.50   ✅
2500.00   ✅

Invalid:
-1000     ❌ (negative)
1,500     ❌ (commas)
₹1500     ❌ (currency symbol)
1500.505  ❌ (too many decimals)
```

---

## Appendix C: Glossary

**Balance**: Total income minus total expenses
**Budget**: Planned spending limit for a category
**Category**: Classification for transactions (e.g., Food, Rent)
**CREDIT**: Income transaction (money coming in)
**CSV**: Comma-Separated Values file format
**Dashboard**: Main overview page with summary and charts
**DEBIT**: Expense transaction (money going out)
**Export**: Download data from system
**Import**: Upload data to system
**Subcategory**: Category under a parent category
**Transaction**: Single income or expense entry

---

## Document Information

**Document Version:** 1.0
**Last Updated:** February 12, 2026
**Prepared By:** FinanceTracker Team
**For:** End Users

**Change Log:**
- v1.0 (2026-02-12): Initial release

---

**End of User Manual**

For questions or support, please refer to Section 13.

© 2026 FinanceTracker. All rights reserved.
