from flask import Flask, request, render_template_string # type: ignore
import requests # type: ignore
import fitz # type: ignore
from io import BytesIO
from model import Summarizer

app = Flask(__name__)
model=Summarizer()
# Simple HTML form
HTML_FORM = '''
<!doctype html>
<title>PDF Fetcher</title>
<h2>Enter PDF URL</h2>
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="pdf" accept="application/pdf" required />
  <input type="submit" value="Summarize PDF" />
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            print("error: No file uploaded, 400")

        pdf_file = request.files['pdf']
        if not pdf_file.filename.endswith('.pdf'):
            print("error: File is not a PDF, 400")

        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            if not text.strip():
                print("error: No extractable text in PDF, 400")

            summary_text = model.infer(text)
            print("summary: ", summary_text)
            print(len(summary_text))

        except Exception as e:
            print("error: Failed to process PDF: ",str(e)), 500
    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)
