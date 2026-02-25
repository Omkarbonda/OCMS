# Online Course Management System (OCMS)

A robust platform built with Django for managing online courses, student enrollments, and user roles.

## 🚀 Features

-   **Role-Based Access Control**: Separate dashboards for Students, Instructors, and Administrators.
-   **Course Management**: Create, update, and browse a wide variety of courses.
-   **Student Enrollments**: Track course progress and status.
-   **Reviews & Ratings**: Students can leave feedback on courses.
-   **Modern UI**: Sleek, responsive design using Vanilla CSS.

## 🛠️ Technology Stack

-   **Backend**: Django
-   **Frontend**: HTML5, Vanilla CSS
-   **Database**: SQLite (default / development)

## 💻 Getting Started

### Prerequisites

-   Python 3.x
-   pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Omkarbonda/OCMS.git
    cd OCMS
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

## 📂 Project Structure

-   `accounts/`: User authentication and profiles.
-   `courses/`: Course creation and management logic.
-   `dashboard/`: Role-specific view logic.
-   `enrollments/`: Handling student-course relationships.
-   `reviews/`: Course feedback system.
-   `static/`: CSS and asset files.
-   `templates/`: HTML structure.
