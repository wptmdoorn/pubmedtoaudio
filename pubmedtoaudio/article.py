from io import BytesIO
from typing import Optional
import requests
from bs4 import BeautifulSoup

SECTIONS_MAPS = {
    'Abstract': 'Abstract',
    'ABSTRACT': 'Abstract',
    'INTRODUCTION': 'Introduction',
    'MATERIALS AND METHODS': 'Methods',
    'Materials and methods': 'Methods',
    'METHODS': 'Methods',
    'RESULTS': 'Results',
    'CONCLUSIONS': 'Conclusions',
    'CONCLUSIONS AND FUTURE APPLICATIONS': 'Conclusions',
    'DISCUSSION': 'Discussion',
    'ACKNOWLEDGMENTS': 'Acknowledgement',
    'TABLES': 'Tables',
    'Tabnles': 'Tables',
    'DISCLOSURE': 'Disclosure',
    'CONFLICT OF INTEREST': 'Disclosure',
    'Acknowledgement': 'Acknowledgements'
}

INTRO_TEXT = {
    "full_text": """This audiobook was created through a software system called X.
                    In this audiobook we will present the full text of an article called
                    {title}. Enjoy listening!""",
    "abstract":  """This audiobook was created through a software system called X.
                    In this audiobook we will present the abstract of an article called
                    {title}. Enjoy listening!"""
}


def obtain_pubmed_pdf(pubmed_id: int) -> str:
    # define url
    url = f'https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/'

    # obtain html of PubMED page
    page_html = BeautifulSoup(requests.get(url).content, 
                              'html.parser')
    
    # find DOI tag (and content) for subsequent searching
    doi = page_html.find("meta", attrs={"name": "citation_doi"}).get('content', None)

    if doi:
        url = f'https://sci-hub.do/{doi}'
        
        # obtain html of SciHub page
        page_html = BeautifulSoup(requests.get(url).content, 
                                  'html.parser')
        
        try:
            idiv = page_html.find("div", {"id":"article"})
            pdf_url = idiv.find('iframe')['src'].split('#')[0]
            pdf_url = f"https:{pdf_url}"
            
            return pdf_url
            
        except Exception as e:
            return None


    return None

def merge_section_list(section_list, section_maps=SECTIONS_MAPS, section_start=''):
    """
    Merge a list of sections into a normalized list of sections,
    you can get the list of sections from parsed article JSON in ``parse_pdf.py`` e.g.
    
    >> section_list = [s['heading'] for s in article_json['sections']]
    >> section_list_merged = merge_section_list(section_list)
    
    Parameters
    ==========
    section_list: list, list of sections
    Output
    ======
    section_list_merged: list,  sections
    """
    sect_map = section_start # text for starting section e.g. ``Introduction``
    section_list_merged = []
    for section in section_list:
        if any([(s.lower() in section.lower()) for s in section_maps.keys()]):
            sect = [s for s in section_maps.keys() if s.lower() in section.lower()][0]
            sect_map = section_maps.get(sect, '') # 
            section_list_merged.append(sect_map)
        else:
            section_list_merged.append(sect_map)
    return section_list_merged

def structure_dict(pdf_dict: dict, audio_target: str) -> dict:
    mainstring = """"""
    mainstring += INTRO_TEXT[audio_target].format(title=pdf_dict['title'])
    
    if audio_target == 'full_text':
        _mainsections = merge_section_list([s['heading'] for s in pdf_dict['sections']])
        structured_dict = {k : [] for k in list(dict.fromkeys(_mainsections))}
        
        for m, s in zip(_mainsections, pdf_dict['sections']):
            structured_dict[m].append(s)
        
        for k, v in structured_dict.items():
            mainstring += k
            mainstring += "\n"
            
            for subtext in v:
                mainstring += subtext['heading']
                mainstring += "\n"
                mainstring += subtext['text']
                mainstring += "\n"
                
            mainstring += "\n\n"    

    elif audio_target == 'abstract':
        mainstring += pdf_dict['abstract']
        
    return mainstring

        