"""
A module for obtaining repo readme and language data from the github API.
Before using this module, read through it, and follow the instructions marked
TODO.
After doing so, run it like this:
    python acquire.py
To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

REPOS = [
    "gocodeup/codeup-setup-script",
    "gocodeup/movies-application",
    "torvalds/linux",
    "abuanwar072/Flutter-Responsive-Admin-Panel-or-Dashboard",
    "pallupz/covid-vaccine-booking",
    "goharbor/harbor",
    "public-apis/public-apis",
    "jwasham/coding-interview-university",
    "DIGITALCRIMINAL/OnlyFans",
    "facebookincubator/cinder",
    "vinta/awesome-python",
    "jlevy/the-art-of-command-line",
    "dogecoin/dogecoin",
    "phamdinhkhanh/vnquant",
    "audacity/audacity",
    "Uniswap/uniswap-v3-periphery",
    "swar/Swar-Chia-Plot-Manager",
    "flutter/flutter",
    "streamich/react-use",
    "dynamicwebpaige/thinking-in-data",
    "forem/forem",
    "Azure/counterfit",
    "Uniswap/uniswap-v3-core",
    "ionic-team/ionic-framework",
    "thedevdojo/wave",
    "devsuperior/sds3",
    "angular/angular-cli",
    "benawad/dogehouse",
    "jtleek/datasharing",
    "rdpeng/ProgrammingAssignment2",
    "octocat/Spoon-Knife",
    "tensorflow/tensorflow",
    "SmartThingsCommunity/SmartThingsPublic",
    "twbs/bootstrap",
    "github/gitignore",
    "rdpeng/ExData_Plotting1",
    "Pierian-Data/Complete-Python-3-Bootcamp",
    "nightscout/cgm-remote-monitor",
    "jwasham/coding-interview-university",
    "opencv/opencv",
    "tensorflow/models",
    "EbookFoundation/free-programming-books",
    "eugenp/tutorials",
    "CyC2018/CS-Notes",
    "jackfrued/Python-100-Days",
    "rdpeng/RepData_PeerAssessment1",
    "firstcontributions/first-contributions",
    "Snailclimb/JavaGuide",
    "facebook/react",
    "spring-projects/spring-boot",
    "jlord/patchwork",
    "barryclark/jekyll-now",
    "DataScienceSpecialization/courses",
    "spring-projects/spring-framework",
    "TheAlgorithms/Python",
    "vuejs/vue",
    "bitcoin/bitcoin",
    "kubernetes/kubernetes",
    "ant-design/ant-design",
    "mrdoob/three.js",
    "getify/You-Dont-Know-JS",
    "freeCodeCamp/freeCodeCamp",
    "DefinitelyTyped/DefinitelyTyped",
    "PanJiaChen/vue-element-admin",
    "donnemartin/system-design-primer",
    "apache/dubbo",
    "justjavac/free-programming-books-zh_CN",
    "udacity/frontend-nanodegree-resume",
    "kamranahmedse/developer-roadmap",
    "d3/d3",
    "ohmyzsh/ohmyzsh",
    "mui-org/material-ui",
    "facebook/create-react-app",
    "dotnet/AspNetCore.Docs",
    "git/git",
    "scikit-learn/scikit-learn",
    "LarryMad/recipes",
    "996icu/996.ICU",
    "macrozheng/mall",
    "airbnb/javascript",
    "iluwatar/java-design-patterns",
    "laravel/laravel",
    "facebook/react-native",
    "sindresorhus/awesome",
    "ansible/ansible",
    "slatedocs/slate",
    "nodejs/node",
    "jquery/jquery",
    "elastic/elasticsearch",
    "shadowsocks/shadowsocks"
    "rails/rails",
    "qmk/qmk_firmware",
    "redis/redis",
    "vinta/awesome-python",
    "BVLC/caffe",
    "microsoft/vscode",
    "keras-team/keras",
    "python/cpython",
    "wesbos/JavaScript30",
    "trekhleb/javascript-algorithms",
    "google/it-cert-automation-practice",
    "moby/moby",
    "labuladong/fucking-algorithm",
    "apache/echarts",
    "flutter/flutter",
    "CSSEGISandData/COVID-19",
    "pjreddie/darknet",
    "helm/charts",
    "xingshaocheng/architect-awesome",
    "github/docs",
    "ColorlibHQ/AdminLTE",
    "wakaleo/game-of-life",
    "danielmiessler/SecLists",
    "aymericdamien/TensorFlow-Examples",
    "public-apis/public-apis",
    "doocs/advanced-java",
    "jenkins-docs/simple-java-maven-app",
    "reduxjs/redux",
    "MicrosoftDocs/mslearn-tailspin-spacegame-web",
    "scm-ninja/starter-web",
    "mmistakes/minimal-mistakes",
    "pallets/flask",
    "RedHatTraining/DO180-apps",
    "scutan90/DeepLearning-500-questions",
    "tastejs/todomvc",
    "CoreyMSchafer/code_snippets",
    "academicpages/academicpages.github.io",
    "selfteaching/the-craft-of-selfteaching",
    "ionic-team/ionic-framework",
    "mdn/learning-area",
    "netty/netty", 
    "MicrosoftDocs/azure-docs",
    "jakevdp/PythonDataScienceHandbook",

























     





    

















]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        if "language" not in repo_info:
            raise Exception(
                "'language' key not round in response\n{}".format(json.dumps(repo_info))
            )
        return repo_info["language"]
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = ""
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)