from flask import Flask, jsonify, request, send_file
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from flask_cors import CORS
import json
import re

es = Elasticsearch()
# tokenizer = SinhalaTokenizer()

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return send_file('views/template.html')

@app.route('/insert_data', methods=['POST'])
def insert_data():
    if es.indices.exists(index="songs"):
        data = []
        with open('sinhala_songs.json', encoding="utf-8") as json_file:
            data = json.load(json_file)
        result = bulk(es, data)
        return jsonify(result), 201
    else:
        return jsonify({"error":"No index found"}), 404

#query_words = input_query.split()
@app.route('/search', methods=['GET'])
def search():
    input_query = request.args.get('q')
    query_words = input_query.split()

    movie_list = ['චිත්‍රපට', 'සිනමා']
    music_keywords = ['සංගීතමය', 'සංගීතවත්', 'අධ්‍යක්ෂණය', 'සංගීත']
    genre_keywords = []
    artist_keywords = ['කීව', 'කී', 'ගායනා කරන', 'ගයන', 'ගායනා', '‌ගේ', 'හඩින්', 'කියනා', 'කිව්ව', 'කිව්', 'කිව', 'ගායනය',
                   'ගායනා කළා', 'ගායනා කල', 'ගැයූ']
    writer_keywords = ['ලියා', 'ලියූ', 'ලිව්ව', 'ලිව්', 'රචනා', 'ලියා ඇති', 'රචිත', 'ලියන ලද', 'ලියන', 'හදපු', 'පද',
                    'රචනය', 'හැදූ', 'හැදුව', 'ලියන', 'ලියන්න', 'ලීව', 'ලියපු', 'ලියා ඇත', 'ලිඛිත']
    popular_kewords = ["ජනප්‍රිය", "ප්‍රසිද්ධ", "හොඳම"]
    is_popular_query = False

    is_title = True
    is_artist = False
    is_lyrics = False
    is_writer = False
    is_music = False
    is_genre = False
    new_query = ""
    fields_list = []
    output_size = -1

    for word in query_words:
        if (word in music_keywords):
            is_music = True
        elif word in genre_keywords:
            is_genre = True
        elif word in artist_keywords:
            is_artist = True
        elif word in writer_keywords:
            is_writer = True
        elif word in popular_kewords:
            is_popular_query = True
        elif (word.isdigit()):
            output_size = word
        else:
            new_query = new_query + word + " "
    print(new_query)
    input_query = new_query

    d_title = "title*"
    d_artist = "artist*"
    d_lyrics = "lyrics*"
    d_writer = "writer*"
    d_music = "music*"
    d_genre = "genre"

    if (d_writer or d_artist or d_music or d_genre):
        is_title = False
    if is_music:
        if (is_popular_query):
            fields_list.append(d_music)
        else:
            d_music += "^4"
    if is_artist:
        if (is_popular_query):
            fields_list.append(d_artist)
        else:
            d_artist += "^4"
    if is_writer:
        if (is_popular_query):
            fields_list.append(d_writer)
        else:
            d_writer += "^4"
    if is_genre:
        if (is_popular_query):
            fields_list.append(d_genre)
        else:
            d_genre += "^4"
    if is_title:
        if (is_popular_query):
            fields_list.append(d_title)
        else:
            d_title += "^4"

    if is_popular_query:
        if (output_size == -1):
            output_size = 40
        if (len(input_query.strip()) == 0):
            body = {
                "sort": [{
                    "visits": {
                        "order": "desc"
                    }
                }
                ],
                "size": output_size
            }

        else:
            body = {
                "query": {
                    "query_string": {
                        "query": input_query,
                        "type": "bool_prefix",
                        "fields": fields_list,
                        "fuzziness": "AUTO",
                        "analyze_wildcard": True
                    }
                },
                "sort": [
                    {
                        "visits": {
                            "order": "desc"
                        }
                    }
                ],
                "size": output_size
            }
            #return jsonify(body)

    else:
        fields_list = [d_title, d_artist, d_lyrics, d_writer, d_music, d_genre]
        body = {
            "query": {
                "query_string": {
                    "query": input_query,
                    "type": "bool_prefix",
                    "fields": fields_list,
                }
            }
        }

    res = es.search(index="songs", doc_type="_doc", body=body)
    # print(res['hits']['hits'])

    return jsonify(res['hits']['hits'])
    # return "abc"

if __name__ == "__main__":
    app.run(debug=True)