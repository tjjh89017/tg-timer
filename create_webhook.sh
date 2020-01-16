#!/bin/bash

token=$1
webhook='https://tg-timer.herokuapp.com/hook'
curl -d "url=$webhook_url "https://api.telegram.org/bot$token/setWebhook"
