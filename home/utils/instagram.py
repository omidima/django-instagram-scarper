from typing import List
import pandas
import instagrapi
from instagrapi.types import Media,Story

class Instagram():
    def __init__(self,username):
        self.client = instagrapi.Client()
        self.client.login_by_sessionid("40355799769%3A9uyxIfOwgd7zRo%3A23")
        self.userId = self.client.user_id_from_username(username=username)

    def getUserFollowers(self):
        return self.client.user_followers_v1(user_id=self.userId)

    def getUserPosts(self,end_post = ""):
        if end_post == "":
            posts = self.client.user_medias_paginated(user_id=self.userId,end_cursor='',amount=20)
        else :
            posts = self.client.user_medias_paginated(user_id=self.userId,end_cursor=end_post)

        return posts

    def getPostWithHashtag(self,hashtag: str) -> List[Media]:
        data = self.client.user_medias(user_id=self.userId)
        items = []
        for item in data:
            if hashtag in item.caption_text:
                items.append(item)
        return items

    def getUserStory(self):
        stories = self.client.user_stories_v1(self.userId)
        return stories

    def getUserStoriesWithHashtag(self,hashtag: str):
        data = self.client.user_stories_v1(self.userId)
        
        items = []
        for item in data:
            for hashtag in item.hashtags:
                if hashtag.hashtag.name.find(hashtag) > -1:
                    items.append(items)
        return items


if __name__ == '__main__':
    posts =Instagram(username='he3am.ui').getUserPosts(end_post='2688086893343726087')
    print(posts)
