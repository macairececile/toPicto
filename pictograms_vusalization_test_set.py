# script to visualize the pictograms linked to each json entry in an html file.
# To run the script, you need to install the following library:
import json
from argparse import RawTextHelpFormatter, ArgumentParser
import pandas as pd


def read_json_file(json_file):
    """
        Read the json file.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    ids = [d['id'] for d in data]
    hyps = [d['hyp'] for d in data]
    return ids, hyps


def read_lexicon(lexicon):
    """
        Read the lexicon and process it.
    """
    df = pd.read_csv(lexicon, sep='\t')
    df.loc[:, 'keyword_no_cat'] = df['lemma'].apply(lambda a: "_".join(str(a).split(' #')[0].strip().split(" ")))
    return df


def get_id_picto_from_predicted_lemma(df_lexicon, lemma):
    """
        Get the pictogram id from the predicted keyword.
    """
    id_picto = df_lexicon.loc[df_lexicon['keyword_no_cat'] == lemma, "id_picto"].tolist()
    return (id_picto[0], lemma) if id_picto else (0, lemma)


def get_pictos_from_hyp(hyps, lexicon):
    """
        Get the pictogram id sequence from the hypothesis.
    """
    pictos = []
    for h in hyps:
        tokens = h.split(" ")
        pictos.append([get_id_picto_from_predicted_lemma(lexicon, t) for t in tokens])
    return pictos


def create_html_file(html_file):
    """
        Create the header of the html file.
    """
    header = "<!doctype html>" \
             "<html lang=\"fr\"><head>" \
             "<meta charset=\"utf-8\">" \
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">" \
             "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css\" integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\" crossorigin=\"anonymous\">" \
             "</head>" \
             "<body>"
    f = open(html_file, 'w')
    f.write(header)
    return f


def write_header_info_per_sentence(html_file, utt_name):
    """
        Write the content of the header for each json entry.
    """
    html_file.write("<div class=\"container-fluid\">")
    html_file.write("<div class=\"row\">")
    html_file.write("<div class=\"col-12\"><div class=\"p-2\">")
    html_file.write(utt_name)
    html_file.write("</div></div></div></div>")


def write_html_file(html_file, ids, pictos):
    """
        Add to the html file the information of each json entry.
    """
    for i, j in enumerate(ids):
        html_file.write("<div class=\"shadow p-3 mb-5 bg-white rounded\">")
        write_header_info_per_sentence(html_file, "ID: " + j)
        html_file.write("<div class=\"container-fluid\">")
        for p in pictos[i]:
            if p[0] == 0:  # if the keyword is linked to no pictogram
                html_file.write(
                    "<span style=\"color: #000080;\"><strong><figure class=\"figure\">"
                    "<img src=\"data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" + "\"alt=\"\" width=\"110\" height=\"110\" />"
                                                                                              "<figcaption class=\"figure-caption text-center\">" +
                    p[1] + "</figcaption></figure></strong>")
            else:
                html_file.write(
                    "<span style=\"color: #000080;\"><strong><figure class=\"figure\">"
                    "<img src=\"https://static.arasaac.org/pictograms/" + str(p[0]) + "/" + str(
                        p[0]) + "_500.png" + "\"alt=\"\" width=\"110\" height=\"110\" />"
                                             "<figcaption class=\"figure-caption text-center\">" +
                    p[1] + "</figcaption></figure></strong>")
        html_file.write("</div>")
        html_file.write("</div>")


def html_file(html_file, ids, pictos):
    """
        Create the html file.
    """
    html = create_html_file(html_file)
    html.write("<div class = \"container-fluid\">")
    write_html_file(html, ids, pictos)
    html.write("</div></body></html>")
    html.close()


def generate_html_file_from_json(args):
    """
        Generate a html file to visualize the pictogram sequence of each json entry.
    """
    ids, hyps = read_json_file(args.json)
    lexicon_data = read_lexicon(args.lexicon)
    pictos = get_pictos_from_hyp(hyps, lexicon_data)
    name_html = args.json.split('.json')[0] + ".html"
    html_file(name_html, ids, pictos)


parser = ArgumentParser(description="Visualize the sequence of pictogram from the hyp json file in a html file.",
                        formatter_class=RawTextHelpFormatter)
parser.add_argument('--json', type=str, required=True,
                    help="")
parser.add_argument('--lexicon', type=str, required=True,
                    help="")
parser.set_defaults(func=generate_html_file_from_json)
args = parser.parse_args()
args.func(args)
