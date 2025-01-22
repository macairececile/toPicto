# script to visualize the pictograms linked to each json entry in an html file.
# To run the script, you need to install the following library:
import json
from argparse import RawTextHelpFormatter, ArgumentParser


def read_json_file(json_file):
    """
        Read the json file.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    ids = [d['id'] for d in data]
    srcs = [d['src'] for d in data]
    pictos = [d['pictos'] for d in data]
    tgts = [d['tgt'] for d in data]
    return ids, srcs, pictos, tgts


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


def write_html_file(html_file, ids, srcs, pictos, tgts):
    """
        Add to the html file the information of each json entry.
    """
    for i, j in enumerate(ids):
        html_file.write("<div class=\"shadow p-3 mb-5 bg-white rounded\">")
        write_header_info_per_sentence(html_file, "ID: " + j)
        write_header_info_per_sentence(html_file, "Src: " + srcs[i])
        if len(tgts[i].split(' ')) == len(pictos[i]):
            html_file.write("<div class=\"container-fluid\">")
            for a, p in enumerate(pictos[i]):
                html_file.write(
                    "<span style=\"color: #000080;\"><strong><figure class=\"figure\">"
                    "<img src=\"https://static.arasaac.org/pictograms/" + str(p) + "/" + str(
                        p) + "_500.png" + "\"alt=\"\" width=\"110\" height=\"110\" />"
                                          "<figcaption class=\"figure-caption text-center\">" +
                    tgts[i].split(' ')[a] + "</figcaption></figure></strong>")
            html_file.write("</div>")
        html_file.write("</div>")


def html_file(html_file, ids, srcs, pictos, tgts):
    """
        Create the html file.
    """
    html = create_html_file(html_file)
    html.write("<div class = \"container-fluid\">")
    write_html_file(html, ids, srcs, pictos, tgts)
    html.write("</div></body></html>")
    html.close()


def generate_html_file_from_json(args):
    """
        Generate a html file to visualize the pictogram sequence of each json entry.
    """
    ids, srcs, pictos, tgts = read_json_file(args.json)
    name_html = args.json.split('.json')[0] + ".html"
    html_file(name_html, ids, srcs, pictos, tgts)


parser = ArgumentParser(description="Visualize the sequence of pictogram from the json file in a html file.",
                        formatter_class=RawTextHelpFormatter)
parser.add_argument('--json', type=str, required=True,
                    help="")
parser.set_defaults(func=generate_html_file_from_json)
args = parser.parse_args()
args.func(args)
