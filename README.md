# Tender-Document-Analyzer

Made a Document Analyzer using Chatgpt API by Open AI for Tender based Documents. Used Django for building the framework on which this web application is based on. The Web App consists of 4 pages- Login,Signup, Upload and Results. Haven't focused much on the UI as this is more about the functionality of the code and harnessing the power of the AI. First I converted the whole PDF into Text followed which I extracted the dates using Python's Library Regex. Passed on the following data as parameters onto the API after a lot of hit and trials with token sizes, chunk sizes and what not upon which I finally settled on the code that gave me fascinating results after going gung ho on the chatgpt documentation. Gave the output side by side along with the original PDF for easy comparision.

## Features

- **User Authentication:** Secure login and signup pages for user management.
- **Document Upload:** Allows users to upload tender documents in PDF format.
- **Information Extraction:** Utilizes Python's Regex library to extract dates and ChatGPT API to analyze the text extracted from documents.
- **Results Display:** Shows the extracted data alongside the original PDF document for easy comparison and verification.

Below is a screenshot of the Login Page:

![Screenshot 2024-03-22 131602](https://github.com/biswajitdashh/Tender_Document_Date_and_Information_Extractor/assets/77931024/71800614-8685-4bc9-a6ca-f7d186b3cdfc)
