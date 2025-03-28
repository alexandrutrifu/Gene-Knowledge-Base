# 🧬 Gene Knowledge Base – Web Application

## 📖 Overview

This project consists in the prototype of a **full-stack web service** aimed towards analyzing **gene activity levels** (and the significance of their changes) across different age groups. Through the employment of **customizable data samples** and **interactive visualization tools**, we offer a scalable solution that facilitates the validation of experimental conclusions, backed by external, public gene knowledge.

## 🚀 Features
- **Interactive plot visualization**
  - Used a _volcano plot_ to visualize the significance level of gene regulation in relation with donor age.
  - Further observed age-related changes in the value-ranges of protein concentration, using _boxplots_.

- Extracted & parsed public information from the **PubMed database** on the purpose and implications of gene regulation, using **REST API requests**.
- Summarized and concluded analytical results with the help of **LLM processing** and **OpenAI API** calls.
- Included the option to **import other statistical datasets** in order to assess their relevance through chosen **parametric tests**.

## 🧰 Tech Stack
| Layer       | Technologies   |
|-------------|----------------|
| Frontend    | _HTML, CSS, JS_ |
| Backend     | _Python, Flask_ |
| Visualization | _Bokeh_ |
| Data        | _Gene datasets, custom samples, PubMed references_|

## 🖥️ Getting Started

### Installation
```bash
# Clone the repo
git clone https://github.com/your-username/gene-knowledge-base.git

# Navigate to project directory
cd gene-knowledge-base

# Set up virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python run.py
```

### Environment Setup
Create a `.env` file in the root directory and add the following:`OPENAI_API_KEY=your_openai_key_here`

### After running the server
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🧑‍💻 Implementation

### 0. Project Structure

The project follows the file-tree structure of a standard Flask-based application:

```
gene-knowledge/
├── app/               # Core backend logic, routes, and app initialization
├── database/          # Database schema & sample data
│
├── static/            # Static frontend assets (CSS, fonts, images, JS)
│   ├── css/           # Custom stylesheets
│   ├── fonts/         # Web fonts used in the UI
│   ├── images/        # Icons & logos
│   └── js/            # Frontend JavaScript logic
│
├── templates/         # HTML templates rendered by Flask (Jinja2)
│
├── package.json       # Node.js dependencies and scripts
├── package-lock.json  # Exact dependency tree for reproducible installs
├── README.md          # Project documentation (you're reading it!)
├── requirements.txt   # Python package dependencies
└── run.py             # Entry point to launch the Flask app
```

### 0.1. Python Modules


The `app/` directory contains the following .py modules:

- `ai_interaction.py`
  - Handles all communication with the OpenAI API. It defines prompts and provides functions to either stream or return a full static response based on the user’s request.
- `data_interaction.py`
  - Handles all logic related to loading, cleaning, and extracting gene data from the SQLite database, and integrates with the AI module to enrich data with PubMed reference summaries.
- `dataframes.py`
  - Acts as a shared memory module for storing and accessing key dataframes and reference information across different parts of the app.
- `donor_plot.py`
  - Generates a custom Bokeh box plot to visualize protein concentration differences between young and elderly donor samples for a given gene.
- `gene_requests.py`
  - Fetches literature references related to a specific gene using the MyGene.info API. These references are later used by the AI module to summarize PubMed findings.
- `routes.py`
  - Defines all Flask web routes for the application, handling everything from home page rendering to dynamic gene analysis using AI and visualizations.
- `volcano_plot.py`
  - Generates an interactive volcano plot using Bokeh to visualize differential gene expression — highlighting log fold changes and statistical significance.

### 1. Application Logic



