#Breadventory: Bakery Management System

> **Note:** This was a finals project for my **AppIntr** class at **DLS-CSB**. I developed this for my parents' bakery business as a proof of concept, and I plan to improve it as they scale larger.

---

## Setup Instructions

### 1. Prerequisites
Ensure you have Python installed. You can check your version in the terminal:

```bash
python --version
2. Environment Setup
Clone the repository and enter the project directory:

Bash
git clone [https://github.com/Not-Artorias/Final-Project-Breadventory.git](https://github.com/Not-Artorias/Final-Project-Breadventory.git)
cd Final-Project-Breadventory
3. Install Dependencies
Create a virtual environment and install the necessary libraries from the requirements.txt file:

Bash
# Create and activate environment
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
4. Initialize Database & Server
Run the migrations to set up your SQLite database and start the development server:

Bash
python manage.py migrate
python manage.py runserver
