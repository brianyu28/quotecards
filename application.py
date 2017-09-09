from flask import Flask, render_template, request, session, redirect, url_for, Response
import os
import os.path
import re
from PIL import Image, ImageFont, ImageDraw
import textwrap
import random
import datetime

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def quotehome():
    if request.method == "GET":
        return render_template('quotecard.html')
    if request.method == "POST":
        quote = request.form['quote']
        author = request.form['author']
        position = request.form['position']
        opinion = 'opinion' in request.form
        filename = img_generate(quote, author, position, opinion)
        mimetype = "image/png"
        content = get_file(filename)
        os.remove(filename)
        with open("quotecard_files/logs.txt", "a") as f:
            f.write(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ": " + quote + " -" + author + " (" + position + ")" + (", Opinion\n" if opinion else "\n"))
            f.close()
        return Response(content, mimetype=mimetype)
    
def get_file(filename):
    try:
        print(filename)
        return open(filename, "rb").read()
    except IOError as exc:
        return str(exc)

def img_generate(quote, author, position, opinion):
    quotetext_font = ImageFont.truetype("quotecard_files/suecaslab-light.otf", 60)
    authortext_font = ImageFont.truetype("quotecard_files/suecaslab-heavy.otf", 60)
    titletext_font = ImageFont.truetype("quotecard_files/suecaslab-light.otf", 45)
    opinion_font = ImageFont.truetype("quotecard_files/suecaslab-semibold.otf", 60)
    thc_op_font = ImageFont.truetype("quotecard_files/bigmoore.otf", 18)
    thc_font = ImageFont.truetype("quotecard_files/bigmoore.otf", 36)

    breakquote = textwrap.wrap(quote, width=35)

    img = None
    if opinion:
        img = Image.new('RGB', (1120, 600), "#a82931")
        draw = ImageDraw.Draw(img)
        counter = 0
        for line in breakquote:
            draw.text((28,50 + (counter * 60)), line, font=quotetext_font, fill=(255,255,255,255))
            counter += 1
        draw.text((28, 420), author, font=authortext_font, fill=(255,255,255,255))
        draw.text((28, 490), position, font=titletext_font, fill=(255,255,255,255))

        draw.text((860, 510), "opinion", font=opinion_font, fill=(255,255,255,255))
        draw.text((922, 570), "The Harvard Crimson", font=thc_op_font, fill=(255,255,255,255))
        draw = ImageDraw.Draw(img)
    else:
        seal = Image.open("quotecard_files/seal-trans-sm.png")
        img = Image.new('RGB', (1120,600), "white")
        img.paste(seal, (800, 250), seal)
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0,0), (1120, 30)], "#a82931")
        counter = 0
        for line in breakquote:
            draw.text((28,50 + (counter * 60)), line, font=quotetext_font, fill="#a82931")
            draw.text((28, 420), author, font=authortext_font, fill="#a82931")
            draw.text((28, 490), position, font=titletext_font, fill="#a82931")
            draw.text((775, 550), "The Harvard Crimson", font=thc_font, fill="#a82931")
            counter += 1
        draw = ImageDraw.Draw(img)

    imgid = random.randint(1000000, 999999999)
    filename = "quotecard_files/tmp/quotecard" + str(imgid) + ".png"

    img.save(filename)
    return filename

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
