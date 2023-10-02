import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from langchain.text_splitter import RecursiveCharacterTextSplitter
from timer_decorator import timer

class PdfHandler:
    # def __init__(self):

    # Main logic for processing pdf
    @timer
    def pdf_to_chunks(self, pdf_url):
        data = self.get_pdf_from_url(pdf_url)
        text = extract_text(data)
        return self.chunk_text(text)


    # Fetches a PDF from a given URL and return it as a BytesIO object
    def get_pdf_from_url(self, url: str) -> BytesIO:
        # Fetch content from the URL
        response = requests.get(url)
        response.raise_for_status()

        # Get the content as a BytesIO object
        pdf_data = BytesIO(response.content)
        return pdf_data

    # Creates chunks from provided text
    def chunk_text(self, text, chunk_size=512, chunk_overlap=30, separators=None):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=separators,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        return text_splitter.split_text(text)

    # Extracts text from a given PDF file and writes the extracted text to an output file
    def extract_text_from_pdf(self, pdf_file, output_text_file: str):
        try:
            text = extract_text(pdf_file)
            # Write the extracted text to the output text file
            with open(output_text_file, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            
            print(f"Text extracted and saved to {output_text_file}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")