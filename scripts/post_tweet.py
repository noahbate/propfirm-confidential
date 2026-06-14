#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script will be used to post tweets to the @Prop_Firm_Codes account.
"""

import os
import sys

def post_tweet(content):
    """
    Posts a tweet using the xurl CLI.
    """
    print(f"Posting tweet: {content}")
    # Use shlex.quote to ensure the content is safely passed to the shell
    import shlex
    quoted_content = shlex.quote(content)
    command = f"xurl post {quoted_content}"
    print(f"Executing: {command}")
    os.system(command)

def main():
    """
    Main function to drive the script.
    """
    if len(sys.argv) > 1:
        tweet_content = sys.argv[1]
        post_tweet(tweet_content)
    else:
        print("Usage: python post_tweet.py \"<your tweet content>\"")

if __name__ == "__main__":
    main()
