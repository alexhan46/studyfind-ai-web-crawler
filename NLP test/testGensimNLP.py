from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords


text1 = """Sleep is a key factor in a person's health, and we actually spend one third of our lives sleeping. 
The latest figures show a prevalence of insomnia in 20-30\% of French adults. Sleep disorders are a growing public health concern.
Treatment for insomnia is often some form of drugs; however, the side effects of these treatments (sedatives, hypnotics or 
anti-anxiety medications) are significant. Non drug-treatments like music therapy are growing in popularity. 
The objective of this study is to demonstrate the effectiveness of musical interventions on sleep disorders in general population.
It is a prospective, multicentered, double-blind, randomized comparative intervention study, comparing 3 parallel patient groups. 
Patients included in this study will be selected by their physicians according to the severity of their disorders. 
Enrollment period will last for 2 months and the study will last 3 months. The primary outcome (score on Pittsburgh Sleep Quality Index, PSQI) 
is a discrete quantitative variable. The statistical tests used will concern the comparison of the average deltas of each group by using analysis
 of variance (ANOVA). The selected alpha risk, or Type 1 error, is 5%.
The results expected in this study are a significant decrease in Pittsburgh scale scores in the music intervention group. 
The decrease in Pittsburgh scale scores should be compared to the results from this study: Qun Wang and Al; 
The Effects of Music Intervention on Sleep Quality in Community-Dwelling Elderly, The Journal of Alternative and Complementary Medicine, 2016. In this 3-month study, the average change compared to the baseline is 6.44 in the musical intervention group and 3.28 in the control group. The pooled standard deviation is estimated to be 3.53.
Musical intervention is non-invasive, so it's a low-risk therapeutic tool for general practice that may be useful in the management of sleep disorders. Its effectiveness, if demonstrated, could lead to new recommendations for the treatment of sleep disorders, and reduce the use of medication such as sedatives and hypnotics."""

print(summarize(text1, ratio=0.2))
# print(summarize(text1, split=True, ratio=0.5))
print("------------------------------------------------------------------------------------------------------------------------------")
print(keywords(text1, words=1).split('\n'))

# ALL options available in gensim
    # keywords(text1, ratio=0.2, words=None, split=False, scores=False, pos_filter=('NN', 'JJ'), lemmatize=False, deacc=True)
    #     text (str) – Input text.
    #     ratio (float, optional) – If no “words” option is selected, the number of sentences is reduced by the provided ratio, else, the ratio is ignored.
    #     words (int, optional) – Number of returned words.
    #     split (bool, optional) – Whether split keywords if True.
    #     scores (bool, optional) – Whether score of keyword.
    #     pos_filter (tuple, optional) – Part of speech filters.
    #     lemmatize (bool, optional) – If True - lemmatize words.
    #     deacc (bool, optional) – If True - remove accentuation