Metatweet
================
MetaTweet is a web application that tacks two of the issues mentioned in Cory Doctorow's "Metacrap", namely "people are lazy" and "people are stupid"--it helps twitter user look for hashtags and images that are relevant to his/her tweet. In addition, the layout is responsive, i.e. it is optimized for different types of displays (desktop, tablet horizontal/vertical, & mobile).

User flow: after writing the tweet, the user would highlight a word/phrase that s/he would like to search and click the "search" link. The app will crawl Twitter and Flickr to find relevant tags and images. The user can then add the tag(s) and/or image(s) that s/he deems relevant to the tweet. Once the user is done, s/he would click "post" and the tweet will be posted on his/her Twitter account.

Re: workflow, in the beginning, we mostly worked in parallel--while Kate & Max focused on the back-end functionalities, Raymon built the front-end components. Around the middle of the timeline, we integrated the components and got a taste of how the app functions. Afterward, we kept on refining the details and worked on functionality issues. 


## Installation ##
heroku config:add TWITTER_CONSUMER_TOKEN='your token here'
heroku config:add TWITTER_CONSUMER_SECRET='your secret here'

## Project Team and Roles
* [Raymon Sutedjo-The](http://ray-mon.com/) -- interaction & interface design, main front-end functionalities
* [Kate Rushton](http://krushton.com) - back-end functionality for image search, additional front-end functionalities
* [Max Gutman]() -- back-end functionality for tag search, additional front-end functionalities

## Demo Version
http://metatweet.herokuapp.com

## What's Under the Hood

### Technologies Used
* Code: HTML, CSS, Python, JavaScript, jQuery, JSON
* Framework: Flask
* APIs: Flickr, Twitter

### Browser Support
Chrome, Safari, Firefox

### Bugs, Quirks, Easter Eggs
* Text selection on mobile is slightly buggy