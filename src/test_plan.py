import pipe
import unittest


class Test_Pipe(unittest.TestCase):
    sample_youtube = "https://www.youtube.com/watch?v=ysXo7MV2zko"
    sample_webpage = "https://core.telegram.org/bots/api"
    sample_twitter = "https://twitter.com/elonmusk/status/1630727911014559745"
    sample_text = "This is a sample text"

    def test_add_youtube_url(self):
        # test add_youtube_url method
        subject, url, html = pipe.create_content(
            f"/add {self.sample_youtube}")
        # assert html contains <html>
        assert "<html>" in html


# def test_get_url(self):
#     # test get_url method
#     self.assertEqual(pipe.get_url("https://www.google.com"), "webpage")
if __name__ == "__main__":
    unittest.main()
