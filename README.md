# 🌲 Cypress - Public Issue Reporting Platform

A user-friendly **public issue reporting application** that enables citizens to report street and campus-related issues, track their resolution, and receive real-time updates. Cypress connects users with the **correct city departments or campus security** using location-based reporting and map visualization.

---

## 👥 Authors

- Parmis Nouri  
- Silvia Das  
- Abisa Rajkumar  

---

## 📌 Project Overview

Cypress is designed to help citizens and students report public issues such as potholes, broken lights, fire hazards, and sidewalk damage, and track their resolution efficiently.

Key goals of the system include:
- Ensuring only **verified users** can submit reports  
- Helping users identify the **correct organization or department** responsible  
- Improving transparency by allowing users to track issue status in real time  

For example, students on campus can report safety or infrastructure issues near building entrances so others can avoid affected areas while the issue is being resolved. Campus security and city officials can monitor, update, and manage reports through an administrative interface.

---

## 🧱 Technologies & Concepts

- **Platform Type:** Mobile / Web Application (Concept & Design)  
- **Core Features:**  
  - Interactive map-based reporting  
  - Location-aware issue tracking  
  - Role-based access (Citizens vs. Officials)  
- **Concepts:**  
  - User stories & agile sprint planning  
  - Product backlog prioritization  
  - Location-based services  
  - Notifications & status tracking  
  - Data validation & abuse prevention  
  - Test planning & quality assurance  

---

## 🗺️ Core Features

### Citizen Functionality
- Report issues by selecting a **precise location on a map**
- Categorize issues (potholes, broken lights, fire hazards, etc.)
- Attach photos or videos to reports
- View nearby reported issues
- Track resolution status (`Pending`, `In Progress`, `Resolved`)
- Receive notifications for nearby or subscribed issues
- Search and filter issues by type, date, urgency, or location

### City Officials / Campus Security
- View all reported issues on a map
- Update issue status with timestamps
- Delete fake or inappropriate reports
- Monitor suspicious activity and duplicate submissions
- Ensure timely response and resolution

---

## 🧩 User Stories Implemented

- Report a street or campus issue using an interactive map  
- Automatically match issue type and location to the correct department  
- Track issue resolution progress through notifications  
- View and filter nearby issues reported by others  
- Detect and flag duplicate reports within a defined radius  
- Prevent spam and false reports via user verification  

---

## 🔍 Test Plan Overview

The Cypress test plan focuses on validating **core system functionality** and **administrative controls**.

### Key Test Areas
- User interface navigation  
- Map display and issue interaction  
- Issue reporting workflow  
- Status updates and notifications  
- Admin issue management (resolve, delete, flag reports)  

Each test case defines:
- Test inputs  
- Expected outputs  
- User or admin role involved  

This ensures a smooth user experience while maintaining system integrity and trustworthiness.

---

## 📊 System Design Highlights

- Location-based issue grouping using radius detection  
- Clear separation between **user-facing features** and **administrative controls**  
- Status tracking with timestamps for accountability  
- Media attachments linked directly to issue reports  
- Duplicate detection to reduce report clutter  
- Verification mechanisms to prevent false reporting  

---

## 📎 Notes

This project was developed as part of an academic software engineering course and demonstrates:

- Agile sprint planning and backlog management  
- User-centered application design  
- Location-aware system architecture  
- Test-driven thinking and quality assurance planning  
- Real-world problem solving for civic technology
