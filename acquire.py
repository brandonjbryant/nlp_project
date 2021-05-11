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
     'torvalds/linux',
   'ansible/ansible',
    'TensorSpeech/TensorFlowTTS',
    'plurals/pluralize',
    'vczh/tinymoe',
 'RHVoice/RHVoice',
 'wapmorgan/Morphos',
 'ChenYCL/chrome-extension-udemy-translate',
 'botupdate/botupdate',
 'VinAIResearch/BERTweet',
 'opencog/link-grammar',
 'makerbase-mks/MKS-TFT',
 'google-research-datasets/wiki-reading',
 'davidsbatista/NER-datasets',
 'words/moby',
 'quadrismegistus/prosodic',
 'libindic/indic-trans',
 'wooorm/parse-english',
 'pannous/english-script',
 'frcchang/zpar',
 'hechoendrupal/drupal-console-en',
 'speechio/BigCiDian',
 'godlytalias/Bible-Database',
 'IlyaGusev/rnnmorph',
 'asweigart/simple-turtle-tutorial-for-python',
 'zacanger/profane-words',
 'kavgan/phrase-at-scale',
 'deep-diver/EN-FR-MLT-tensorflow',
 'ElvisQin/ProjectEnglish',
 'jmsv/ety-python',
 'wapmorgan/TimeParser',
 'vim-scripts/LanguageTool',
 'csebuetnlp/banglanmt',
 'SadaqaWorks/Word-By-Word-Quran-Android',
 'PDKT-Team/ctf',
 'mozilla/language-mapping-list',
 'surfinzap/typopo',
 'adlawson/nodejs-langs',
 'Kyubyong/neural_tokenizer',
 'bikenik/Anki_Templates',
 'scriptin/jmdict-simplified',
 'rust-lang-cn/english-chinese-glossary-of-rust',
 'msg-systems/coreferee',
 'davidmfoley/storevil',
 'chadkeck/Natural-Language-Clock',
 'gtarawneh/languagetool-sublime',
 'vilic/a-plus-dictionary',
 'stefantruehl/research-proposal-template',
 'harsh19/Shakespearizing-Modern-English',
 'vanderlee/php-sentence',
 'adetuyiTolu/Language_Time',
 'panda-lang/light',
 'thomhastings/mimikatz-en',
 'dchest/stemmer',
 'google-research-datasets/RxR',
 'chrisjbryant/lmgec-lite',
 'amrsaeedhosny/countries',
 'thomascgray/NooNooFluentRegex',
 'cijic/phpmorphy',
 'notAI-tech/DeepTranslit',
 'AnotherTest/-English',
 'narze/toSkoy',
 'gertd/go-pluralize',
 'binarybottle/engram',
 'pcjbird/fbCharm',
 'echen/unsupervised-language-identification',
 'libindic/soundex',
 'jpaya17/englishisfun',
 'purvanshi/isolvemath',
 'logue/MabiPack',
 'javadev/moneytostr-russian',
 'ddmcdonald/sparser',
 'haliaeetus/iso-639',
 'kariminf/jslingua',
 'mikahama/uralicNLP',
 'wietsedv/gpt2-recycle',
 'rubyworks/english',
 'jan-Lope/Toki_Pona_lessons_English',
 'noops-challenge/wordbot',
 'elliotchance/bento',
 'IINemo/isanlp',
 'matbahasa/TALPCo',
 'rothos/lexitron',
 'PanderMusubi/locale-en-nl',
 'words/ap-style-title-case',
 'RienNeVaPlus/human-id',
 'sharad461/nepali-translator',
 'carlosbrando/custom_resource_name',
 'dlang-tour/english',
 'danakt/spell-checker.js',
 'words/wiktionary',
 'ARIA-VALUSPA/AVP',
 'words/similar-english-words',
 'IBM/MAX-News-Text-Generator',
 'wapmorgan/yii2-inflection',
 'RightCapitalHQ/chinese-style-guide',
 'SpongeBob-222/gomoku',
 'onlyphantom/elang',
 'cofface/superrs-kitchen',
 'rameshjes/Semantic-Textual-Similarity',
 'tomasz-oponowicz/spoken_language_dataset',
 'SuzanaK/english_synonyms_antonyms_list',
 'shenhuanet/Ocr-android',
 'Vedenin/code-for-learning-languages',
 'musicamecclesiae/English-Hymns',
 'anuragk240/Speech-to-Sign-Language-Translator',
 'SuzanaK/english_synonyms_antonyms_list',
 'shenhuanet/Ocr-android',
 'Vedenin/code-for-learning-languages',
 'musicamecclesiae/English-Hymns',
 'anuragk240/Speech-to-Sign-Language-Translator',
 'derintelligence/en-az-parallel-corpus',
 'chaira19/Hindi-DateTime-Parser',
 'dhvani-tts/dhvani-tts',
 'UniversalDependencies/UD_English-ESL',
 'dolanskurd/kurdish',
 'crossbowerbt/prolog-talk',
 'shvmshukla/Machine-Translation-Hindi-to-english-',
 'IBM/MAX-Review-Text-Generator',
 'jonschlinkert/diacritics-map',
 'AndriesSHP/Gellish',
 'HoldOffHunger/convert-british-to-american-spellings',
 'vipul-khatana/Hinglish-Sentiment-Analysis',
 'hjian42/Natural-Language-Processing-Nanodegree',
 'oligoglot/theedhum-nandrum',
 'mageplaza/magento-2-italian-language-pack',
 'dan1wang/jsonbook-builder',
 'brentsnook/numerouno',
 'aishek/js-countdown',
 'zoomio/tagify',
 'Kaosam/HTBWriteups',
 'openlanguageprofiles/olp-en-cefrj',
 'ivanovsaleksejs/NumToText',
 'preranas20/Emotion-Detection-in-Speech',
 'freeduke33/rerap2',
 'germanattanasio/professor-languo',
 'jonschlinkert/alphabet',
 'citiususc/SimpleNLG-ES',
 'fizyk/sfForkedDoctrineApplyPlugin',
 'hci-lab/LearningMetersPoems',
 'willettk/common_language',
 'opener-project/coreference-base',
 'khzaw/athena',
 'cogenda/cgdrep',
 'jonschlinkert/common-words',
 'microsoft/LID-tool',
 'srijan14/Document-Machine-Translation',
 'tonianelope/Multilingual-BERT',
 'RimWorld-zh/RimWorld-English',
 'TotalVerb/EnglishText.jl',
 'p1u3o/MiWifi-Language-Mod',
 'humenda/isolang-rs',
 'rljacobson/JLCPCBBasicLibrary',
 'edigu/almanca',
 'mauryquijada/word-complexity-predictor',
 'brackendev/ELIZA-Smalltalk',
 'prashishh/Devanagari-Unicode',
 'fibanneacci/langplusplus',
 'azu/nlp-pattern-match',
 'tedunderwood/noveltmmeta',
 'JEnglishOrg/JEnglish',
 'akio-tomiya/intro_julia_minimum',
 'djstrong/PL-Wiktionary-To-Dictionary',
 'Prior99/node-espeak',
 'Helloisa22/Naruto-CardHouver',
 'swirldev/translations',
 'Toluwase/Word-Level-Language-Identification-for-Resource-Scarce-',
 'gasolin/lingascript',
 'Kaljurand/Grammars',
 'nanaian/english',
 'zhaoweih/countries_json',
 'vk4arm/pysoundex',
 'comdet/SnapOCR',
 'karakorakura/Sign-Language-Interpreter',
 'henryfriedlander/Crossword-Puzzle-Maker',
 'A9T9/Baidu-OCR-API',
 'klumsy/DayBreak-ChinesePowerShell',
 'dialogflow/fulfillment-multi-locale-nodejs',
 'rempelj/rawchars',
 'denman2328/Help',
 'qixuanHou/Mapping-My-Break',
 'cetinsamet/pos-tagging',
 'hosford42/pyramids',
 'ajbkr/Hence',
 'Kycb42148/MagicMod',
 'TeamLS/Buzz',
 'tshrinivasan/dhvani-tts',
 'brijohn/onscripter-wii',
 'Rushikesh8983/MastersDataScience_Deep-learning-project',
 'CkauNui/ckau-book',
 'littlefive5/Chinese-English-NLI',
 'piotrmurach/queen',
 'ELI-Data-Mining-Group/PELIC-dataset',
 'Insighter2k/GodHand',
 'Shivam0712/End-to-End_Speech-to-Text_Translation',
 'SayCV/tools-SourceNavigator-NG',
 'HakuoGakuen/HakuoukiSSL',
 'Kaljurand/aceview',
 'placemarkt/wiki_coordinates',
 'puconghan/Computational-Journalism-for-People-s-Daily-Opinion',
 'soumendrak/MTEnglish2Odia',
 'LanguageChatBot/LanguageChatbot',
 'roryap/NppHorizontalRuler-x64-en-US',
 'MifletzetDigdoogim/TextToSignLanguage',
 'Satyaki0924/language-translation-english-to-french',
 'joaomilho/to-be-or-not-to-be',
 'ggu/LanguageSaver',
 'Marwa-Eltayeb/EnglishQuiz',
 'eknkc/dateformat',
 'ridwanskaterock/alrabic',
 'anusaaraka/anusaaraka',
 'Sadhinrana/lms',
 'Chintan2108/Text-Classification-and-Context-Mining-for-Document-Summarization',
 'sigilante/solar-system',
 'nko/nodelay',
 'projeduc/edible-plants-book',
 'MauryaRitesh/Multi-Lingual-Speech-Recognition',
 'Nekliukov/Parleo-backend',
 'yannick-c/expander',
 'konstantinkrumin/konstantinkrumin.github.io',
 'Edditoria/numbo',
 'svilendobrev/smok',
 'catherine667/Automatic-Text-Summarization-and-Title-Generation',
 'jinyanliu/PopularMovies',
 'pulkit110/Natural-Language-Parser',
 'longnow/TeraDict',
 'anseljh/simplified-contract-english',
 'nehal96/Seq2Seq-Language-Translation',
 'words/tree-names',
 'linxiulei/EPlayer',
 'al73rna/Sentibot',
 'kyrylo/entooru',
 'mtancret/pySentencizer',
 'hVostt/PawnHunter.Numerals',
 'bwbaugh/haikupy',
 'jin519/OnlineNaturalLanguageProcessor',
 'elevenvac/asuna-bot',
 'dejurin/language-name-map',
 'rushilrai/A2E',
 'mlsteele/tokipona-lipunimi',
 'Kwbmm/WR-translator',
 'stratosphereips/Hexa_Payload_Decoder',
 'ferhatgec/translatfe',
 'niklasberglund/SwiftChinese',
 'kaplanan/deep-emotion-sense',
 'inwords/InWords',
 'brackendev/Readability-Swift',
 'andreabac3/Bot-Gender-Profiling-Pan2019',
 'abodehq/QuranPDF',
 'hmtanbir/hijricalendar',
 'punkrockpolly/babel-brain',
 'wandji20/Grammar-checker',
 'abhisheknaiidu/BONGS',
 'dreygur/Quran.com',
 'devfabiosilva/myCryptoBot',
 'beatrizalbiero/MsResearch',
 'SerhiiCho/timeago',
 'jefurry/feige',
 'msamwelmollel/2nd-Solution-Swahili-News-Classification-Challenge',
 'heaplinker/heaplinker.github.io',
 'jettbrains/-L-',
 'EllisLab/EE-Language-English',
 'unraid/lang-en_US',
 'g0v-network/training.g0v.network',
 'mandeepshetty/NeuralNetLanguageDetect',
 'sm0svx/svxlink-sounds-en_US-heather',
 'kayspiegel/shopify-notification-templates-l10n',
 'bipinkc19/language-model-lstm',
 'AlaFalaki/ANN-languageDetecor',
 'shashwatkathuria/NLP-Hindi-English',
 'ashishgupta1350/Hindi-English-Code-Mixed-Stemmer',
 'strategineer/writerator',
 'baiyyang/BLEU',
 'alexa/ramen',
 'techczech/phonicsengine',
 'imliam/php-name-of-person',
 'IAmS4n/English_with_Movie',
 'rohitjha/um',
 'ortolanph/JavaBasicConcepts',
 'hack4impact-uiuc/glen-world',
 'campoy/gotalks',
 'facebookresearch/m-amr2text',
 'ChristianSi/lytspel',
 'opener-project/pos-tagger-en-es',
 'off99555/.spacemacs.d',
 'Norod/TrainGPT2-127M-FromScratch',
 'brackendev/Readability-Pharo',
 'shreyansh26/Multilingual-Spellchecker',
 'lucylow/En_francais_si_vous_plait-',
 'heitor31415/LearnSubtitles',
 'AylaRT/ACTER',
 'Tzesh/TzeBot',
 'joaquingatica/notie-imberisseo',
 'klonikar/js-keyboard',
 'mxdi9i7/book',
 'rsalvado/gettext_localize',
 'hotlittlewhitedog/BibleMultiTheLight',
 'google-research-datasets/ccpe',
 'kasraoliz/home.php',
 'michealbalogun/Horizon-dashboard',
 'vivo-project/VIVO-languages',
 'jafl/language_game',
 'Sangarshanan/Neural-Language-Translation',
 'ELI-Data-Mining-Group/pelitk',
 'rin-nas/language-typos',
 'JonathanReeve/cenlab',
 'louisstow/Hence',
 'MegaIng/language',
 'arunism/English-to-Nepali-Language-Translation',
 'IllusionMods/KoikatsuImageTranslation',
 'Guhanxue/Speech-Rater',
 'Drunkar/japanese_talk_api',
 'arpitsaan/wordapp',
 'tedunderwood/hathimetadata',
 'scorpiodwy/MultipleLanguage',
 'spencermountain/simple_english',
 'zbgreen/NaturalLanguageShell',
 'natein/rslang',
 'TotallyPythonic/EnglishComposition',
 'appsplash99/english-to-minion-speak-translator',
 'khromov/wp-english-wp-admin',
 'l5shi/Halide_Tutorial',
 'learn-fluently/learn-fluently-ios',
 'brackendev/Readability-Objective-C',
 'accessibility/multilingual',
 'eaydin/sylco',
 'winkjs/wink-eng-lite-model',
 'hasanTheBest/Al-Quran',
 'PabloEmidio/MultiLanguage-Dictionary',
 'BaseMax/ToyLanguageTranslator',
 'fraunhofer-iais/language-recognition',
 'felipelodur/RNN-Language-Translation-EN-FR',
 'Tejas1415/Neural-Machine-Translation-NMT',
 'vedraj360/Jat-Status',
 'Cuperino/Signspeech',
 'tummychow/titlechaser',
 'jacobkrantz/ProbSyllabifier',
 'DMs-Journal/rosetta',
 'hansel-reinhart/codex-amiatinus',
 'applenob/text_normalization',
 'sarschu/CodeSwitching',
 'perfidia/andip',
 'VedantKhairnar/Translator',
 'ibro45/Speech-to-Speech-Translator',
 'FinNLP/en-lexicon',
 'pjhanwar/POS-Tagger',
 'AliRadwan/Create_PDF',
 'dazcona/sign2text',
 'LiamTownsley/MinecraftEnchantment',
 'karan/learneveryword',
 'prakhar21/Hindi-Transliteration',
 'jainanuj7/indian-numbers',
 'ryanmark1867/git_assistant',
 'joshcutler/Classyfier',
 'paul-shen-stanford/ai-grammar-style-api',
 'mountain-viewer/Translate2Learn',
 'SemanticSoftwareLab/TextMining-MuNPEx',
 'soonin/IOS-Swift-TextToSpeech01',
 'SunilGundapu/DIALOG-ACT-TAGGING-FOR-CODE-MIXED-DATA-SET',
 'krypton-unite/Perspective-Bot',
 'PPPI/POSIT',
 'ayy-em/TelegramSimple_java',
 'Sahrawat1/Semantic-Textual-Similarity',
 'Tanmayrg1999/Web_application_to_convert_numeric_currency_to_text',
 'dallyswag/sqygd',
 'haseebalam/python-twitter-api',
 'AjayKadoula/-Video-English-to-Another-Language-Converter-VEALC-',
 'tomelf/CNIT623-Native-Language-Identification-On-English-Learner-Dataset',
 'pkp/defaultTranslation',
 'mageplaza/magento-2-japanese-language-pack',
 'HegdeChaitra/machine_translation',
 'yuechen/CS-51-Final-Project',
 'fmehmetun/tf_word_language_predictor',
 'TrsNium/TextNormalizationChallenge-EnglishLanguage',
 'NEKOGET/ci_language',
 'Crackshell/heroes-english-history',
 'mapbox/model-un',
 'XoopsModules25x/xlanguage',
 'piyushmishra12/Middle-English-Language-Model',
 'seahrh/wikipedia-spark',
 'alexanderwallin/pineapple-lang',
 'mozilla-bteam/bugzilla-readable-status',
 'dineshvg/LanguageApp',
 'taineleau-zz/Neural-Learner-for-English-Language-Test',
 'dhh15/varieng',
 'naranil/Language-recognition-software',
 'mlightner/engrel',
 'adsglass/NGram-ErrorDetection',
 'RomanKornev/Translate',
 'coraharmonica/blisscribe',
 'winkjs/wink-eng-lite-web-model',
 'gytdau/tome',
 'thatcherclough/Text2ASL',
 'kor0p/translitbot',
 'amirhnajafiz/Airgap-Research',
 'ConverseCSC/asl2english',
 'runexec/WordyBirdy',
 'DQNEO/gospec'
 

 


 
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
            f"response: {json.dumps(response_data)}, "
            f" url: {url}"
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