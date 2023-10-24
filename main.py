from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('../AgeDataset-V1.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/table')
def table():
    data = pd.read_csv('../AgeDataset-V1.csv')

    max_rows = max(data.axes[0])
    max_columns = len(data.axes[1])

    info_df = pd.DataFrame({
        "Name": data.columns,
        "Type": data.dtypes,
        "EmptyCells": data.isna().sum().fillna(0).astype(int),
        "FilledCells": data.count()
    })

    row_from = request.args.get("row_from")
    row_to = request.args.get("row_to")
    column_from = request.args.get("column_from")
    column_to = request.args.get("column_to")

    if row_from is not None and row_to is not None and column_from is not None and column_to is not None:
        row_from = int(row_from)
        row_to = int(row_to)
        column_from = int(column_from)
        column_to = int(column_to)

        result_table = pd.DataFrame(data.iloc[row_from:row_to+1, column_from:column_to+1])
        ad_table = pd.DataFrame(data.iloc[row_from:row_to+1, 0:10])
        ad_table['Birth year'] = pd.to_numeric(ad_table['Birth year'], errors='coerce')
        ad_table['Century'] = ad_table['Birth year'].apply(lambda x: (x // 100) + 1 if not pd.isnull(x) else x)

        first_ad = simple_ad(ad_table, 'Gender', 'Age of death')
        second_ad = simple_ad(ad_table, 'Occupation', 'Age of death')
        third_ad = simple_ad(ad_table, 'Occupation', 'Birth year')
        fourth_ad = ad_table.groupby('Century')['Occupation'].count().agg(['min', 'max', 'mean']).reset_index()
    else:
        result_table = pd.DataFrame()
        first_ad = pd.DataFrame()
        second_ad = pd.DataFrame()
        third_ad = pd.DataFrame()
        fourth_ad = pd.DataFrame()

    search_values = [("row_from", row_from), ("column_from", column_from), ("row_to", row_to), ("column_to", column_to)]

    return render_template('table.html',
                           max_rows=max_rows,
                           max_columns=max_columns,
                           info_df=info_df,
                           result_table=result_table,
                           first_ad=first_ad,
                           second_ad=second_ad,
                           third_ad=third_ad,
                           fourth_ad=fourth_ad,
                           search_values=search_values)


def simple_ad(table, column_section, column_main):
    return table.groupby(column_section)[column_main].agg(['min', 'max', 'mean']).reset_index()


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
