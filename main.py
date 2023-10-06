from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('../AgeDataset-V1.csv')
df.to_csv('../AgeDataset-V1.csv', index=None)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/table')
def table():
    data = pd.read_csv('../AgeDataset-V1.csv')

    max_rows = max(data.axes[0])
    max_columns = len(data.axes[1])
    empty_cells = data.isna().sum().sum()
    filled_cells = data.count().sum()

    info_df = pd.DataFrame({
        "Название столбца": data.columns,
        "Тип данных": data.dtypes,
    })

    if request.args.get("row_from") is None:
        return render_template('table.html',
                               max_rows=max_rows,
                               max_columns=max_columns,
                               info_df=info_df,
                               empty_cells=empty_cells,
                               filled_cells=filled_cells)

    row_from = 1 if request.args.get("row_from") is None else int(request.args.get("row_from")) - 1
    row_to = 1 if request.args.get("row_to") is None else int(request.args.get("row_to"))
    column_from = 1 if request.args.get("column_from") is None else int(request.args.get("column_from")) - 1
    column_to = 1 if request.args.get("column_to") is None else int(request.args.get("column_to"))

    result_table = data.iloc[row_from:row_to, column_from:column_to]
    result_table['Birth year'] = pd.to_numeric(result_table['Birth year'], errors='coerce')
    result_table['Century'] = result_table['Birth year'].apply(lambda x: (x // 100) + 1 if not pd.isnull(x) else x)

    first_ad = simple_ad(result_table, 'Gender', 'Age of death')
    second_ad = simple_ad(result_table, 'Occupation', 'Age of death')
    third_ad = simple_ad(result_table, 'Occupation', 'Birth year')
    fourth_ad = result_table.groupby('Century')['Occupation'].count().agg(['min', 'max', 'mean']).reset_index()



    return render_template('table.html',
                           first_ad=first_ad.to_html(),
                           second_ad=second_ad.to_html(),
                           third_ad=third_ad.to_html(),
                           fourth_ad=fourth_ad.to_html(),
                           tables=[result_table.to_html()],
                           titles=[''],
                           max_rows=max_rows,
                           info_df=info_df,
                           max_columns=max_columns,
                           empty_cells=empty_cells,
                           filled_cells=filled_cells)


def simple_ad(table, column_section, column_main):
    return table.groupby(column_section)[column_main].agg(['min', 'max', 'mean']).reset_index()

if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
