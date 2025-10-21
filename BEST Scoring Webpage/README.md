Run the scoring web server (Python + Flask)

Prerequisites

- Python 3.10+ (3.11+ recommended)
- pip

Install

```bash
pip install -r requirements.txt
```

Start server

```bash
python main.py
```

Then open http://localhost:5000/ in your browser to view `scoreboard.html` from the `public/` folder.

Notes

- To enable debug mode during development set `FLASK_DEBUG=1` in the environment.
- The server serves files from the `public/` directory and exposes a simple `/api/data` POST endpoint.
