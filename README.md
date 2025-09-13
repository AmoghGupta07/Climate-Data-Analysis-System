# Climate-Data-Analysis-System
Semester-1 Gorup Project built in Python.
25BCE2437 Areeb Ali Khan
25BCE2414 Sidharth P Nair
25BCE2394 Amogh Gupta
25BCE2427 Shashank Reddy
25BCE2459 Bonda Uma Venkata Varalakshmi
Project Title: Climate Data Analysis System (Admin & Researcher CLI
System)
1. Overview
This project simulates a climate data management and research
portal where Admins can manage climate datasets, update records, and generate
analytics, while Researchers can analyse climate patterns, query datasets, and
download reports. The project will be menu-driven, CLI-based in Python, and
use JSON/CSV for storage with full CRUD (Create, Read, Update,
Delete) functionality.
2. Roles & Features
Admin Functionalities (Menu Options)
• Login as Admin.
• Add / Update / Delete climate data records (region, date, temperature,
rainfall, CO₂ levels, humidity).
• Upload bulk data (CSV/JSON import).
• Manage climate categories (air quality, temperature, rainfall, emissions).
• Generate reports (monthly/annual climate trends, anomalies, extreme
events).
• Approve researcher access requests.
Researcher Functionalities (Menu Options)
• Register as a new researcher (name, organization, field of study, contact).
• Login with Researcher ID.
• Search & filter climate data (by region, time period, parameter).
• Perform basic analysis (avg/max/min values, trend detection).
• Generate and export reports (CSV/JSON).
• View data visualizations (tables/summary statistics).
• Logout.
3. Data Handling
External Storage → JSON/CSV files for persistence.
Files / Tables Needed:climate_data.json → (record_id, region, date, temperature, rainfall,
co2_level, humidity).
• researchers.json → (researcher_id, name, org, field, contact).
• reports.json →
(report_id,
researcher_id,
type,
parameters,
generated_on).
• categories.json → (cat_id, name, description).
• access.json → (req_id, researcher_id, status, approved_by).
CRUD Examples:
• Admin → CRUD on climate data, categories, and researcher access.
• Researcher → CRUD on reports, manage profile, query datasets.
•
4. Tech Stack
• Python
• Libraries:
o json → data storage.
o tabulate → display data in tables.
o datetime → date-based queries and trends.
o (Optional) matplotlib / pandas → extended analysis & graphs (if
CLI allows exporting).
5. Sample CLI Flow
=== Climate Data Analysis System ===
1. Admin Login
2. Researcher Login
3. Register as New Researcher
4. Exit
(Admin Logs In)
--- Admin Menu ---
1. Add Climate Record
2. Update/Delete Climate Data
3. Manage Categories
4. Upload Bulk Data
5. Generate Reports
6. Manage Researcher Access
7. Logout
(Researcher Logs In)
--- Researcher Menu ---
1. Search Climate Data
2. Perform Analysis
3. Generate Report
4. Export Report5. View Profile
6. Logout
6. Dataset Suggestion
• Synthetic dataset for testing:
o Climate records of 10 regions over 5 years (temperature, rainfall,
CO₂, humidity).
o 5 categories: Temperature, Rainfall, Air Quality, CO₂ Emissions,
Humidity.
o 10 researchers with different organizations & fields of study.
o 20 reports generated (monthly & yearly summaries).
• Or use public datasets like:
o NASA Earth Science Data.
o NOAA Climate Data Records.
o Kaggle climate datasets (global temp & emissions).
