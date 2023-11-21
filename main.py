import base64

import numpy as np

import BloomFilter as bf
import SiteKeywords as sk
import Links
import matplotlib.pyplot as plt
from io import BytesIO
from flask import Flask, render_template, request, Response
import pandas as pd

app = Flask(__name__)
data = pd.read_csv("../AgeDataset-V1.csv")
max_rows = max(data.axes[0])
max_columns = len(data.axes[1])
before_table_lab3 = data
before_table_lab3['Birth year'] = pd.to_numeric(before_table_lab3['Birth year'], errors='coerce')
before_table_lab3['Century'] = before_table_lab3['Birth year'].apply(
    lambda x: (x // 100) + 1 if not pd.isnull(x) else x)
after_table_lab3 = data


def checkArgs(arg):
    if arg is not None:
        return int(arg)
    else:
        return 0


def simple_ad(table, column_section, column_main):
    if column_section == 'Century' and column_main == "Occupation":
        return table.groupby(column_section)[column_main].count().agg(['min', 'max', 'mean']).reset_index()
    return table.groupby(column_section)[column_main].agg(['min', 'max', 'mean']).reset_index()


def generate_plot(kind, plot_data, first_column, second_column, title, x_label, y_label):
    info = simple_ad(plot_data, first_column, second_column)

    if first_column == "Occupation":
        info = info.head(10)
    if first_column == "Century" and second_column == "Occupation":
        ax = info.plot(kind=kind, x="index", title=title)
    elif first_column == "Gender":
        plt.boxplot([info['min'], info['max'], info['mean']], labels=['min', 'max', 'mean'])
    else:
        ax = info.plot(kind=kind, x=first_column, title=title)
        ax.set_xticklabels(info[first_column])
        ax.set_xticks(info.index)

    plt.tight_layout()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='upper right')
    plt.grid(True)
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return base64.b64encode(img.read()).decode()


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/lab1")
def lab1():
    info_table = pd.DataFrame({
        "Name": data.columns,
        "Type": data.dtypes,
        "EmptyCells": data.isna().sum().fillna(0).astype(int),
        "FilledCells": data.count()
    })

    row_from = checkArgs(request.args.get("row_from"))
    row_to = checkArgs(request.args.get("row_to"))
    column_from = checkArgs(request.args.get("column_from"))
    column_to = checkArgs(request.args.get("column_to"))

    result_table = pd.DataFrame(data.iloc[row_from:row_to + 1, column_from:column_to + 1])
    search_values = [("row_from", row_from), ("column_from", column_from), ("row_to", row_to), ("column_to", column_to)]

    return render_template("lab1.html",
                           max_rows=max_rows,
                           max_columns=max_columns,
                           info_table=info_table,
                           result_table=result_table,
                           search_values=search_values)


@app.route("/lab2")
def lab2():
    row_from = checkArgs(request.args.get("row_from"))
    row_to = checkArgs(request.args.get("row_to"))

    global ad_table
    ad_table = data.iloc[row_from:row_to, 0:10]
    ad_table['Birth year'] = pd.to_numeric(ad_table['Birth year'], errors='coerce')
    ad_table['Century'] = ad_table['Birth year'].apply(lambda x: (x // 100) + 1 if not pd.isnull(x) else x)

    first_ad = simple_ad(ad_table, 'Gender', 'Age of death')
    second_ad = simple_ad(ad_table, 'Occupation', 'Age of death')
    third_ad = simple_ad(ad_table, 'Occupation', 'Birth year')
    fourth_ad = simple_ad(ad_table, 'Century', 'Occupation')

    search_values = [("row_from", row_from), ("row_to", row_to)]

    return render_template("lab2.html",
                           max_rows=max_rows,
                           first_ad=first_ad,
                           second_ad=second_ad,
                           third_ad=third_ad,
                           fourth_ad=fourth_ad,
                           search_values=search_values)


@app.route("/lab3")
def lab3():
    extended_table = after_table_lab3
    if request.args.get("chart") is None:
        return render_template("lab3.html")
    params = {
        "first": ['Gender', 'Age of death'],
        "second": ['Occupation', 'Age of death'],
        "third": ['Occupation', 'Birth year'],
        "fourth": ['Century', 'Occupation'],
    }

    numeric_columns = ["Birth year", "Death year", "Age of death"]
    string_columns = ["Name", "Short description", "Gender", "Country", "Occupation", "Manner of death"]

    for i in data.columns:
        if i in numeric_columns:
            extended_table[i].fillna(data[i].mean(), inplace=True)
        elif i in string_columns:
            extended_table[i].fillna(data[i].mode().values[0], inplace=True)

    num_rows_to_add = int(len(data) * 0.1)

    new_row = {}
    for j in data.columns:
        if data[j].dtype in [int, float]:
            new_row[j] = data[j].mean()
        else:
            new_row[j] = data[j].mode().values[0]

    new_data = pd.DataFrame()
    for key, value in new_row.items():
        new_data[key] = [value] * num_rows_to_add
    extended_table = pd.concat([extended_table, new_data], ignore_index=True)

    extended_table['Birth year'] = pd.to_numeric(extended_table['Birth year'], errors='coerce')
    extended_table['Century'] = extended_table['Birth year'].apply(lambda x: (x // 100) + 1 if not pd.isnull(x) else x)

    plotbeforeurl = generate_plot("bar",
                                  before_table_lab3,
                                  params[str(request.args.get("chart"))][0],
                                  params[str(request.args.get("chart"))][1],
                                  "До",
                                  params[str(request.args.get("chart"))][0],
                                  params[str(request.args.get("chart"))][1], )

    plotafterurl = generate_plot("bar",
                                 extended_table,
                                 params[str(request.args.get("chart"))][0],
                                 params[str(request.args.get("chart"))][1],
                                 "После",
                                 params[str(request.args.get("chart"))][0],
                                 params[str(request.args.get("chart"))][1], )

    return render_template("lab3.html",
                           plot_before_url=plotbeforeurl,
                           plot_after_url=plotafterurl)


@app.route("/lab4")
def lab4():
    site_keywords = sk.SiteKeywords()
    num_of_links = len(Links.links)
    bloom_filter = bf.Bloomfilter(num_of_links * 10, num_of_links)
    keyword = request.args.get("search_keyword")
    sites = list()

    for i in Links.links:
        for j in i[1]:
            bloom_filter.add_to_filter(j.lower())
        site_keywords.add_keywords_for_site(i[0], [string.lower() for string in i[1]])

    if keyword is not None:
        if bloom_filter.check_is_in_filter(keyword.lower()):
            sites.extend(site_keywords.get_sites_for_keyword(keyword.lower()))

    return render_template("lab4.html",
                           sites=sites)


@app.route("/lab5")
def lab5():
    before_table_lab3["Age of death"].fillna(data["Age of death"].mean(), inplace=True)
    data_for_regression = before_table_lab3.groupby(["Century"])["Age of death"].agg('mean').reset_index()
    all_ages = list(map(int, data_for_regression["Age of death"]))
    all_centuries = list(map(int, data_for_regression["Century"]))

    max_age, min_age = max(all_ages), min(all_ages)
    #all_ages = [(i - min_age) / (max_age - min_age) for i in all_ages]

    age = all_ages[:len(all_ages) - int(len(all_ages) * 0.1)]
    century = all_centuries[:len(all_centuries) - int(len(all_centuries) * 0.1)]

    check_age = all_ages[len(all_ages) - int(len(all_ages) * 0.1):]
    check_century = all_centuries[len(all_centuries) - int(len(all_centuries) * 0.1):]

    plt.title('99% data')
    plt.plot(century, age, 'ro')
    b0, b1 = calc_coeff(century, age)
    plt.plot(century, do_predict(b0, b1, century))
    plt.text(min(century), max(age), f'y={b1:.4f}*x + {b0:.4f}', fontsize=20,
             bbox={'facecolor': 'yellow', 'alpha': 0.2})
    plt.tight_layout()
    plt.grid(True)
    img99 = BytesIO()
    plt.savefig(img99, format="png")
    img99.seek(0)
    plt.close()

    plt.title('1% data')
    plt.plot(check_century, check_age, 'ro')
    b0, b1 = calc_coeff(check_century, check_age)
    plt.plot(check_century, do_predict(b0, b1, check_century))
    plt.text(min(check_century), max(check_age), f'y={b1:.4f}*x + {b0:.4f}', fontsize=20,
             bbox={'facecolor': 'yellow', 'alpha': 0.2})
    plt.grid(True)
    img1 = BytesIO()
    plt.savefig(img1, format="png")
    img1.seek(0)
    plt.close()

    age_mean = sum(age) / len(age)
    ss_total = sum((i-age_mean)**2 for i in age)
    ss_residual = sum((i - age_predi)**2 for i, age_predi in zip(age, do_predict(b0, b1, check_century)))
    r = 1-(ss_residual/ss_total)

    return render_template("lab5.html",
                           r=r,
                           img1=base64.b64encode(img1.read()).decode(),
                           img99=base64.b64encode(img99.read()).decode())


def calc_coeff(x, y):
    a = len(y)
    b = sum(x)
    c = sum(y)
    d = sum([i * i for i in x])
    e = sum([x[i] * y[i] for i in range(len(y))])

    b1 = (a * e - c * b) / (a * d - b * b)
    b0 = (c - b1 * b) / a
    return b0, b1


def do_predict(b0, b1, x):
    y = [b1 * i + b0 for i in x]
    return y


if __name__ == "__main__":
    plt.switch_backend('agg')
    app.run(host="localhost", port=int("5000"))
