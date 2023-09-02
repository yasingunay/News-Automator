
 # News Automator - CS50P Final Project
  #### Video Demo:  <https://youtu.be/iHCkeewtyvE>


This is a Python script that allows you to retrieve news articles and sources from the [News API](https://newsapi.org/). It provides the following functionalities:

- Get top headlines by category.
- Search for articles by a specific query.
- Get news sources by country.

## Prerequisites

Before using this script, make sure you have the following prerequisites:

- Python 3.x installed on your system.
- An API key from [News API](https://newsapi.org/) (set as the `NEWS_API_KEY` environment variable).



## Installation

Clone this repository to your local machine:



```bash
  git clone <repository-url>
```

Install the required Python packages:

```bash
  pip install requests
```
## Usage

You can run the script with the following command-line arguments:

- `action`: The action to perform (`category`, `query`, or `sources`).
- `value`: The category, query, or country (depending on the action).
- `--language` (optional): The language for query search (e.g., 'en' for English, 'fr' for French).

#### Get top headlines by category:
```bash
python news.py category <category>

```
Available categories: `business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`.

#### Search for articles by query:
```bash
python news.py query <query> [--language <language>]

```
#### Get news sources by country:
```bash
python news.py sources <country>

```

## Examples

#### Get top headlines by category:
```bash
python news.py category technology

```

#### Search for articles by query:
```bash
python news.py query Trump

```
or
```bash
python news.py query Trump --language en

```
#### Get news sources by country:
```bash
python news.py sources us

```
## Output

The script will display the titles, descriptions, and links to news articles or news sources based on your chosen action.



## Acknowledgments

- [News API](https://newsapi.org/) for providing the API service.

