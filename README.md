# Tender-Document-Analyzer

I developed a Document Analyzer application utilizing the ChatGPT API from OpenAI, designed to process tender documents. The application is built on Django, providing a robust framework for our web application, which consists of four main pages: Login, Signup, Upload, and Results.
The core functionality begins with converting PDF documents into text. This is achieved through a reliable text extraction process. Following this, I implemented Python’s Regex library to meticulously extract dates from the converted text.
After refining the process through extensive experimentation with token sizes and chunking strategies, I established optimal parameters for the API interactions. This approach has resulted in highly accurate and relevant outputs.
To enhance user experience, the application displays the AI-generated insights alongside the original PDF text, enabling straightforward comparison and verification of the information extracted by the AI. This setup emphasizes functionality over aesthetics, focusing on leveraging the AI's capabilities rather than the user interface design.

## Features

- **User Authentication:** Secure login and signup pages for user management.
- **Document Upload:** Allows users to upload tender documents in PDF format.
- **Information Extraction:** Utilizes Python's Regex library to extract dates and ChatGPT API to analyze the text extracted from documents.
- **Results Display:** Shows the extracted data alongside the original PDF document for easy comparison and verification.

Below is a screenshot of the Login Page:

![Screenshot 2024-03-22 131602](https://github.com/biswajitdashh/Tender_Document_Date_and_Information_Extractor/assets/77931024/71800614-8685-4bc9-a6ca-f7d186b3cdfc)
