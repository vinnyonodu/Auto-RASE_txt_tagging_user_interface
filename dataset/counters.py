from bs4 import BeautifulSoup


def count_in_html():
    array = ["a.html", "b.html", "c.html", "d.html", "e.html", "f.html", "g.html", "h.html", "i.html", "j.html",
             "k.html",
             "l.html", "m.html", "n.html", "o.html", "p.html", "q.html", "r.html", "s.html", "t.html", "u.html",
             "v.html",
             "w.html", "x.html", "y.html"]
    counts_for_rasetypes = {}

    for i, file in enumerate(array):
        with open(file) as f:
            soup = BeautifulSoup(f, "html.parser")

        tags = soup.find_all(lambda tag: tag.has_attr('data-rasetype'))

        for tag in tags:
            rasetype = tag["data-rasetype"]
            if rasetype not in counts_for_rasetypes:
                counts_for_rasetypes[rasetype] = 1
            counts_for_rasetypes[rasetype] += 1

    # sort it by value
    counts_for_rasetypes = {k: v for k, v in
                            sorted(counts_for_rasetypes.items(), key=lambda item: item[1], reverse=True)}
    print(counts_for_rasetypes)


def count_for_flair():
    files = ["train.txt", "dev.txt", "test.txt"]

    counts_for_rasetypes = {}

    for file in files:

        with open(file) as f:
            lines = f.readlines()

        for line in lines:
            try:
                label = line.split(" ")[1]
                if label not in counts_for_rasetypes:
                    counts_for_rasetypes[label] = 1
                counts_for_rasetypes[label] += 1
            except:
                pass

    # sort it by value
    counts_for_rasetypes = {k: v for k, v in
                            sorted(counts_for_rasetypes.items(), key=lambda item: item[1], reverse=True)}
    print(counts_for_rasetypes)


count_for_flair()
count_in_html()
