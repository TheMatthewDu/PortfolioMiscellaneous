# U of T Course Recommender System

This program is a machine learning model that strives to find patterns within the Course Descriptions of courses 
offered by the Faculty of Applied Sciences and Engineering at the University of Toronto. 

## File Breakdown
A brief discussion of all the files and design decisions is presented below.

### read_uoft_descriptions.py
First, data is read from the [University of Toronto Faculty of Applied Science and Engineering Academic Calendar](https://engineering.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug) 
into a `.csv` file ([`UofT_descriptions.csv`](data/uoft_descriptions.csv)). The data is then filtered to UTF-8 standard and punctuations removed manually.

### generate_sparce.py
The text data is first filtered for frequent words (such as 'the' and 'and') and 50 random combinations of words are 
sampled and converted to a sparce matrix using a `CountVectorizer` from the `sklearn` library.

### naive_bayes.py
A Naive Bayes model with a Multinomial prior is fitted to the data. In this case, a generative model needed to be used,
as a discriminative model would not be able to find any patterns that would want, since it does not model the data 
explicitly. A multinomial prior is used as the input data is discrete and multivariable.

### evaluate.py
The top k values are printed for any input course, which presents the most similar courses.

## Next Steps
Further analysis of course information will involve getting more data from various other institutions to find trends in 
descriptions of curriculums to create an engineering-program-generator.

