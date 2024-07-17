import os
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from google.cloud import translate_v3 as translate

def extract_text_from_pdf(pdf_path, project_id, location, processor_id):

    credentials = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    client = documentai.DocumentProcessorServiceClient(credentials=credentials)
    name = f'projects/{project_id}/locations/{location}/processors/{processor_id}'


    with open(pdf_path, 'rb') as file:
        pdf_content = file.read()


    raw_document = documentai.RawDocument(content=pdf_content, mime_type='application/pdf')
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)


    result = client.process_document(request=request)


    document = result.document
    text = document.text

    return text


def translate_text(text, project_id, location, target_language='ro'):

    credentials = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    client = translate.TranslationServiceClient(credentials=credentials)

    parent = f'projects/{project_id}/locations/{location}'


    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type='text/plain',  # mime types: text/plain, text/html
        target_language_code=target_language
    )


    translated_text = response.translations[0].translated_text
    return translated_text


def main(pdf_path, dest_language='en'):
    project_id = 'proiectpdftransator'  # Actualizați cu ID-ul proiectului dvs.
    location = 'us'  # Actualizați cu locația procesorului dvs., de exemplu, 'us'
    processor_id = 'fc01c3ab7d18577e'  # Actualizați cu ID-ul procesorului dvs.
    location2='global'

    extracted_text = extract_text_from_pdf(pdf_path, project_id, location, processor_id)
    print(f"Extracted Text:\n{extracted_text}\n")


    translated_text = translate_text(extracted_text, project_id, location2)
    print(f"Translated Text:\n{translated_text}\n")



if __name__ == "__main__":
    pdf_path = "index.pdf"
    dest_language = 'ro'
    main(pdf_path, dest_language)

