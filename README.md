# Lets ID

LetsID.ai is a free service provided by Autonomys Labs that allows users to easily create, register, and manage an Auto ID

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python (3.8 or later recommended)
- pip (Python package installer)
- git (Version control system)

### Cloning the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/subspace/letsid.git
cd letsid
```

### Setting Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies for your project. This keeps your global installation of Python clean and manages project-specific dependencies independently.

```bash
# Install virtual environment if you haven't installed yet
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

### Installing Dependencies

With your virtual environment activated, install the project dependencies using pip:

```bash
pip install -r requirements.txt
```

### Environment Variables

This project uses environment variables for configuration. Copy the example environment variables and set your own values:

```bash
cp .env.example .env
```

Now edit the .env file with your preferred editor

### Running the Application for development

To run the Flask application locally:

```bash
bash dev.sh
```

This command starts the Flask server on http://localhost:8080. You can open this URL in your web browser to view the application.

### RContributing

We welcome contributions! Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests to us.

### License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.

