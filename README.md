# AiCore Scenario - Data Handling

This project aims to develop a data management system for a multinational company. In particular, the organization operates in various countries, but its data is currently spread across multiple sources, making it challenging to access and analyze.

The primary objective of this project is to develop a system that stores the company's data in a database, enabling easy access from a centralized location, and allowing the team to query the relational database for up-to-date business metrics.

## Milestone 1
In Milestone 1, the focus was on setting up the development environment. This involved installing the necessary tools and libraries required to run the program. A virtual environment was created to keep the dependencies for the project isolated from the other projects on the machine. This step helped to avoid potential conflicts with other projects.

## Milestone 2
In Milestone 2, a new database was set up and the data extracted from various sources, such as PDF documents, an AWS RDS database, RESTful API, JSON, and CSVs. To realized that, three classes were created - `DataExtractor`, `DataCleaning`, and `DatabaseConnector` - which contain methods to extract, clean, and connect the data to the database.

These classes were designed to provide an efficient and straightforward process for handling the data from multiple sources and ensure its accuracy and consistency. Overall, this represents a significant step towards centralizing the company's sales data and enabling the team to access it more efficiently.

## Milestone 3
In Milestone 3, I have developed the star-based schema of the database in SQL, ensuring that the columns are of the correct data types. This design has a simple structure that enables faster querying and aggregation of data. The database schema includes one fact table that contains the primary metrics and several dimension tables with the attributes that provide context to the analysis.

## Milestone 4
In order to integrate the game with the model, I used the _OpenCV_ library to capture frames from the webcam. Then, I utilize the `cv2.resize()` function to resize the frames, which is the input size of the pre-trained model.  Finally, I employed `cv2.imshow()` to display the original frame on the screen, and the `model.predict()` function to get the predicted class of the resized image.

## Conclusion
To improve the functionality of the program, the following features could have been implemented:
- **Scorekeeping** - A scoring system that keeps track of the number of rounds won by the user and the computer, and displays the score on the screen;
- **GUI** - A graphical user interface (GUI) library, such as _Pygame_ or _Tkinter_, to create a more user-friendly interface for the game.