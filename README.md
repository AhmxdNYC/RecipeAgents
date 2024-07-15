# RecipeAgents

RecipeAgents is a personalized recipe recommendation system that generates tailored recipes based on user dietary preferences and available ingredients. This project utilizes the LangGraph framework for defining agent workflows and the Tavily API for fetching recipe data.

## Table of Contents

- [Architecture](#architecture)
- [Agents](#agents)
  - [User Input Agent](#1-user-input-agent)
  - [Recipe Fetching Agent](#2-recipe-fetching-agent)
  - [Recipe Filtering Agent](#3-recipe-filtering-agent)
  - [Recipe Summarization Agent](#4-recipe-summarization-agent)
  - [Output Agent](#5-output-agent)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## architecture

![Diagram](./website//public/diagram.png "Diagram")

## Agents

- out of date

### 1. User Input Agent

**Task:** Collects user preferences such as dietary restrictions and available ingredients.

```python
 # assumptions of what it will look like
class UserInputAgent:
    def get_user_input(self):
        return {
            "preferences": "vegan",
            "ingredients": ["tomato", "spinach"]
        }
```

### 2. Recipe Fetching Agent

**Task:** Uses the Tavily API to search for recipes based on the input data.

```python
 # assumptions of what it will look like
class RecipeFetchingAgent:
    def fetch_recipes(self, preferences, ingredients):
        api_key = "XXX"
        query = f"{preferences} recipes with {', '.join(ingredients)}"
        url = f"https://api.tavily.com/query?api_key={api_key}&q={query}"
        response = requests.get(url)
        return response.json()

```

### 3. Recipe Filtering Agent

**Task:** Filters recipes based on dietary preferences.

```python
 # assumptions of what it will look like
class RecipeFilteringAgent:
    def filter_recipes(self, recipes, preferences):
        return [recipe for recipe in recipes if preferences in recipe['tags']]
```

### 4. Recipe Summarization Agent

**Task:** Summarizes recipes into an easy-to-read format.

```python
 # assumptions of what it will look like
class RecipeSummarizationAgent:
    def summarize_recipes(self, recipes):
        return [{"title": recipe['title'], "summary": recipe['summary']} for recipe in recipes]
```

### 5. Output Agent

**Task:** Presents the personalized recipes to the user.

```python
class OutputAgent:
    def display_recipes(self, summaries):
        for summary in summaries:
            print(f"Title: {summary['title']}\nSummary: {summary['summary']}\n")
```

## Getting Started

### Prerequisites

- Python 3.x
- Tavily API key (sign up for an API key at [Tavily](https://api.tavily.com))
- Requests library (`pip install requests`)
- LangGraph library (`pip install langgraph`)

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/AhmxdNYC/RecipeAgents.git
   cd RecipeAgents
   ```

2. Install the required dependencies:

- double check this
  ```sh
   pip install requests langgraph
  ```

3. Set up your Tavily API key:

- Replace `YOUR_WAVILY_API_KEY` with your actual Tavily API key in the `RecipeFetchingAgent` class.

## Usage

- Run the main workflow:

## Project Structure

- Agents folder: contains implementation of all agents

- Workflow folder: contains implementation of workflow

- README.md: Project documentation.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## Acknowledgements

- Tavily API for providing the recipe data.
- LangGraph for the workflow framework.
