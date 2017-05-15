DEEP MEME
=========

```
Picture + Text == Meme -> Text2
```

Super credits to https://github.com/lilleswing/memegen for the base of this project, and [evq](https://github.com/evq) for contributing the OpenCV code!

Dependencies
============

- libsqlite3-dev
- libjpeg8-dev
- opencv3
- tesseract

pip packages:
- pillow
- flask
- pysqlite

To run:
```bash
python memegen.py
```

Features
========
* New Image Template Upload
* Creates static links for all memes generated

How It Works
============

Memegen stores all images on the local file system in the static/images and static/memes folders.  memegen.db is a sqlite3 database that keeps track of all the files in these folders.

Memegen uses PIL (Python Image Library) to write text on images.

