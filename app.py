from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk

app = Flask(__name__)

socket_io = SocketIO(app)


@app.route('/')
def hello_world():
    return render_template("summarize.html")


@socket_io.on("summarize")
def summarize(data):
    # use sumy to summarize the text entered
    summarizer = LexRankSummarizer()
    parser = PlaintextParser.from_string(data["text"], Tokenizer("english"))
    summary = summarizer(parser.document, data["lines"])

    # formatted summary
    text = "\t"

    # extract and format the text from the summarizer
    counter = 0
    for line in summary:
        if counter >= 5:
            text += "<br><br>\t"
            counter = 0

        text += str(line) + " "
        counter += 1

    # respond to the user with the summarized text
    emit("response", text)
    pass


if __name__ == '__main__':
    socket_io.run(app)
