#!/usr/bin/env python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, render_template, request
from random2 import randint
import json, urllib
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = Flask("Final_Project")

def get_synonyms(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    key_dict = {"key": key}
    keystr = urllib.parse.urlencode(key_dict)
    request_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?" + keystr
    request_str = urllib.request.urlopen(request_url).read()
    word_json = json.loads(request_str)
    syns_lists = word_json[-1]["meta"]["syns"]
    final_list = []
    for syns in syns_lists:
        for syn in syns:
            final_list.append(syn)
    return final_list

def get_synonyms_safe(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    try:
        result = get_synonyms(word = word, key = key)
    except Exception as error:
        print("Error: " + str(error))
    return result

def get_frequency(word_list):
    new_list = word_list
    for word in word_list:
        new_part = get_synonyms_safe(word)
        for new_word in new_part:
            new_list.append(new_word)
    freq_dict = {}
    for word in word_list:
        if word not in freq_dict:
            freq_dict[word] = 0
        else:
            freq_dict[word] += 1
    return freq_dict

def make_word_cloud(freq_dict):
    img_name = "crow" + str(randint(1,6)) + ".png"
    crow_mask = np.array(Image.open(img_name))
    cloud = WordCloud(background_color="Moccasin", mask=crow_mask)
    cloud.generate_from_frequencies(freq_dict)
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()
    plt.savefig("wordcloud.png")



@app.route("/",methods=["GET","POST"])
def main_handler():
    app.logger.info("In MainHandler")
    word = request.form.get('word')
    if word:
        syn_list = get_synonyms_safe(word)
        page_title = "Synonyms for %s"%word
        return render_template('project_template.html',
            word=word,
            page_title=page_title,
            syn_list = syn_list)
    else:
        return render_template('project_template.html',
            page_title="HW7 Synonyms - Error",
            prompt="We need a word")

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)