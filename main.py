#!/usr/bin/env python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, render_template, request
import numpy
from PIL import Image
import json, urllib
from wordcloud import WordCloud
from random2 import randint

app = Flask("Final_Project")

def get_synonyms(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    key_dict = {"key": key}
    keystr = urllib.parse.urlencode(key_dict)
    word = "-".join(word.split(" "))
    request_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?" + keystr
    request_str = urllib.request.urlopen(request_url).read()
    word_json = json.loads(request_str)
    syns_lists = word_json[0]["meta"]["syns"]
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

def get_frequency(word_list, used):
    new_list = []
    for word in word_list:
        new_list.append(word)
        syn_list = get_synonyms_safe(word)
        for new_word in syn_list:
            new_list.append(new_word)
    freq_dict = {}
    for word in new_list:
        if word not in freq_dict:
            freq_dict[word] = 0
        freq_dict[word] += 1
    used = used.lower()
    new_dict = {key: val for key, val in freq_dict.items() if key != used}
    return new_dict

def get_frequency_safe(word_list, used):
    try:
        result = get_frequency(word_list = word_list, used = used)
    except Exception as error:
        print("Error: " + str(error))
    return result

def make_word_cloud(freq_dict):
    image_name = "crow_images/crow" + str(randint(1,6)) + ".jpg"
    crow_mask = numpy.array(Image.open(image_name))
    cloud = WordCloud(background_color="black", mask = crow_mask)
    cloud.generate_from_frequencies(freq_dict)
    return cloud.to_svg()

def make_word_cloud_safe(freq_dict):
    try:
        result = make_word_cloud(freq_dict = freq_dict)
    except Exception as error:
        print("Error: " + str(error))
    return result

@app.route("/",methods=["GET","POST"])
def main_handler():
    app.logger.info("In MainHandler")
    word = request.form.get('word')
    if word:
        syn_list = get_synonyms_safe(word)
        syn_dict = get_frequency_safe(syn_list, word)
        cloud_image = make_word_cloud_safe(syn_dict)
        return render_template('project_template.html',
            word=word,
            cloud_image = cloud_image)
    else:
        return render_template('project_template.html',
            page_title="CROW - Error",
            prompt="We need a word")

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)