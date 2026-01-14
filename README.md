# VisionCare AI

## Overview
VisionCare AI is an advanced web-based application that uses artificial intelligence to detect and analyze eye diseases from retinal fundus images. The system can identify conditions like Cataracts, Diabetic Retinopathy, and Glaucoma with high accuracy, providing users with preliminary diagnostic insights.

## Features
- **AI-Powered Analysis**: Utilizes a deep learning model (MobileNetV2) trained on thousands of retinal images
- **User Authentication**: Secure login and registration system
- **Real-time Detection**: Instant analysis of uploaded fundus images
- **Comprehensive Reports**: Detailed PDF reports with confidence scores and recommendations
- **History Tracking**: View and manage past analyses
- **Responsive Design**: Modern, mobile-friendly web interface

## Technology Stack
- **Backend**: Python Flask
- **Database**: MySQL
- **AI/ML**: TensorFlow, OpenCV
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **PDF Generation**: ReportLab

## Key Components
- **Disease Detection**: Identifies 4 classes - Normal, Cataract, Diabetic Retinopathy, Glaucoma
- **Image Processing**: Automatic preprocessing and feature extraction
- **User Management**: Registration, login, and session management
- **Report Generation**: Professional PDF reports with embedded images