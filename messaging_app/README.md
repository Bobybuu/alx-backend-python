# Django RESTful API Development Project

## Overview
This project guides learners through the complete lifecycle of designing and implementing robust RESTful APIs using Django. Starting from project scaffolding to building scalable data models and establishing clean URL routing, this project emphasizes Django's best practices for creating maintainable, production-ready codebases.

## Project Objectives
By completing this project, learners will be able to:
- Scaffold a Django project using industry-standard structures
- Design and implement scalable data models using Django's ORM
- Establish various database relationships (one-to-many, many-to-many, one-to-one)
- Create modular Django apps with clean separation of concerns
- Configure URL routing for APIs using Django's path and include functions
- Build maintainable API layers using Django REST Framework
- Validate and test APIs with real data using tools like Postman

## Learning Outcomes
Upon completion, learners will:
- Understand Django project structure and proper scaffolding techniques
- Design relational database schemas based on feature requirements
- Use Django models and migrations effectively for data persistence
- Build RESTful API endpoints following conventions
- Apply modular development strategies with reusable apps
- Follow Django's naming and configuration conventions for better collaboration

## Key Implementation Phases

### 1. Project Setup and Environment Configuration
- Create virtual environment and install Django
- Scaffold project with `django-admin startproject` and `python manage.py startapp`
- Configure settings.py (INSTALLED_APPS, middleware, CORS, etc.)

### 2. Defining Data Models
- Identify core models based on requirements
- Use Django ORM to define model classes with proper field types and constraints
- Apply migrations and use Django Admin for verification

### 3. Establishing Relationships
- Implement foreign keys, many-to-many relationships, and one-to-one links
- Use related_name, on_delete, and reverse relationships effectively
- Test object relations using Django shell

### 4. URL Routing
- Define app-specific routes using urls.py
- Use include() to modularize routes per app
- Follow RESTful naming conventions with versioned APIs

## Project Tasks

### Task 0: Project Setup
**Objective**: Create a new Django project and install Django REST Framework

**Instructions**:
```bash
django-admin startproject messaging_app
pip install djangorestframework
python manage.py startapp chats
```

Add 'rest_framework' and 'chats' to INSTALLED_APPS in settings.py

### Task 1: Define Data Models
**Objective**: Design models for users, messages, and conversations

**Database Specification**:
- **User**: Extended AbstractUser with additional fields
- **Conversation**: Tracks participants in conversations
- **Message**: Contains sender, conversation, and message content

### Task 2: Create Serializers
**Objective**: Build serializers for models with proper relationship handling

**Instructions**:
- Create serializers for User, Conversation, and Message models
- Ensure nested relationships are handled properly
- Include messages within conversation serializers

### Task 3: Build API Endpoints
**Objective**: Implement API endpoints for conversations and messages

**Instructions**:
- Use viewsets from DRF for listing conversations and messages
- Implement endpoints for creating conversations and sending messages
- Ensure proper authentication and permissions

### Task 4: Set Up URL Routing
**Objective**: Configure URLs for conversations and messages

**Instructions**:
- Use Django REST Framework's DefaultRouter for automatic route creation
- Include routes in main project's urls.py with appropriate API paths
- Implement versioned APIs (e.g., /api/v1/)

### Task 5: Run and Test Application
**Objective**: Test the application and fix any errors

**Instructions**:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
- Test API endpoints using Postman or similar tools
- Fix any bugs or errors encountered

## Best Practices

### Project Structure
- Keep modular structure with reusable apps
- Consistent naming and organized folders (apps/, core/, etc.)

### Environment Configuration
- Use .env files and django-environ for secret management
- Separate development and production settings

### Models & Migrations
- Avoid business logic in models
- Commit migration files and test on fresh databases

### Security
- Use ALLOWED_HOSTS properly
- Avoid hardcoding credentials
- Enable CORS appropriately

### Documentation
- Add inline comments
- Maintain clear README
- Use tools like Swagger for API documentation

## Assessment
Your project will be evaluated through:
- ✅ Timely completion
- 📄 Submission of all required files
- 🔗 Generated review link
- 👥 Peer reviews

An auto-check will verify the presence of core files needed for manual review.

**Important**: Generate your review link before the deadline to ensure evaluation.

We're here to support your learning journey. Happy coding! 
