from flask import Flask, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

def find_matching_pairs(html):
    soup = BeautifulSoup(html, 'html.parser')
    matching_pairs = ['b', 'i', 'p', 'h1']
    elements_within_pairs = []

    for tag in matching_pairs:
        opening_tags = soup.find_all(tag)
        for opening_tag in opening_tags:
            closing_tag = opening_tag.find_next_sibling(f'/{tag}')
            if closing_tag:
                element = str(opening_tag) + opening_tag.get_text() + str(closing_tag)
                elements_within_pairs.append(element)

    return elements_within_pairs

def remove_matching_pairs(html):
    soup = BeautifulSoup(html, 'html.parser')
    matching_pairs = ['b', 'i', 'p', 'h1']

    for tag in matching_pairs:
        opening_tags = soup.find_all(tag)
        for opening_tag in opening_tags:
            closing_tag = opening_tag.find_next_sibling(f'/{tag}')
            if closing_tag:
                opening_tag.extract()
                closing_tag.extract()

    return str(soup)

@app.route('/', methods=['GET', 'POST'])
def process_html():
    if request.method == 'POST':
        html = request.form['html']
        elements_within_pairs = find_matching_pairs(html)
        html_without_pairs = remove_matching_pairs(html)  
        return render_template('result.html', elements_within_pairs=elements_within_pairs, html_without_pairs=html_without_pairs)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
