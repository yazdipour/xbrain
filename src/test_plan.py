import pipe
import unittest


class Test_Pipe(unittest.TestCase):
    sample_youtube = "https://www.youtube.com/watch?v=ysXo7MV2zko"
    sample_webpage = "https://core.telegram.org/bots/api"
    sample_twitter = "https://twitter.com/elonmusk/status/1630727911014559745"
    sample_text = "This is a sample text"

    def test_add_youtube_url(self):
        _, _, html = pipe.create_content(f"/add {self.sample_youtube}")
        assert "URL:" in html
    
    def test_add_webpage_url(self):
        subject, _, html = pipe.create_content(f"/add {self.sample_webpage}")
        assert "" in html # raw url should not have html
        assert subject == self.sample_webpage

if __name__ == "__main__":
    unittest.main()
