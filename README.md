# Streamlining Real Estate Operations with AI

In the hustle and bustle of real estate, every second counts, and so does every detail. Recently, a friend of mine, 
a dedicated real estate agent, shared how challenging it was to keep track of client calls, jot down details, and ensure nothing was overlooked. 
Inspired by this, I decided to create a solution that simplifies their workflow. Here’s what I built using Hugging Face Spaces:


## The Solution 
**Upload Recordings:** Users upload recorded client calls directly to the platform.  

**Transcription:** Leveraging Whisper, the voice recordings are transcribed with precision.  

**Data Extraction:** Powered by GPT-3.5-Turbo, it extracts key details from the transcripts.  

**Streamlined Output:** The extracted data is automatically populated into a Google Sheet in a clean, tabular format.  

![Untitled Diagram drawio](https://github.com/user-attachments/assets/feace50e-f687-421a-b076-034db538d0ce)

### Details Extracted

Client’s Name  
Property Type  
Location  
Size (in sq. ft)  
Number of Bedrooms  
Price  
Description  

**Google Sheet Preview**
![image](https://github.com/user-attachments/assets/1c33fb8f-dba9-455e-a475-190eca262c39)

The Realtor can be more effective in analysing and catering to his clients needs by using the information in the google sheets and do efficient follow-ups.

### Whats next?

**Analysis of Sales calls:**  
Leveraging LLMs to Analyse the calls and extract engagement levels, tract metrics, win/loss reasons and summarization of conversations.  
**Direct Call Integration:**  
Skip the upload step by integrating with call systems for real-time transcription and data capture.
