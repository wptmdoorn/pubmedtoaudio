from pubmedtoaudio.pubmedtoaudio import get_audiobook

PUBMED_ID = 31724117

a = get_audiobook(PUBMED_ID,
                  audio_type='full_text')

print(a)
