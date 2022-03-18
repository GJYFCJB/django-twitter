#Social Media Backend System

This project is similar to twitter’s backend system. By the help of Django’s api and databases, we can realize this system which can support twitter functions like sending likes and comments, add friends and send messages, post and follow.

Using django: model, view, **template**

Django rest framework: ***Serializer***

I design this project and divide it into nine parts:

use the `method_decorator` to limit the ****Visit frequency and method of bad users.

**accounts :** 

store the information of users by using model layer and MySQL to store the account information - like to_user-id and from_user-id. 

Implement serializers class to rendered data into JSON

**comments:** 

has 3 variable to identify - content tweet_id user_id

Using Redis to store the reliional data comments and implement the foreignKey to add relations between the comments and users who give comments.

implement list create update destroy method for comments .generic’ views class  `get_queryset`  to list. Implements DRF `serializer.save()` to create / update comments. 

**Hbase:** 

use hbase to access the data we store. non-relational database. imitate the twitter’s accessing data process.

we store id’s nickname and avatar in the hbase cause we do not need change id usually and id’s number is huge usually.

Use Apache HBase™ when you need random, realtime read/write access to your Big Data. This project's goal is the hosting of very large tables -- billions of rows X millions of columns -- atop clusters of commodity hardware. 

**friendships:** 

use DRF’ pagination class. Set the friendships viewSet and effect like following and unfollowing. Using redis to store relationship like following and unfollowing cause redis is **In-memory datastore which means faster response times.**

**Gatekeeper:** helper class for Redis. Help us access and read cache data from Redis. non-relational database. 

**inbox:** inbox message of social media.  get post querySet method to read and mark the notifications read or unread - actually access the value stored in the database. 

**Likes:** 

develop create, cancel in views class by django response ap

use memcached to store user id in likes comments friendships tweets class.

**Newsfeeds:** 

like notifications in the IOS. Store these data in the memory and implement get_cached_newsfeeds and push_cached_newsfeeds to push and get data from Redis

if the user click the newsfeeds we need to switch to other database to access data like tweets.

use `HBaseNewsFeed` method to realize.

**Tweets:** Store the data id,content,likes,photos,etc, like a real tweet. 

store in the hbase cause we need to store it for long time and he number is huge.

But we also store some tweets(the newest) in redis so the user can access it quickly. 

normal create and list method in views class
