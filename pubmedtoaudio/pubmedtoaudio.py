from .article import obtain_pubmed_pdf, structure_dict
from .parser import parse_pdf_to_dict
from .audio import pdf_to_audio
from .text import process_text, wrap_text

import os, json, datetime, itertools, textwrap

def get_audiobook(pubmed_id: int,
                  out_file: str = None, 
                  audio_type: str = 'full_text') -> str:
    
    # define out_file if this is not defined as argument
    if not(out_file):
        now = datetime.datetime.now()
        now_str = now.strftime("%d%m%Y_%H%M")
        out_file = f'{now_str}_{audio_type}_{pubmed_id}'

    # obtain the PDF url from the PubMED ID through sci-hub
    pdf_url = obtain_pubmed_pdf(pubmed_id)
    
    # obtain processed PDF as python dictionary
    processed_pdf = parse_pdf_to_dict(pdf_url)
    
    # structure dictionary and subsequently process the text
    parsed_text = structure_dict(processed_pdf, audio_target=audio_type)
    parsed_text = process_text(parsed_text)
    
    # wrap text
    parsed_text_list = wrap_text(parsed_text)
    
    with open(os.path.join('output', f'{out_file}.text'),
            'w',
            encoding='utf-8') as f:
        for item in parsed_text_list:
            f.write(f'{item}\n')

    #audio_file = pdf_to_audio(mylist, 
    #                        out_name=os.path.join('output', f'{out_file}.mp3'))
    
    return f'{out_file}.mp3'