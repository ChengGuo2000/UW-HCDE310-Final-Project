#!/usr/bin/env python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from flask import Flask, render_template, request
import logging, json, urllib

app = Flask("HW7")

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

def get_def(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    key_dict = {"key": key}
    keystr = urllib.parse.urlencode(key_dict)
    word = word.split(" ")[-1]
    request_url = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?" + keystr
    request_str = urllib.request.urlopen(request_url).read()
    word_json = json.loads(request_str)
    word_def = word_json[-1]["shortdef"][0]
    return word_def

def get_def_safe(word, key = "b218b944-89f2-4f6d-909e-37649d0fc5fa"):
    try:
        result = get_def(word = word, key = key)
    except Exception as error:
        print("Error: " + str(error))
    return result

@app.route("/",methods=["GET","POST"])
def main_handler():
    app.logger.info("In MainHandler")
    word = request.form.get('word')
    wantDefinitions = request.form.get("definitions")
    if word:
        syn_list = get_synonyms_safe(word)
        page_title = "Synonyms for %s"%word
        def_dict = {}
        for word in syn_list:
            new_word = "-".join(word.split(" "))
            short_def = get_def_safe(new_word)
            def_dict[word] = short_def
        return render_template('hw7form.html',
            word=word,
            wantDefinitions = wantDefinitions,
            page_title=page_title,
            syn_list = syn_list,
            def_dict = def_dict)
    else:
        return render_template('hw7form.html',
            page_title="HW7 Synonyms - Error",
            prompt="We need a word")

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)