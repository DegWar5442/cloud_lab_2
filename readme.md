# **📝 Hugging Face BART Text Summarizer**

This project provides two different interfaces—a command-line application and a standalone web application—to perform abstractive text summarization using the **Hugging Face Inference API** and the powerful **facebook/bart-large-cnn** model.

Both interfaces require a Hugging Face API key to function.

## **✨ Project Interfaces**

This repository contains two primary ways to access the summarization functionality:

### **1\. Command-Line Interface (CLI)**

* **File:** summarizer.py  
* **Description:** This is an interactive Python script that runs directly in your terminal. It allows for quick, iterative summarization tasks.  
* **Key Feature Highlight:** This console version provides detailed **compression statistics**, showing the percentage reduction in characters between the original text and the generated summary.

### **2\. Web Interface (HTML/JavaScript)**

* **File:** index.html  
* **Description:** A single, self-contained HTML file featuring modern styling. This provides a user-friendly graphical interface (GUI) to paste text and receive the summary directly in the browser.  
* **Key Feature Highlight:** Offers a simple, click-to-summarize experience that is easy to share and use without installing Python dependencies.

## **🚀 Getting Started**

### **Prerequisites**

You must have a **Hugging Face API Token** (Key). You can obtain one for free by signing up on Hugging Face and navigating to your [Settings \> Access Tokens](https://huggingface.co/settings/tokens).

### **A. Console Interface Setup (bart\_python\_with\_stats.py)**

1. **Requirements:** You need Python 3.6+ and the requests library.  
   pip install requests

2. **Execution:** Run the script and follow the prompts.  
   python summarizer.py

### **B. Web Interface Setup (bart\_web\_interface.html)**

1. **Requirements:** No special requirements. The file is a standalone application that uses pure HTML, CSS, and JavaScript.  
2. **Execution:** Simply open the index.html file in any modern web browser.  
3. **Usage:** Paste your API key, enter your text, and click the "Summarize" button.

## **📊 Core Feature: Compression Rate**

The summarizer.py (CLI) includes a utility function to calculate and display the compression statistics after a successful summary is generated.

This feature shows:

* **Original Character Count**  
* **Summary Character Count**  
* **Compression Rate (**%**)**: The percentage by which the summary is shorter than the original text.

This is highly useful for benchmarking the efficiency of the BART model on different lengths and types of input.