# Melody Analysis and Harmony Generation

I worked with [Dr. Kurt Stallmann](http://www.kurtstallmann.com) at Rice
University to determine the key of a piece of music *given only its melodic
line* as well as generating a complementary harmonic progression. This is a
tricky task to do automatically because:

* Only half of the information regarding the piece is given,
* Different melodies carry different types/amounts of information,
* Often the harmony is very crucial in establishing the key of a piece.

We define **consonance** and **scale membership** correlations to select the
best key for an input score. We then use those same correlations along with
a limited key set (due to the new knowledge of the supposed key) to generate
the complementary harmonic progression.

**Citation**: Sen, O. and Stallmann, K. Analysis of Melody Through Key
Definition and Generation of Complementary Harmonies. Rice Undergraduate
Research Symposium. Houston, TX, April 13, 2012.

**Downloads**:

* [Paper](/research/2012rurs-music/2012rurs-music-paper.pdf)
* [Poster at RURS 2012](/research/2012rurs-music/2012rurs-music_poster.pdf)
