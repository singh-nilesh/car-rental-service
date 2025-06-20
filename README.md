# 🚗 Peer-to-Peer Rental Car System

This is a **Service-Oriented Architecture (SOA)** based web application for a **peer-to-peer car rental platform**. Users can either **rent cars** from others or **upload their own cars** to rent out. The system handles all communication and bookings.

---

## 🏗️ Architecture Overview

### 🔧 Tech Stack
- **Frontend:** Angular
- **Backend:** Flask (REST API)
- **Architecture:** SOA (Service-Oriented Architecture)
- **Services:**
  - `user-service`: Handles user registration and login
  - `inventory-service`: Manages car listings and image uploads
  - `order-service`: Handles bookings and order tracking
  - **Database:** Each service has its own database (can be SQL/NoSQL based on need)

---

## 🔩 Services Breakdown

### 1. 👤 User Service
- User registration and authentication
- Role: owner, renter, or both
- Profile management
- (Optional) KYC/verification

### 2. 🚘 Inventory Service
- Add/update/delete cars for renting
- Upload images of the car (via `multipart/form-data`)
- Manage availability and car details
- Associate cars with user IDs

### 3. 📦 Order Service
- Book cars for a specified duration
- Booking lifecycle: requested → confirmed → completed/cancelled
- Calculate total cost
- (Optional) Integrate with payment gateway (e.g., Razorpay/Stripe)

---
