"""Unit tests for HTML content cleaner."""

from core.content_cleaner import ContentCleaner


def test_content_cleaner_strips_scripts_and_nav():
    cleaner = ContentCleaner()
    raw_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Business API Pricing Guide | Wati</title>
        <meta property="article:published_time" content="2024-04-12T10:00:00Z" />
    </head>
    <body>
        <nav>Home | Products | Contact</nav>
        <script>console.log('tracker');</script>
        <div class="cookie-banner">Accept cookies to continue</div>
        <article>
            <h1>Understanding WhatsApp Business API Pricing</h1>
            <p>Meta charges per 24-hour conversation window which makes cost forecasting difficult for small retailers.</p>
            <p>Many small business owners struggle with unpredictable monthly conversation charges.</p>
        </article>
        <footer>Copyright 2024. All rights reserved.</footer>
    </body>
    </html>
    """

    title, text, pub_date = cleaner.clean_html(raw_html, "https://getwati.com/pricing")

    assert "WhatsApp Business API Pricing Guide" in title
    assert pub_date == "2024-04-12"
    assert "tracker" not in text
    assert "Accept cookies" not in text
    assert "All rights reserved" not in text
    assert "Meta charges per 24-hour conversation window" in text
    assert "unpredictable monthly conversation charges" in text


def test_content_cleaner_empty_input():
    cleaner = ContentCleaner()
    title, text, pub_date = cleaner.clean_html("", "")
    assert title == "Untitled Page"
    assert text == ""
    assert pub_date is None

