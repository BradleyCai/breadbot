# BreadBot
A bot written in python for posting files from a list with source.

## Setup
A server config file must be made for each discord server you'd like to post to. 
To create one, first populate the folder `./bots/files` with the files you'd like 
to use. Then use the `initlist` function in filelister.py to create your config
file. This config file will keep track of the files you can post, and which you
have posted already. To add files to the list, use the function `relist` in filelister.py.

## Usage
"discordbot.py" is used to post the images. It's syntax is:  
`discordbot.py [-h] <config-name>`  
It will post the next file in the list, and update the config file. It is recommended to set up
a cron job to schedule when you'd like to post these files.

## License
This tool is licensed under the MIT license.

