# pipedream add-package youtube-transcript-api

from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
import openai


def handler(pd: "pipedream"):
    event = pd.steps["trigger"]["event"]["message"]
    global openapi_key
    openapi_key = pd.inputs["openai"]["$auth"]["api_key"]
    if event["from"]["username"] != "theshahriar":
        raise ValueError("Not authorized")
    msg = event["text"]
    subject, html = create_content(msg)
    return {
        "subject": f"[XBrain] {subject}",
        "text": f"Text: [XBrain] {subject}",
        "html": html,
    }


def create_content(
    user_msg="/add Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
):
    # check if the user_msg starts with a command '/'
    if user_msg[0] != "/":
        command = "/add"
        content = user_msg
    else:
        command = user_msg.split(" ")[0]
        content = " ".join(user_msg.split(" ")[1:])

    if content == "":
        raise ValueError("Content is empty")
    # check if the command is valid
    if command == "/sum":
        subject, html = sum(content)
        return subject, html
    elif command == "/book":
        subject, html = book(content)
        return subject, html
    if command == "/thread":
        subject, html = add_twitter_thread_url(content)
        return subject, html
    else:
        # add command to the content if it is not /add
        if command != "/add":
            content = f"{command} {content}"
        subject, html = add(content)
        return subject, html


def add(content):
    type = content_type(content)
    if type == "youtube":
        subject, html = add_youtube_url(content)
        return subject, html
    elif type == "webpage":
        subject, html = add_webpage_url(content)
        return subject, html
    else:
        subject = content.split("\n")[0]
        return subject, f"<html>{content}</html>"


def sum(content):
    type = content_type(content)
    if type == "youtube":
        subject, html = sum_youtube_url(content)
        return subject, html
    elif type == "webpage":
        subject, html = sum_webpage_url(content)
        return subject, html
    else:
        html = get_summarized(content)
        subject = content.split("\n")[0]
        return subject, html


# TODO: NOT SUPPORTED YET
def book(url):
    raise ValueError("Not supported yet")
    # subject = get_pagetitle(url, "")
    # html = f"<html>NOT SUPPORTED YET</html>"
    # return subject, html


def add_webpage_url(url):
    html = download_html(url)
    subject = get_pagetitle(url, html)
    return subject, f"{html}<br><a href='{url}'>URL: {url}</a>"


def add_twitter_thread_url(url):
    # convert twitter url to threadreaderapp url
    twit_id = url.split("/")[-1]
    url = f"https://threadreaderapp.com/thread/{twit_id}"
    html = download_html(url)
    html = f"<html>{html}<a href='{url}'>URL: {url}</a></html>"
    subject = get_pagetitle(url, html)
    return "[TWT]" + subject, html


def add_youtube_url(url):
    subject = get_pagetitle(url, "")
    transcript = get_youtube_transcript(url)
    html = f"<html><br>{transcript}<a href='{url}'>URL: {url}</a></html>"
    return subject, html


def sum_youtube_url(url):
    transcript = get_youtube_transcript(url)
    if "Error:" not in transcript:
        transcript = get_summarized(transcript)
    html = f"<html><a href='{url}'>URL: {url}</a><br>{transcript}</html>"
    subject = get_pagetitle(url, "")
    return "[SUM]" + subject, html


def sum_webpage_url(url):
    html = download_html(url)
    body = html.split("<body>")[1].split("</body>")[0]
    # remove all the svg, img, script, style, link, meta, noscript
    body = re.sub(r"<svg.*?</svg>", "", body, flags=re.DOTALL)
    body = re.sub(r"<img.*?>", "", body, flags=re.DOTALL)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.DOTALL)
    body = re.sub(r"<link.*?>", "", body, flags=re.DOTALL)
    body = re.sub(r"<meta.*?>", "", body, flags=re.DOTALL)
    body = re.sub(r"<noscript.*?</noscript>", "", body, flags=re.DOTALL)
    body = get_summarized(body)
    subject = get_pagetitle(url, html)
    return "[SUM]" + subject, f"<html><a href='{url}'>URL: {url}</a><br>{body}</html>"


def content_type(content):
    # url is from youtube or not
    if "youtu.be" in content or "youtube.com" in content:
        return "youtube"
    elif "twitter.com" in content:
        return "twitter"
        # starts with http or https
    elif re.match(r"^https?://", content):
        return "webpage"
    else:
        return "text"


def get_pagetitle(url, html):
    # html is empty or does not contain title
    if html == "" or "<title>" not in html:
        title = url
    else:
        title = html.split("<title>")[1].split("</title>")[0]
    return title


def download_html(url):
    return requests.get(url).text


def get_summarized(text, openai_api_key: str = ""):
    if openai_api_key == "":
        global openapi_key
        openai_api_key = openapi_key
    openai_helper = OpenAIHelper(openai_api_key)
    return openai_helper.get_summary(text)


def get_youtube_transcript(url):
    return YoutubeTranscriptApiHelper().get_transcript(url)


class OpenAIHelper:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def call_chatgpt(
        self,
        messages: List[Dict[str, str]],
        temperature: int = 0,
        model: str = "gpt-3.5-turbo",
    ) -> str:
        # temperature: What sampling temperature to use, between 0 and 2.
        # Higher values like 0.8 will make the output more random,
        # while lower values like 0.2 will make it more focused and deterministic.
        return openai.ChatCompletion.create(
            model=model, temperature=temperature, max_tokens=100, messages=messages
        )

    def get_system_prompt(self):
        return [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant to help you create TLDR summaries of content from various sources like books, webpage articles, and YouTube transcripts."
                ),
            },
        ]

    def get_user_prompt(self, content: str):
        return {"role": "user", "content": (f"Create a TLDR summary for the following content, capturing all important information: {content}")}

    def get_summary(self, text):
        prompt = self.get_system_prompt()
        prompt.append(self.get_user_prompt(text))
        response = self.call_chatgpt(prompt)
        return response.choices[0].message.content


class YoutubeTranscriptApiHelper:
    def get_video_id_from_url(self, url):
        video_id = None
        pattern = re.compile(
            r"(?:http(?:s)?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9-_]+)"
        )
        match = pattern.search(url)
        if match:
            video_id = match.group(1)
        return video_id

    def get_transcript_from_id(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_transcript(self, url):
        video_id = self.get_video_id_from_url(url)
        if video_id:
            transcript = self.get_transcript_from_id(video_id)
            if transcript:
                return " ".join([entry["text"] for entry in transcript])
            else:
                raise Exception("No transcript found for the video.")
        else:
            raise Exception("Invalid YouTube URL.")
