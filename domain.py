import pandas as pd
import streamlit as st
import re

st.title('Extract domain name from URLs')


def is_url(text):
    pattern = re.compile(r'^(https?://|www)(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return bool(re.match(pattern, text))


def extract_domain(url):
    if url.startswith('http'):
        start = url.find("//") + 2
        end = url.find("/", start)
        if end == -1:
            domain = url[start:]
        else:
            domain = url[start:end]
    # domain = url[start + 2:end] if end != -1 else url[start + 2:]

    elif url.startswith('www'):
        end = url.find('/')
        if end == -1:
            domain = url
        else:
            domain = url[:end + 1]
        # domain = url[:end] if end !=-1 else url
    else:
        start = url.find('/')
        if start == -1:
            domain = url
        else:
            domain = url[:start]

    if 'www' in domain:
        domain = domain[4:]
    return domain


# Define a function to apply styling
def color_cells(value):
    if value == 'Enter url in proper format':
        return 'background-color: yellow'
    else:
        return ''


# url = st.text_input('Enter Url:')
# if url:
#    st.write("Domain: ", extract_domain(url))

grp = st.text_area("Enter a list of URLs  (separated by spaces):")

lst = grp.split()
df = pd.DataFrame(lst, columns=["URL"])

temp = []

for row in df['URL']:
    if is_url(row):
        temp.append(extract_domain(row))
    else:
        temp.append('Enter url in proper format')
df['domain'] = temp

csv = df.to_csv().encode('utf-8')
# style_df = df.style.applymap(color_cells)

if grp:
    st.write(df)
    st.download_button('Download file', data=csv, file_name="domains.csv", mime='text/csv')

st.write('#### OR')
file = st.file_uploader('Upload URLs csv file with one column', type='csv')

if file:
    df2 = pd.read_csv(file)
    t2 = []
    for row in df2.iloc[:, 0]:
        if is_url(row):
            t2.append(extract_domain(row))
        else:
            t2.append('Enter url in proper format')
    df2['domain'] = t2
    style_df2 = df2.style.applymap(color_cells)
    csv2 = df2.to_csv().encode('utf-8')
    st.write(style_df2)
    st.download_button('Download file', data=csv2, file_name="domains.csv", mime='text/csv')
