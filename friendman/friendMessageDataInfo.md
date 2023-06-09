# INFORMATION ABOUT FRIEND DATA

The model FriendMessageData is a model that contains the 
information of friend requests, friend information, and chat
messages that may have been sent.

## FriendRequest
* **user**: The username of the user that sent the friend rq
* **date**: The date the friend request was sent. This will be 
            stored in epoch time, for easy time zone manipulation
* **id**: The id of the friend request. This is a unique id
         that is generated by the database

Friend request information will be stored in the database as a 
python list. An example of this is shown below:

    "user": "atomtables",
    "date": 1234567890,
    "id": "72826-7ds7ashd289j-4324764" ***randomly generated***

This will be stored in the database using the JSONField model
for Django. This will allow for easy manipulation of the data
in the database, and easy access through Django templates and
views.

## Friend
* **user**: The username of the user **that was friended**
* **date**: The date the friend was added. This will be 
            stored in epoch time, for easy time zone manipulation
* **id**: The id of the friend. This is a unique id
         that is generated by the database, and this will only be deleted
         if the friend is removed

Friend information will be stored in the database as a python
list. An example of this is shown below:

    "user": "atomtables",
    "date": 1234567890,
    "id": "72826-7ds7ashd289j-4324764" ***randomly generated***

This will be stored in the database using the JSONField model,
the same way as a FriendRequest. Friend information will be 
accessed by the user using the url: `/friends/<username>`. To
chat with a friend, a user will go to `/chatting/<username>`. The user
will be unable to chat with a user until they have sent a friend
request, and the friend request has been accepted.

## UPDATE 20/5
we are adding an extra field to the friend information
model called `outgoing_friend_requests`. This will only
be used to manage the friend requests that the user has
sent. This will be stored in the database as a python list.
For everything else, we will use `incoming_friend_requests`,
prior known as `friend_requests`.
