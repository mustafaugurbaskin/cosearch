# CoSearch

CoSearch is a Python-based tool designed to streamline lead generation for businesses. It automates the process of finding business information, including websites, phone numbers, email addresses, and LinkedIn profiles, making it faster and more efficient than manual methods.

---

## Features

- **Bulk Business Information Finder:** Upload a `.txt` file containing a list of business names, and CoSearch retrieves relevant information in bulk.
- **Single Business Information Finder:** Search for information about individual businesses.
- **Integrated Output:** Saves results into an Excel file for easy access and sharing.
- **Customizable and Scalable:** Modular design allows for easy integration and updates.

---

## Setup and Installation

### Prerequisites

- Python 3.7 or later
- Required libraries listed in `requirements.txt`

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/mustafaugurbaskin/cosearch.git
   cd cosearch
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Prepare the necessary files:
   - Add the required logo and icons in the `logo/` and `icons/` directories.
   - Ensure you have valid API keys for the search functionality.
4. Run the application:
   ```
   python cosearchgui.py
   ```

## Usage

### Bulk Search
1. Prepare a `.txt` file listing business names (one business name per line).
2. Place the `.txt` file in the same directory as the application.
3. Run the application:
   ```
   python cosearchgui.py
   ```
4. Use the "Upload File" button to load the .txt file.
5. CoSearch will process the list and save the results in an Excel file in the same directory.

### Single Search

1. Run the application:
   ```
   python cosearchgui.py
   ```
2. Use the "Single Business Information Finder" option in the application interface.
3. Enter the business name into the provided input field.
4. Start the search by clicking the "Search" button.
5. The results will:
   - Be displayed on the application interface.
   - Automatically save to an Excel file in the application directory for further use.
