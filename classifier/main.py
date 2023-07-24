from classifier.custom_classifier import run_custom
from classifier.textblob_classifier import run_textblob
from classifier.vader_classifier import run_vader


def run_classifiers(scrape_id):
    """Run vader, textblob and custom classifiers sequentially"""
    run_vader(scrape_id)
    run_textblob(scrape_id)
    run_custom(scrape_id)

    return
