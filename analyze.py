import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scopus_merged_2016-2026_merged.csv")


### pubs per year
pubs_per_year = df.groupby('Year').size()
plt.figure()
pubs_per_year.plot(kind='line',marker='o',
                   title="Eye-Tracking publications per year (2016-2026)")
plt.xlabel('Year')
plt.ylabel('number of papers:')
plt.tight_layout()
plt.show()

## auto classify domains  
domain_keywords = {
    'Software Engineering': ['software', 'program', 'programming',
                             'coder', 'coding', 'debug', 'code review'],
    'Driving / Automotive': ['driver', 'driving', 'vehicle',
                             'car', 'road', 'traffic'],
    'Movies / Media'     : ['movie', 'film', 'screen',
                             'cinema', 'watching video', 'tv'],
    'Gaming / VR'        : ['game', 'gaming', 'video game',
                             'vr', 'virtual reality'],
    'Education / Learning': ['student', 'learning', 'reading',
                             'teaching', 'classroom', 'education'],
    'Medical'            : ['surgery', 'patient', 'medical',
                             'diagnosis', 'surgical']
}
def classify_domain(row):
    text = f"{row['Title']} {row.get('Abstract', '')}".lower()
    for dom, kws in domain_keywords.items():
        if any(kw in text for kw in kws):
            return dom
    return 'Other'

df['Domain'] = df.apply(classify_domain,axis=1)

domain_counts = df['Domain'].value_counts()
plt.figure()
domain_counts.plot(kind='bar', title='papers by application domain')
plt.ylabel('number of papers')
plt.tight_layout()
plt.show()

swe_df = df[df['Domain'] == 'Software Engineering']
swe_df.to_csv('Domain.csv', index=False)

