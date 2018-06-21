# PIIA - Person Identification in the Internet Archive
This is the official GitHub page for the paper:

> Eric Müller-Budack, Kader Pustu-Iren, Sebastian Diering and Ralph Ewerth:
"Finding Person Relations in Image Data of News Collections in the Internet Archive."
Submitted and Accepted in: *22nd International Conference on Theory and Practice of Digital Libraries (TPDL).* 2018.

# Person Dictionary

The list of entities in the person dictionary which are identified in the news articles of the *Internet Archive* is given in:
* Actors: top_100_tv_actors.csv
* Politicians: top_100_politicians.csv

# Demo

A demo of the retrieved results can be found on:
https://tib-visual-analytics.github.io/PIIA/

The demo was successfully tested with recent versions of:
* Microsoft Edge
* Mozilla Firefox
* Google Chrome (Chromium)

Please note, that Microsoft Internet Explorer is currently not supported.

# Model

The ResNet-101 model was trained using TensorFlow on the MS-Celeb-1M dataset and can be found here:

https://github.com/TIB-Visual-Analytics/PIIA/releases/download/untagged-16fde96f569b77f5dfb7/model.tar.gz

We are currently working on a deploy source code.

# LICENSE

This work is published under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007. For details please check the LICENSE file in the repository.
