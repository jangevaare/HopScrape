import pandas as pd
import numpy as np

if __name__ == '__main__':
    structured_hops = pd.read_csv('structured_hops.csv')
    cleaned_hops = structured_hops[['Hop', 'Origin', 'Description']]

    oils = ['Alpha Acid', 'Beta Acid', 'Myrcene', 'Farnesene', 'Geraniol', 'Caryophyllene', 'Humulene', 'Co-humulone', 'Linalool', 'B-Pinene']

    for j in oils:
        cleaned_hops.loc[:, '%s_lpct' % j] = np.nan
        cleaned_hops.loc[:, '%s_lpct' % j] = np.nan
        for i in range(0, len(cleaned_hops), 1):
            if structured_hops.notna().loc[i, '%s' % j]:
                if structured_hops.loc[i, '%s' % j] == "< 1.0% of total oil":
                    try:
                        cleaned_hops.loc[i, '%s_lpct' % j] = 0.0
                        cleaned_hops.loc[i, '%s_upct' % j] = 1.0
                    except:
                        pass
                else:
                    try:
                        cleaned_hops.loc[i, '%s_lpct' % j] = float(structured_hops.loc[i, '%s' % j].split(" - ")[0])
                        cleaned_hops.loc[i, '%s_upct' % j] = float(structured_hops.loc[i, '%s' % j].split(" - ")[1].split("%")[0])
                    except:
                        pass

    cleaned_hops.loc[:, 'total_lpct'] = np.nan
    cleaned_hops.loc[:, 'total_upct'] = np.nan
    for i in range(0, len(cleaned_hops), 1):
        if structured_hops.notna().loc[i, 'Total Oil']:
            cleaned_hops.loc[i, 'total_lpct'] = float(structured_hops.loc[i, 'Total Oil'].split(" - ")[0])
            cleaned_hops.loc[i, 'total_upct'] = float(structured_hops.loc[i, 'Total Oil'].split(" - ")[1].split(" mL/100g")[0])

    cleaned_hops.to_csv('cleaned_hops.csv')
