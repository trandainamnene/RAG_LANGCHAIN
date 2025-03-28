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
    {
        "title": "Bai giang benh hoc ngoai khoa (tap 1)",
        "url": "https://drive.google.com/file/d/1MVoLIg8kiTbkVKw-4qLGLAufC4Vm4bZK/view"
    },
    {
        "title": "Bai giang benh hoc ngoai khoa (tap 2)",
        "url": "https://drive.google.com/file/d/1HPlGHIZShtWH-PHIQajF9O1DKDPnbYUe/view"
    },
    {
        "title": "Noi khoa co so tap 1",
        "url": "https://drive.google.com/file/d/1JPoFG7n4gXfxULaYaeHS5CCGQpGgpNhN/view"
    },
    {
        "title": "Noi khoa co so tap 2",
        "url": "https://drive.google.com/file/d/1nkTYQ-CzxJ8ppx67GJRvaMppZzskRlPh/view"
    },
    {
        "title": "Trieu chung ngoai khoa",
        "url": "https://drive.google.com/file/d/1R_OpzX0890ToakB90KsW9gdpoLC7lv4G/view"
    },
    {
        "title": "Trieu chung ngoai khoa",
        "url": "https://drive.google.com/file/d/1R_OpzX0890ToakB90KsW9gdpoLC7lv4G/view"
    },
    {
        "title": "Kinh nghiem lam sang",
        "url": "https://drive.google.com/file/d/1RlXDuODTeyhOsY082PF5cwmNVSpNTd3T/view"
    },
    {
        "title": "Co che trieu chung hoc",
        "url": "https://drive.google.com/file/d/1I2Hxb6r3xOZmKu6SUyXYsTHM5vJmHCpb/view"
    },
    {
        "title": "Nguyen li noi khoa tap 3",
        "url": "https://drive.google.com/file/d/1o3IdydI4FTaSQC4QvY4XFY1C4rGXbNGg/view?fbclid=IwY2xjawJN6LhleHRuA2FlbQIxMAABHWKBEtdUlSBC_Qvb7Q7ZSEDPA_Ud-lwStzmN39r1ka2WtTvIoT8a5uM3gQ_aem_vabUyQcUFSVVXNzLAtQN-Q"
    },
    {
        "title": "Nguyen li noi khoa tap 2",
        "url": "https://drive.google.com/file/d/1NpR2iVANz23w5wNUGmt3J1sdlt2Nl2vM/view?fbclid=IwY2xjawJN6JtleHRuA2FlbQIxMAABHWKBEtdUlSBC_Qvb7Q7ZSEDPA_Ud-lwStzmN39r1ka2WtTvIoT8a5uM3gQ_aem_vabUyQcUFSVVXNzLAtQN-Q"
    },
    {
        "title": "Nguyen li noi khoa tap 2",
        "url": "https://drive.google.com/file/d/1NpR2iVANz23w5wNUGmt3J1sdlt2Nl2vM/view?fbclid=IwY2xjawJN6JtleHRuA2FlbQIxMAABHWKBEtdUlSBC_Qvb7Q7ZSEDPA_Ud-lwStzmN39r1ka2WtTvIoT8a5uM3gQ_aem_vabUyQcUFSVVXNzLAtQN-Q"
    },
    {
        "title": "Dieu tri hoc noi khoa tap 1",
        "url": "https://drive.google.com/file/d/1Z6jdPAw86Z9ZIoB9XPnhMhtPCPkcli_H/view"
    },
    {
        "title": "Dieu tri hoc noi khoa tap 2",
        "url": "https://drive.google.com/file/d/1g-lbiGJTykmscr6awu19vlUpthy2WYPP/view"
    },
    {
        "title": "So tay noi khoa",
        "url": "https://drive.google.com/file/d/1snO3ga_IK5uM_AYS3VwiohbgmduJmTzO/view"
    },
    {
        "title": "Cam nang dieu tri noi khoa Washinton",
        "url": "https://drive.google.com/file/d/19ZLcccdAplV_2HjNBR5NAO9nQt0FbFdU/view"
    },
    {
        "title": "Phac do dieu tri ngoại nhi tap 1",
        "url": "https://drive.google.com/file/d/1IeZnYke8SzxKGyrZXbZxVjCZzQBGqsLp/view"
    },
    {
        "title": "Phac do dieu tri ngoai nhi tap 2",
        "url": "https://drive.google.com/file/d/19ZLcccdAplV_2HjNBR5NAO9nQt0FbFdU/view"
    },
    {
        "title": "So tay dieu tri nhi khoa",
        "url": "https://drive.google.com/file/d/1wVQtCYSfsD9m0GFsEANk_zxLQafig4wX/view"
    },
    {
        "title": "Phac do ngoai tru nhi khoa",
        "url": "https://drive.google.com/file/d/1P7klX5F5PycbGX_-bQENKJCjNL0OFkdy/view"
    },



]


def clean_title(title):
    return title.replace(":", "_").replace("-", '').replace(' ', "_")


def is_exist(file_link):
    return os.path.exists(f"./{file_link['title']}.pdf")


for file_link in filelinks:
    if not is_exist(file_link):
        wget.download(f"{file_link['url']}",
                      out=f"./{clean_title(file_link['title'])}.pdf")
