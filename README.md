# XBrain

<img src="logo.jpg" height="240"/>

Telegram bot to help you read and summarize the content. It uses [Omnivore](https://Omnivore.app) [or Pocket, Instapaper, Matter] to save the content and [OpenAI](https://openai.com) to summarize it.

## Features

* Message Template: `/command [args: URL or text]`.
* `/add` to add the content to the ReadLater service.
* `/add YoutubeURL` grabes youtube transcript.
* `/sum` to summarize the content.
* `/sum YoutubeURL` get youtube transcript and summarize.
* `/ask` to ask a question from ChatGPT about the content.
* `/token` to add your OpenAI token [ToDo].

## TODO

* [ ] This sends the content to the pipedream user email. Find a way to make it general.

## AppDiagram

Copy the Pipedream diagram for yours: <https://pipedream.com/new?h=tch_3M9fP9>

```mermaid
graph TB
  User -->|message| TelegramServer
  subgraph "PipeDream Service";

    pipeTelegram --> checkType
    checkType -->|youtube| GetTranscript
    checkType -->|URL| GetHTML
    checkType -->|text| PipePython

    GetHTML --> PipePython
    GetTranscript --> PipePython
    PipePython --> checkCommand
    checkCommand -->|/add| pipeEmail
  end
  
  OpenAI([OpenAI])
  checkCommand -->|/sum| OpenAI
  checkCommand -->|/ask| OpenAI
  TelegramServer --> pipeTelegram
  OpenAI --> pipeEmail
  pipeEmail -->|HTML| Omnivore
```

## Pipedream setup

![image](https://github.com/yazdipour/xbrain/assets/8194807/da63d7cd-51f9-4d6a-bfa3-984cf5fd3bdc)
