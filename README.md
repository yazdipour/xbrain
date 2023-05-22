# XBrain

<img src="logo.jpg" height="240"/>

Telegram bot to help you read and summarize content. It uses [Omnivore](https://Omnivore.app) [or Pocket, Instapaper, Matter] to save the content and [OpenAI](https://openai.com) to summarize it.

## Features

* Message Template: `/command [args: URL or text]`
* `/add` to add the content to the ReadLater service
* `/add YoutubeURL` get youtube transcript
* `/sum` to summarize the content
* `/sum YoutubeURL` get youtube transcript and summarize
* `/ask` to ask a question from ChatGPT about the content
* `/thread` to get a twitter thread
* `/token` to add your OpenAI token

## TODO

* [ ] Book Reader!
* [ ] OpenAI Token Getter (Now it check if it is me, it will allow openAI usage)

## Pipedream

![image](https://github.com/yazdipour/xbrain/assets/8194807/da63d7cd-51f9-4d6a-bfa3-984cf5fd3bdc)

## AppDiagram

![xbrain diagram](docs/diagram.png)
