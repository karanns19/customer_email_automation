# Customer Email Feedback Analysis Automation

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)

## Introduction

With the increasing demand for automation in business processes, leveraging tools like Datamatics TruBot and TruCap+ can significantly reduce manual tasks, improve accuracy, and increase efficiency. This project aims to automate the processing of customer feedback emails, streamlining customer service operations. The automation solution fetches customer feedback from an email inbox, analyzes the content, classifies it as positive, negative, or neutral, and extracts key details to insert into a Google Form.

## Features

- Connects to a specified email inbox (e.g., Gmail) to fetch customer feedback emails.
- Analyzes email content to classify it as positive, negative, or neutral.
- Extracts key details, including:
  - Customer Name
  - Order ID (if applicable)
  - Feedback Category (e.g., product, service, delivery)
  - Sentiment Score
- Inserts extracted details into a Google Form.
- Sends a summary email notification to the customer service team with sentiment scores and key details.

## Technologies Used

- Python
- Datamatics TruBot
- Datamatics TruCap+
- Google APIs (Gmail, Google Forms)
- Natural Language Processing (NLP) libraries (e.g., NLTK, TextBlob)

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Access to Google APIs (Gmail and Google Forms).
- Datamatics TruBot and TruCap+ accounts set up.

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/karanns19/customer_email_automation.git
   cd customer_email_automation
