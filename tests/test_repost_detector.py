import pytest
import modbot.input.test as test

TEST_SUBREDDIT = "testsub123"
enable_flair_posts = """
[Enabled Plugins]
repost_detector
"""

@pytest.fixture
def create_bot():
    test.create_bot(TEST_SUBREDDIT)

def test_repost_detector(create_bot):
    wiki_flair_posts = """
    [Setup]
    minimum_word_length = 3
    minimum_nb_words = 5
    min_overlap_percent = 50
    """
    sub = test.get_subreddit(TEST_SUBREDDIT)

    # Update control panel and plugin wiki
    sub.edit_wiki("control_panel", enable_flair_posts)
    sub.edit_wiki("repost_detector", wiki_flair_posts)

    # Give some time to the bot to get the new wiki configuration
    test.advance_time_60s()

    # Create a new submissinon that we will be testing against
    test_submission1 = test.FakeSubmission(subreddit_name=TEST_SUBREDDIT, author_name="JohnDoe1",
        title="AAAA BBBB CCCC DDDD EEEE FFFF")
    test.new_all_sub(test_submission1)

    test.advance_time_30m()

    # Create another submission
    test_submission2 = test.FakeSubmission(subreddit_name=TEST_SUBREDDIT, author_name="JohnDoe1",
        title="AAAA BBBB CCCC DDDD EEEE GGGG")
    test.new_all_sub(test_submission2)
    test.advance_time_10m()

    assert(len(test_submission2.reports) == 1)

    test.advance_time_30m()

    # Test short word elimination
    test_submission3 = test.FakeSubmission(subreddit_name=TEST_SUBREDDIT, author_name="JohnDoe1",
        title="AAAA BBBB CCCC DDDD")
    test.new_all_sub(test_submission3)

    assert(len(test_submission3.reports) == 0)

    # Jump in time one month
    test.advance_time(2592000)
    test.new_all_sub(test.FakeSubmission(subreddit_name=TEST_SUBREDDIT, author_name="JohnDoe1",
        title="AAAB BBBC CCCD DDDE EEEG GGGF"))
    # Give the chance to remove a post from storage due to being too old
    test.advance_time_30m()

def test_invalid_cfg(create_bot):
    wiki_flair_posts = """
    [Seup]

    """
    test.create_bot(TEST_SUBREDDIT)
    sub = test.get_subreddit(TEST_SUBREDDIT)
    # Update flair posts control panel
    sub.edit_wiki("control_panel", enable_flair_posts)
    sub.edit_wiki("repost_detector", wiki_flair_posts, author="wikieditboy_repost")

    test.advance_time_30m()

    assert(len(test.get_user("wikieditboy_repost").inbox) == 1)