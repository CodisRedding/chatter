# Chatter

Chatter is a Python project designed for idea management and analysis. It supports generating, critiquing, and storing ideas, with extensible features for technical and ethical review.

## Getting Started

1. **Clone the repository**
2. **Create and activate a Python virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the project root. Example:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     OTHER_SECRET=your_other_secret_here
     ```
   - Required variables:
     - `OPENAI_API_KEY`: Your OpenAI API key for AI-powered features.
     - Add any other secrets or API keys as needed for your extensions.

## Usage

- Run the main script:
  ```sh
  python chatter.py
  ```
- Ideas and critiques are stored in the `ideas/` folder (ignored by git).
- Customize `.env` for your API keys and secrets.

## Project Structure

- `chatter.py` — Main application script
- `requirements.txt` — Python dependencies
- `.env` — Environment variables (not tracked by git)
- `ideas/` — Generated idea files (ignored by git)

## Notes

- The `.env` file is required for API integrations. Never commit your secrets.
- The `ideas/` folder is ignored by git to keep generated content private.
- For more details, see comments in `chatter.py` or extend as needed.

## License

MIT License
