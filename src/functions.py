function_list ={
    "run_datagen": {
        "name": "run_datagen",
        "description": " Runs the data generation script with email address to generate necessary files in './data/'",
        "parameters": {
            "type": "object",
            "properties": {
                "user_email": {"type": "string", "description": "Email address of user."},
            },
            "required": ["user_email"],
            "additionalProperties": False
        }
    },
    "count_days": {
        "name": "count_days",
        "description": "Count the number of Wednesdays in a given file.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing dates."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."},
                "day_name": {"type": "string", "description": "Name of the day, If the day name is given in plural format like Wednesdays, change it to singular format Wednesday, and if name of day is any other language translate it to english language."}
            },
            "required": ["source_file", "output_file","day_name"],
            "additionalProperties": False
        }
    },
    "format_md": {
        "name": "format_md",
        "description": "Format a Markdown file using Prettier.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing markdown file."},
                },
            "required": ["source_file"],
            "additionalProperties": False
        }
    },
    "sort_contacts": {
        "name": "sort_contacts",
        "description": "Sorts contacts in a JSON file by last name, then first name.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing contacts file."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."},
                "sort_field": {"type": "string", "description": "Field on which we have to sort source file."}
                },
            "required": ["source_file", "output_file", "sort_field"],
            "additionalProperties": False
        }
    },
    "get_recent_logs": {
        "name": "get_recent_logs",
        "description": "Fetch the first line from the 10 most recent .log files.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing logs."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."},
                "recent": {"type": "string", "description": "This tells of how much recent logs we want."}
                },
            "required": ["source_file", "output_file", "recent"],
            "additionalProperties": False
        }
    },
    "generate_md_index": {
        "name": "generate_md_index",
        "description": "Creates an index of Markdown files in the /data/docs directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing md files."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
                },
            "required": ["source_file", "output_file"],
            "additionalProperties": False
        }
    },
    "extract_sender_email": {
        "name": "extract_sender_email",
        "description": "Extracts the sender's email address from an email file.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing email."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
                },
            "required": ["source_file", "output_file"],
            "additionalProperties": False
        }
    },
    "extract_credit_card_number": {
        "name": "extract_credit_card_number",
        "description": "Extracts a credit card number from an image and saves it without spaces.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing credit card image."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
                },
            "required": ["source_file", "output_file"],
            "additionalProperties": False
        }
    },
    "find_most_similar_comments": {
        "name": "find_most_similar_comments",
        "description": "Finds the two most similar comments in a text file using embeddings.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing comments file."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
                },
            "required": ["source_file", "output_file"],
            "additionalProperties": False
        }
    },
    "calculate_gold_ticket_sales": {
        "name": "calculate_gold_ticket_sales",
        "description": "Calculates total sales for 'Gold' tickets in the database.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {"type": "string", "description": "Path to the file containing database."},
                "output_file": {"type": "string", "description": "Path where the result should be saved."}
                },
            "required": ["source_file", "output_file"],
            "additionalProperties": False
        }
    },
    "fetch_api_data": {
        "name": "fetch_api_data",
        "description": "Fetches data from an API and saves it as a JSON file.",
        "parameters": {
            "type": "object",
            "properties": {
                "api_url": {"type": "string", "description": "The URL of the API to fetch data from."},
                "output_file": {"type": "string", "description": "Path where the API response should be saved."}
            },
            "required": ["api_url", "output_file"],
            "additionalProperties": False
        }
    },
    "clone_and_commit": {
        "name": "clone_and_commit",
        "description": "Clones a GitHub repository and makes a commit.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_url": {"type": "string", "description": "URL of the GitHub repository."},
                "commit_message": {"type": "string", "description": "Commit message for the changes."}
            },
            "required": ["repo_url", "commit_message"],
            "additionalProperties": False
        }
    },
    "run_sql_query": {
        "name": "run_sql_query",
        "description": "Runs an SQL query on SQLite or DuckDB database.",
        "parameters": {
            "type": "object",
            "properties": {
                "db_file": {"type": "string", "description": "Path to the database file."},
                "query": {"type": "string", "description": "SQL query to execute."},
                "output_file": {"type": "string", "description": "Path where query result should be saved."}
            },
            "required": ["db_file", "query", "output_file"],
            "additionalProperties": False
        }
    },
    "scrape_website": {
        "name": "scrape_website",
        "description": "Extracts and saves data from a given website URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Website URL to scrape."},
                "output_file": {"type": "string", "description": "Path where scraped data should be saved."}
            },
            "required": ["url", "output_file"],
            "additionalProperties": False

        }
    },
    "resize_image": {
        "name": "resize_image",
        "description": "Resizes an image to specified dimensions.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to the image file."},
                "output_path": {"type": "string", "description": "Path where the resized image should be saved."},
                "width": {"type": "integer", "description": "Width of the resized image."},
                "height": {"type": "integer", "description": "Height of the resized image."}
            },
            "required": ["image_path", "output_path"],
            "additionalProperties": False

        }
    },
    "transcribe_audio": {
        "name": "transcribe_audio",
        "description": "Transcribes speech from an MP3 file into text.",
        "parameters": {
            "type": "object",
            "properties": {
                "audio_path": {"type": "string", "description": "Path to the MP3 audio file."},
                "output_text_file": {"type": "string", "description": "Path where the transcribed text should be saved."}
            },
            "required": ["audio_path", "output_text_file"],
            "additionalProperties": False

        }
    },
    "convert_md_to_html": {
        "name": "convert_md_to_html",
        "description": "Converts a Markdown file into an HTML file.",
        "parameters": {
            "type": "object",
            "properties": {
                "md_file": {"type": "string", "description": "Path to the Markdown file."},
                "output_html_file": {"type": "string", "description": "Path where the HTML file should be saved."}
            },
            "required": ["md_file", "output_html_file"],
            "additionalProperties": False

        }
    },
    "filter_csv": {
        "name": "filter_csv",
        "description": "Filters a CSV file by a column value and saves the result as JSON.",
        "parameters": {
            "type": "object",
            "properties": {
                "csv_file": {"type": "string", "description": "Path to the CSV file."},
                "filter_column": {"type": "string", "description": "Column name to filter by."},
                "filter_value": {"type": "string", "description": "Value to match in the filter column."},
                "output_json_file": {"type": "string", "description": "Path where the filtered JSON should be saved."}
            },
            "required": ["csv_file", "filter_column", "filter_value", "output_json_file"],
            "additionalProperties": False

        }
    },
}
