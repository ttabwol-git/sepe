# SEPECheck
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/160ab9d6850840388dc3f2798c7220db)](https://app.codacy.com/gh/ttabwol-git/sepe/dashboard)
![Known Vulnerabilities](https://snyk.io/test/github/ttabwol-git/sepe/badge.svg)

Finding an available appointment at a SEPE (Servicio Púbico de Empleo Estatal) office can be a frustrating experience — especially when you’ve just lost your job and need to apply for unemployment subsidies as soon as possible. Appointments are often booked out, and checking availability manually is time-consuming and unreliable.

This application automates the process of finding SEPE office appointments. It allows users to subscribe to notifications for specific postal codes, validate their subscriptions, and remove them when no longer needed. The system is designed to save time and reduce stress by providing a reliable and efficient way to monitor appointment availability.

**Notes**: The project is in its early stages and is not yet fully functional. The code is not optimized for production use and may contain bugs. It is intended for educational purposes only.

This project has been developed by **Xabi Moreno** <xabi.moreno.maya@gmail.com>.

## 1. File Structure
```
project-root/
├── .github/                 # GitHub actions
├── app/                     # Backend application (Python – FastAPI)
├── ui/                      # Frontend application (Next.js – React)
├── README.md                # Project documentation
├── .gitignore               # Git ignore file
└── docker-compose.yml       # Docker compose file
```

## 2. Requirements
- Docker >= 28.0.4
- Docker Compose >= 2.29.1

**Notes**: The project has been tested on UNIX systems. It may work on other platforms, but it is not guaranteed.

## 3. Usage
```bash
# Clone the repository
git clone git@github.com:ttabwol-git/sepe.git

# Change to the project directory
cd sepe

# Build the application
docker compose build

# Start the application
docker compose up
```
The application will be available at `http://localhost:3000` (frontend) and `http://localhost:8000` (backend). Keep the terminal open to see the logs. You can stop the application by pressing `Ctrl + C` in the terminal.

## 4. Backend - API
### 4.1. File Structure
```
app/
├── data/                     # JSON data files
├── src/                      # Main application file
│   ├── app.py                # Main engine
│   ├── logs.py               # Logging utilities
│   ├── schemas.py            # Data schemas
│   └── smtp.py               # SMTP utilities (not used yet)
├── .env                      # Environment variables
├── .api.py                   # Main entry point - API routers
├── Dockerfile                # Dockerfile
├── poetry.lock               # Python dependencies
└── pyproject.toml            # Python project configuration
```

### 4.2. Environment Variables
The application uses environment variables for configuration. Create a `.env` file in the `app/` directory with the following content:
```env
SECRET_KEY=your_secret_key
```
You can generate a random secret key from [here](https://fernetkeygen.com/).

### 4.3. Stack
- **FastAPI**: Web framework for building APIs.
- **uvicorn**: ASGI server.
- **pydantic**: Data validation.
- **aiohttp**: Asynchronous HTTP client.
- **cryptography**: Encryption and decryption.
- **loguru**: Logging library.
- **dotenv**: Environment variable management.

### 4.4. API Endpoints
- `GET /postal`: Get a list of postal codes.
- `POST /subscription/queue`: Queue a subscription.
- `GET /subscription/validate`: Validate a subscription.
- `GET /subscription/remove`: Remove a subscription. 

For more details, refer to the [API documentation](http://localhost:8000/docs) after starting the application.

### 4.5. Linting and Formatting
The project uses [Black](https://black.readthedocs.io/en/stable/) for code formatting [Ruff](https://docs.astral.sh/ruff/) for linting.


## 5. Frontend - UI
### 5.1. File Structure
```
ui/
├── public/              # Public assets
├── src/                 # Main application files
│   ├── api/             # API client
│   ├── app/             # Main application
│   └── components/      # Reusable components
├── .env                 # Environment variables
├── Dockerfile           # Dockerfile
├── eslint.config.ts     # Eslint configuration
├── next.config.ts       # Next.js configuration
├── package.json         # Node.js dependencies
├── package-lock.json    # Node.js lock file
├── postcss.config.mjs   # PostCSS configuration
├── tsconfig.json        # TypeScript configuration
└── yarn.lock            # Yarn lock file
```

### 5.2. Environment Variables
The application uses environment variables for configuration. Create a `.env` file in the `ui/` directory with the following content:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5.3. Stack
- **Next.js**: React framework.
- **Tailwind CSS**: CSS framework.
- **Catalyst**: UI component library.

## 5.4. Linting and Formatting
The project uses [Prettier](https://prettier.io/) for code formatting and [ESLint](https://eslint.org/) for linting.

## 6. CD/CI
The project uses GitHub Actions for continuous integration and deployment. The workflow is defined in the `.github/workflows/build.yml` file. The workflow runs on every push to the `main` branch and performs the following steps:
- Build the Docker images for the backend and frontend applications.
- Push the images to repository.

## 7. Next Challenges

### 7.1. SMTP Client
The SMTP client is not yet implemented. By the moment, token validations are done using a simple GET request and the API is currently exposing the token. The plan is to implement a third party email system to send emails and notifications. This will be implemented in the future.

### 7.2. Unit Tests
The project does not currently have unit tests. The plan is to implement unit tests for the backend and frontend applications. This will be implemented in the future.

### 7.3. Splitting the Backend
Both the engine that runs the subscriptions on the background and the API are asynchronously executed in the same process. If this were to be deployed in high-demand production environment, the engine should be separated from the API. This would ensure that only one engine is running and subscriptions are reused while keeping the API elastic and responsive. This will be implemented in the future.