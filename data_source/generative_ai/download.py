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
    # {
    #     "title": "Noi khoa co so tap 1",
    #     "url": "https://drive.usercontent.google.com/uc?id=1JPoFG7n4gXfxULaYaeHS5CCGQpGgpNhN&export=download"
    # },
    # {
    #     "title": "Noi khoa co so tap 2",
    #     "url": "https://drive.usercontent.google.com/uc?id=1nkTYQ-CzxJ8ppx67GJRvaMppZzskRlPh&export=download"
    # },
    # {
    #     "title": "Trieu chung ngoai khoa",
    #     "url": "https://drive.usercontent.google.com/uc?id=1R_OpzX0890ToakB90KsW9gdpoLC7lv4G&export=download"
    # },
    # {
    #     "title": "Trieu chung ngoai khoa",
    #     "url": "https://drive.usercontent.google.com/uc?id=1R_OpzX0890ToakB90KsW9gdpoLC7lv4G&export=download"
    # },
    # {
    #     "title": "Kinh nghiem lam sang",
    #     "url": "https://drive.usercontent.google.com/uc?id=1RlXDuODTeyhOsY082PF5cwmNVSpNTd3T&export=download"
    # },
    # {
    #     "title": "Co che trieu chung hoc",
    #     "url": "https://drive.usercontent.google.com/uc?id=1I2Hxb6r3xOZmKu6SUyXYsTHM5vJmHCpb&export=download"
    # },
    # {
    #     "title": "Nguyen li noi khoa tap 3",
    #     "url": "https://drive.usercontent.google.com/uc?id=1o3IdydI4FTaSQC4QvY4XFY1C4rGXbNGg&export=download"
    # },
    # {
    #     "title": "Nguyen li noi khoa tap 2",
    #     "url": "https://drive.usercontent.google.com/uc?id=1NpR2iVANz23w5wNUGmt3J1sdlt2Nl2vM&export=download"
    # },
    # {
    #     "title": "Nguyen li noi khoa tap 2",
    #     "url": "https://drive.usercontent.google.com/uc?id=1NpR2iVANz23w5wNUGmt3J1sdlt2Nl2vM&export=download"
    # },
    # {
    #     "title": "Dieu tri hoc noi khoa tap 1",
    #     "url": "https://drive.usercontent.google.com/uc?id=1Z6jdPAw86Z9ZIoB9XPnhMhtPCPkcli_H&export=download"
    # },
    # {
    #     "title": "Dieu tri hoc noi khoa tap 2",
    #     "url": "https://drive.usercontent.google.com/uc?id=1g-lbiGJTykmscr6awu19vlUpthy2WYPP&export=download"
    # },
    # {
    #     "title": "So tay noi khoa",
    #     "url": "https://drive.google.com/file/d/1snO3ga_IK5uM_AYS3VwiohbgmduJmTzO/view"
    # },
    # {
    #     "title": "Cam nang dieu tri noi khoa Washinton",
    #     "url": "https://drive.usercontent.google.com/uc?id=1snO3ga_IK5uM_AYS3VwiohbgmduJmTzO&export=download"
    # },
    # {
    #     "title": "Phac do dieu tri ngoại nhi tap 1",
    #     "url": "https://drive.usercontent.google.com/uc?id=1IeZnYke8SzxKGyrZXbZxVjCZzQBGqsLp&export=download"
    # },
    # {
    #     "title": "Phac do dieu tri ngoai nhi tap 2",
    #     "url": "https://drive.usercontent.google.com/uc?id=19ZLcccdAplV_2HjNBR5NAO9nQt0FbFdU&export=download"
    # },
    # {
    #     "title": "So tay dieu tri nhi khoa",
    #     "url": "https://drive.usercontent.google.com/uc?id=1wVQtCYSfsD9m0GFsEANk_zxLQafig4wX&export=download"
    # },
    # {
    #     "title": "Phac do ngoai tru nhi khoa",
    #     "url": "hhttps://drive.usercontent.google.com/uc?id=1P7klX5F5PycbGX_-bQENKJCjNL0OFkdy&export=download"
    # },



]


def clean_title(title):
    return title.replace(":", "_").replace("-", '').replace(' ', "_")


def is_exist(file_link):
    return os.path.exists(f"./{file_link['title']}.pdf")


for file_link in filelinks:
    if not is_exist(file_link):
        wget.download(f"{file_link['url']}",
                      out=f"./{clean_title(file_link['title'])}.pdf")
