import os.path
import wget
filelinks = [
    {
        "title": "From Faces to Voices",
        "url": "https://arxiv.org/pdf/2503.16956"
    },
    {
        "title": "Learning disentangled representations for instrument-based music similarity",
        "url": "https://arxiv.org/pdf/2503.17281"
    },
    {
        "title": "Auditory Knowledge Generation can be an Effective Assistant for Language Models",
        "url": "https://arxiv.org/pdf/2503.16853"
    },
    {
        "title": "A Chinese Conversation Dataset with Rich Annotations for Super-Aged Seniors",
        "url": "https://arxiv.org/pdf/2503.16578"
    },
    {
        "title": "A Speech Production Model for Radar: Connecting Speech Acoustics with Radar-Measured Vibrations",
        "url": "https://arxiv.org/pdf/2503.15627"
    },
    {
        "title": "UniSync: A Unified Framework for Audio-Visual Synchronization",
        "url": "https://arxiv.org/pdf/2503.16357"
    },
    {
        "title": "Learning disentangled representations for instrument-based music similarity",
        "url": "https://arxiv.org/pdf/2503.17281"
    },
    {
        "title": "Development of an Inclusive Educational Platform Using Open Technologies and Machine Learning",
        "url": "https://arxiv.org/pdf/2503.15501"
    },
    {
        "title": "Collaborative Artistic Creation through Human-AI Interactions in Musical Creativity",
        "url": "https://arxiv.org/pdf/2503.15498"
    },
    {
        "title": "Towards a Speech-Oriented LLM That Hears Acoustic Context",
        "url": "https://arxiv.org/pdf/2503.15338"
    },
]

def clean_title(title) :
    return title.replace(":" , "_").replace("-" , '').replace(' ' , "_")

def is_exist(file_link) :
    return os.path.exists(f"./{file_link['title']}.pdf")

for file_link in filelinks :
    if not is_exist(file_link) :
        wget.download(f"{file_link['url']}" , out=f"./{clean_title(file_link['title'])}.pdf")