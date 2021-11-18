# books-scraping
This program extracts product (books) information details from the website [books.toscrape.com](https://books.toscrape.com/),
and loads the output into a .CSV file per book category.
The picture of each product is also downloaded into a separate folder.

## How to use
Please follow the next steps in order.

### Prerequisites
* A command terminal (on Windows PowerShell is enough)
* Python3 version >= 3.7.1 (check with command `python -V`)

### 1 - Download the necessary files
* Download the zip from the following link: 
[https://github.com/[...]/main.zip](https://github.com/Wil31/books-scraping/archive/refs/heads/main.zip)
* Extract the zip

### 2 - Configure a virtual environment
* Open a command terminal
* Navigate to the folder you extracted _([...]\books-scraping-main)_
* Use command `python -m venv env` to create a new environment
* Activate the environment with `.\env\Scripts\activate` (`source env/bin/activate` on Linux)
* Install the Python packages with `pip install -r .\requirements.txt`

### 3 - Execute the code
* Be sure you are in the folder you extracted _([...]\books-scraping-main)_
* Execute the program with command `py.exe .\main.py`
* At the end of execution you will find a new folder /data, with a CSV file for each book category, and another 
folder /images with every product picture.