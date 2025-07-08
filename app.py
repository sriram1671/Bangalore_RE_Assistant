import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import openai
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import gradio as gr
import re
import os

# Set up Whisper model
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v2")
openai.api_key = os.environ["OPENAI_API_KEY"]


def transcribe_audio(audio_files):
    """Transcribes multiple audio files using Whisper."""
    transcripts = []
    for file in audio_files:
        result = transcriber(file)
        transcripts.append(result['text'])
    return transcripts

def extract_real_estate_details(transcripts):
    try:
        
        responses = []
        for transcript in transcripts:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a real estate expert in Bangalore. Extract and format property details as: Client Name, Property type, Location, Size (in sq ft), Number of Bedrooms, Price, Description. Separate each field with a comma."},
                    {"role": "user", "content": f"Extract real estate details from this: {transcript}"}
                ]
            )
            responses.append(response.choices[0].message.content)
        return responses
    except openai.RateLimitError:
        return "Error: API quota exceeded. Please check your OpenAI API billing settings."
    except Exception as e:
        return f"Error processing request: {str(e)}"

#Formating Data
def format_data_for_google_sheets(data):
    print(f"Input data type: {type(data)}")

    if isinstance(data, list):  
       data = "\n".join(data)
    elif not isinstance(data, str):  
       raise TypeError(f"Input `data` must be a string or a list of strings. Got {type(data)} instead.")
       
      
    print(f"Data after ensuring string type:\n{data}")
    entries = re.split(r"(?:\n\s*\n|,)", data.strip())
    entries = [entry.strip() for entry in entries if entry.strip()]
   
    headers = ["Client Name", "Property Type", "Location", "Size (in sq ft)", "Number of Bedrooms", "Price", "Description"]
    formatted_data = []
    
    row_dict = {key: "" for key in headers}

   
    for entry in entries:
        print(f"Processing entry:\n{entry}")
   
        values = re.findall(
            r"(Client Name|Property type|Location|Size|Number of Bedrooms|Price|Description):\s*(.*?)(?:,|$)",
            entry,
            flags=re.DOTALL,
        )
        print(f"Extracted key-value pairs:\n{values}")

        for key, value in values:
            row_dict[key.strip()] = value.strip().replace(",", "")  # Strip and clean values
    
    # Append the row_dict as a list to formatted_data
    formatted_data.append([row_dict[header] for header in headers])
    print("Formatted Data for Sheets:")
    for row in formatted_data:
        print(row)
    
    return formatted_data


def connect_to_sheets(json_key_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    return gspread.authorize(credentials)


def create_google_sheet(client, title):
    sheet = client.create(title)
    sheet.share('abc@gmail.com', perm_type='user', role='writer')  # Replace with your email
    return sheet


def write_data_to_sheet(sheet, worksheet_title, data):
    worksheet = sheet.add_worksheet(title=worksheet_title, rows="100", cols="20")
    worksheet.update('A1', data)  
    
def append_data_to_sheet(worksheet, data):
    worksheet.append_rows(data, value_input_option="USER_ENTERED")



def create_data(data):
    json_key_file = "path/to/your-service-account-key.json"
    client = connect_to_sheets(json_key_file)
    spreadsheet = client.open("Bangalore Real Estate")
    worksheet = spreadsheet.worksheet("Sale Properties")
    append_data_to_sheet(worksheet, data)
    # Create a new sheet
    #sheet = create_google_sheet(client, "My New Sheet")
    #print(f"Google Sheet created: {sheet.url}")
    #write_data_to_sheet(sheet, "Sheet23", data)





def process_audio(audio_files):
    """Main processing function for audio transcription and data extraction.""" 
    transcripts = transcribe_audio(audio_files)
    extracted_data = extract_real_estate_details(transcripts)
    
    data = []
    for r in extracted_data:
        try:
            details = r.split(",")
            

            data.append(details)
        except Exception:
            data.append(["Error Parsing"] *7 )
    d_F = format_data_for_google_sheets(extracted_data)
    create_data(d_F)
    return data

def gradio_interface(audio_files):
    df = process_audio(audio_files)
    print(df)
    return df





interface = gr.Interface(
    fn=process_audio,
    inputs=gr.File(file_types=["audio"], label="Upload Audio", file_count="multiple"),
    outputs=gr.Textbox(label="Extracted Real Estate Details"),
    title="Audio Transcription Tool",
    description="Upload one or more audio files to get their transcriptions.")

if __name__ == "__main__":
    interface.launch(share=True)
