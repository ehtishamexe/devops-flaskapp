Project Requirements Document (PRD): "The Flight Log"
1. Project Overview
A minimalist, dark-themed, and witty web application designed to demonstrate full CRUD operations and basic cloud deployment on an AWS EC2 instance. The application serves as a satirical administrative portal for managing the infamous "VIP Flight Log" and its associated system administrators (fixers).

2. Tech Stack (The "Dead Simple" Approach)
Backend framework: Python (Flask) - Requires almost zero boilerplate.

Database: SQLite - Serverless and built directly into Python. Requires no installation, no credentials, and no external services.

Frontend: HTML5 / CSS3 (Using a dark-mode micro-framework like Pico.css or custom minimal CSS).

Deployment: Direct execution on AWS EC2 (python app.py) accessible via a public IPv4 address.

3. UI/UX Design & Theme
Aesthetic: Strict "Dark Mode". Deep charcoal/black backgrounds with stark white text and subtle red/orange accent colors for buttons (giving it a classified, late-night hacker vibe).

Tone: Highly satirical, classified, and mildly incriminating.

4. User Flow & Architecture
To ensure the professor easily navigates the application and grades the assignment quickly, the UX will follow a strict, linear flow with baked-in humor:

The Gate (Login Page)
Clean, centered login box on a dark background.

Header text: "Jeffery Epstein Island - Authorized Personnel Only."

Guest credentials prominently displayed on the screen to prevent grading friction:

Username: guest_admin

Password: i_plead_the_5th

The Command Center (Dashboard)
The hub of the application.

Hero text: "Welcome To Jeffery Epstein Island."

Sub-text: "Please ensure all tracking devices are turned off before modifying the logs."

Features two distinct, massive navigation buttons:

Path A: "Scrub The Flight Log" (Takes user to the VIP CRUD section).

Path B: "Manage The Fixers" (Takes user to the Admin CRUD section).

The CRUD Interfaces
Clean, dark-themed tables displaying existing data.

"Add New Accomplice" / "Add New Fixer" buttons at the top of their respective pages.

"Edit Alibi" and "Redact (Delete)" buttons next to every single entry.

5. Database Schema (Entities)
The application will manage two specific tables to satisfy the CRUD requirement twice over:

Entity 1: "The VIPs" (Public Figures)
ID: (Auto-incrementing Integer)

Name: (Text Input) - Placeholder text: "e.g., Prince A..."

Official Alibi: (Dropdown Menu)

Options: "Philanthropy Meeting", "Getting Financial Advice", "Never Met Him", "My PR Team Was Hacked", "Pleaded the 5th".

Entity 2: "The Fixers" (System Admins)
ID: (Auto-incrementing Integer)

Username: (Text Input) - Placeholder text: "Enter burner alias"

Password: (Text Input - plain text for simplicity, since security is explicitly not the goal of this assignment).

6. Deployment Strategy
Provision an AWS EC2 instance (Ubuntu/Amazon Linux).

Configure the Security Group to allow inbound HTTP traffic on port 80/8080.

SSH into the instance.

Clone the repository.

Run python app.py (SQLite will automatically create the database file the first time the script runs).