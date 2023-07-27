中文说明：https://github.com/Lovelumine/DangDang_Book_Scraper/blob/main/README_CN.md
# DangDang Book Scraper

This Python project aims to crawl detailed information about books from Dangdang.com and export it as a CSV file. 

## Features

1. **Login and Authentication**: This program will prompt you to manually log in to your DangDang account in a browser window. This step is crucial to bypass any potential CAPTCHA or Two-Factor Authentication.
2. **Book Information Scraping**: The scraper collects and organizes detailed information about a book based on your search input. The collected information includes the book's title, author, publisher, price, ISBN, publication time, and a brief description.
3. **Output to CSV**: After the scraping process, the book information is saved to a CSV file for further processing or analysis. The program allows you to specify the file's name and location via a GUI dialog.

## How to Use

1. **Install Required Libraries**: Before running the program, make sure you have installed the required Python libraries by running:

    ```
    pip install selenium beautifulsoup4 requests tkinter csv
    ```

2. **Run the Program**: Navigate to the directory where the main Python file is located and execute the command:

    ```
    python main.py
    ```

3. **Login to DangDang**: A browser window will pop up, and you will be prompted to log in to your DangDang account. After successful login, switch back to the terminal and press Enter.

4. **Enter Book Name**: Input the name of the book you want to search for. The program will fetch the detailed information about the book.

5. **Save to CSV**: Once you decide to terminate the program, type '退出并导出'. The program will prompt you to choose a file location to save the data to a CSV file. 

## Caution

This scraper is intended for educational purposes and personal use. Please respect DangDang's terms of service and do not use it for any activity that breaches them. 

## Contribution

Feel free to fork the project and make contributions. If you find any bugs or issues, please raise an issue in the GitHub repository.

## License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.

This repository is not affiliated with, maintained, sponsored or endorsed by DangDang.
