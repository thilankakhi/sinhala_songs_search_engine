# Sinhala Songs Search Engine

This project is a web application search engine for the Sinhala songs which is based on the elastic search. Users are allowed to search for Sinhala songs by querying in Sinhala Language.
Metadata of a song - title, lyrics, artist, writer, genre, visits and musician

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Folder Structure

```
.
+-- search_app - Flask application
+-- songs_corpus - 
|   +-- sinhala_songs.json - songs corpus immediately after scraping
|   +-- sinhala_songs-processed.csv - translated songs corpus
|   +-- sinhalaTranslation.py - python file for translate English metadata to Sinhala
+-- songs_scrapping - scrapy project to scrape website for songs data
```

### Dataset

The sinhala songs dataset is created by scraping [SinhalaSongBook](https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/) website using scrapy web-crawling framework.

### Prerequisites

The following softwares/libraries should be installed before running the application

* [Elasticsearch 7.8](http://www.dropwizard.io/1.0.2/docs/)

### Installing

A step by step series of examples that tell you how to get a development env running

1. Get elasticsearch server up and running.

2. Install [ICU Analysis](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html) plugin.

3. Ceate 'songs' index in elasticsearch using `settings.json` in `search_app` folder as the body.

```
PUT <elsticsearch-host: port>/songs
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "names-analyser-si": {
          "type": "custom",
          "tokenizer": "icu_tokenizer",
          "char_filter": ["punctuation_char_filter"],
          "filter": ["edge_n_gram_filter"]
        },
        "lyrics-analyser-si": {
          "type": "custom",
          "tokenizer": "icu_tokenizer"
        },
        "names-search-analyser-si": {
          "type": "custom",
          "tokenizer": "icu_tokenizer",
          "char_filter": ["punctuation_char_filter"],
          "filter": ["sinhala_stop_filter"]
        }
      },
      "char_filter": {
        "punctuation_char_filter": {
          "type": "mapping",
          "mappings": [
            ".=>\\u0020",
            "|=>",
            "-=>",
            "_=>",
            "'=>",
            "/=>",
            ",=>\\u0020"
          ]
        }
      },
      "filter": {
        "edge_n_gram_filter": {
          "type": "edge_ngram",
          "min_gram": "2",
          "max_gram": "10"
        },
        "sinhala_stop_filter": {
          "type": "stop",
          "stopwords": [
            "සහ",
            "හා",
            "වැනි",
            "සේ",
            "‌මෙන්",
            "සමග",
            "කල",
            "කළ",
            "කරපු",
            "කරන"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "song_id": {
        "type": "integer"
      },
      "title": {
        "type": "text",
        "analyzer": "names-analyser-si",
        "search_analyzer": "names-search-analyser-si"
      },
      "artist": {
        "type": "text",
        "analyzer": "names-analyser-si",
        "search_analyzer": "names-search-analyser-si"
      },
      "genre": {
        "type": "text",
        "analyzer": "names-analyser-si",
        "search_analyzer": "names-search-analyser-si"
      },
      "writer": {
        "type": "text",
        "analyzer": "names-analyser-si",
        "search_analyzer": "names-search-analyser-si"
      },
      "music": {
        "type": "text",
        "analyzer": "names-analyser-si",
        "search_analyzer": "names-search-analyser-si"
      },
      "visits": {
        "type": "integer",
        "index": false
      },
      "lyrics": {
        "type": "text",
        "analyzer": "lyrics-analyser-si"
      }
    }
  }
}
```


3. Install `pip` dependencies and start python server by running the following command in the root directory of the project

```
cd ./search-application
pip install -r requirements.txt
python ./app.py
```
4. Insert songs data into `songs` index by sending the following command to the python server
```
POST http:\\localhost:5000\insert_data
```
5. Navigate to `http:\\localhost:5000` to view the search application interface

6. This application allows users to search following queries.

   *  Using the titile or the lyrics
   ```
    ආලෝකේ පතූරා, දිනෙක මේ නදී
   ```
   *  Using artist, musician or writer
   ```
    ක්ලැරන්ස් විජේවර්ධන සංගීතවත් කල ගීත
   ```
   *  Using the words "ජනප්‍රිය", "ප්‍රසිද්ධ", "හොඳම"
   ```
    හොඳම ගීත 5
   ```
   *  Using artist, musician or writer with the key words "ජනප්‍රිය", "ප්‍රසිද්ධ", "හොඳම"
   ```
    ක්ලැරන්ස් විජේවර්ධන සංගීතවත් කල ජනප්‍රිය ගීත 5
   ```

## Authors

* **Isuri Thilanka** - *Initial work* - [GithubProfile](https://github.com/thilankakhi)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
