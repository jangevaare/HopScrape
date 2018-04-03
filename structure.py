import pandas as pd

if __name__ == '__main__':
    raw_hops = pd.read_csv('raw_hops.csv')
    properties = set(raw_hops.Property)
    structured_hops = raw_hops[raw_hops.Property == 'Description'][['Hop', 'Origin']]
    for i in properties:
        single_property = raw_hops[raw_hops.Property == i][['Hop', 'Origin', 'Value']]
        single_property = single_property.rename(columns={'Value': i})
        structured_hops = structured_hops.merge(single_property, how='outer', on=['Hop', 'Origin'])

    structured_hops.to_csv('structured_hops.csv')
