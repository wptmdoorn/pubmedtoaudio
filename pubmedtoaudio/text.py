import re, textwrap

# remove square brackets (references)
# remove confidence intervals and stuff?

def _process_parenth(matcho) -> str:
    s = matcho.group(0)[1:-1].replace(" ","")
    numbers = sum(map(str.isdigit, s))
    letters = sum(map(str.isalpha, s))
    spaces = sum(map(str.isspace, s))
    marks = sum(map(lambda x: x in ".=>=<,/\%|±~≥≤", s))
    others  = len(s) - numbers - letters - spaces - marks
    
    pct_let = (letters / len(s))
    
    print(f'Matched: {s} - Perc. letters: {pct_let}')
    
    if pct_let <= 0.5:
        return ''

    return matcho.group(0)

def process_text(text: str) -> str:
    patterns = [(r'\[.*?\]', ''), # remove square brackets
                (r'\(.*?\)', _process_parenth)
               ]
    
    for p in patterns:
        text = re.sub(p[0], p[1], text)
        
    return text
        
def wrap_text(text: str) -> list:
    wrapper = textwrap.TextWrapper(width = 80)
    wrapped_list = [wrapper.wrap(i) for i in text.split('\n') if i != '']
    
    return list(itertools.chain.from_iterable(wrapped_list))