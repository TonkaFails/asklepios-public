# Hierarchical BERT
A challenge of this project is the alternating, almost open end size of PDFs.
That means we need a strategy to generate embedings while keeping the usual max token length of 512. (up to 4096 is possible, around 3000 words)

This paper from 2022 proposes using a hierarchical BERT model that splits the text into regions managed by a BERT model while also using a global BERT model that composes the information.

see: paper-hierarchical-bert.pdf