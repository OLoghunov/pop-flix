# Pop-Flix

Pop-Flix is a web application, a parody of Kinopoisk, allowing users to search for movies, add them to "Watched" and "Planned" lists, and receive personalized recommendations.

## Features
- **Movie search** via Kinopoisk API.
- **Add movies** to "Watched" and "Planned" lists.
- **Update movie status** (e.g., from planned to watched).
- **Remove movies** from the user's list.
- **Recommendation system** based on watched movies.
- **Authentication and authorization** using JWT tokens.
- **Email verification** with Celery and RabbitMQ.
- **Containerization** using Docker and Docker Compose.

## Tech Stack
- **Backend:** FastAPI, PostgreSQL, Redis, Celery, RabbitMQ, asyncpg
- **Frontend:** HTML, CSS, JavaScript
- **Recommendations:** Kinopoisk API
- **Infrastructure:** Docker, Docker Compose

## Installation & Running

### Local Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/OLoghunov/pop-flix.git
   cd pop-flix
   ```
2. **Create a virtual environment and install dependencies:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. **Set up environment variables (.env):**
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   REDIS_URL=redis://localhost:6379
   SECRET_KEY=your_secret_key
   ```
4. **Run the application:**
   ```sh
   fastapi dev src
   ```

### Running with Docker
1. **Copy `.env.docker_example` to `.env.docker` and configure the variables.**
2. **Start the containers:**
   ```sh
   docker-compose up --build
   ```

## API Documentation
After starting the server, API docs are available at:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## TODO
- 📌 Add OAuth2 login (Google, VK, GitHub)
- 🔬 Improve recommendation algorithm
- 📊 Further develop the recommendation microservice

## Author
👨‍💻 **OLoghunov**  
📌 GitHub: [@OLoghunov](https://github.com/OLoghunov)
