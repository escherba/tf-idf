tf-idf
======

Experiments with TF-IDF and Dickens

Most TF-IDF projects expect you to give them a list of documents. 
This one will process a *single* document and it will output
a list of five most important words under each paragraph, like so:

    A large cask of wine had been dropped and broken, in the street. The
    accident had happened in getting it out of a cart; the cask had tumbled
    out with a run, the hoops had burst, and it lay on the stones just
    outside the door of the wine-shop, shattered like a walnut-shell.

    {cask:0.245, walnut:0.148, shell:0.148, hoops:0.148, tumbled:0.135}
