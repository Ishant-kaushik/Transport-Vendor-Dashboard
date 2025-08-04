import pandas as pd
import os
import base64
import io
from dash import Dash, dcc, html, dash_table, Output, Input, State
import plotly.express as px

app = Dash(__name__)
app.title = "Transport Vendor Dashboard"

def process_excel(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')

    # Clean and transform
    df.columns = df.columns.str.strip()
    df = df.astype(str).replace("nan", "Missing")

    # ----- Fleet Size by Company -----
    company_chart_data = df.groupby("Company name")["Vehicle No"].count().reset_index(name="Vehicle Count")
    company_fig = px.bar(
        company_chart_data.sort_values("Vehicle Count", ascending=False),
        x="Company name",
        y="Vehicle Count",
        title="Fleet Size by Company"
    )

    # ----- Fleet Size by Vendor Name -----
    vendor_chart_data = df.groupby("Name")["Vehicle No"].count().reset_index(name="Vehicle Count")
    vendor_fig = px.bar(
        vendor_chart_data.sort_values("Vehicle Count", ascending=False),
        x="Name",
        y="Vehicle Count",
        title="Fleet Size by Vendor"
    )

    # ----- Location Pie Chart -----
    location_fig = px.pie(df, names="Location", title="Vendor Distribution by Location", hole=0.4)

    # ----- Compliance -----
    compliance_columns = ["Name", "A/c", "IFSC Code", "Pan No"]
    compliance_df = df[compliance_columns].copy()
    compliance_df["Compliance"] = compliance_df.apply(
        lambda row: "✅" if all(val != "Missing" and val.strip() != "" for val in row[1:]) else "❌",
        axis=1
    )

    return df.to_dict('records'), company_fig, vendor_fig, location_fig, compliance_df.to_dict('records')


app.layout = html.Div([
    html.H1("🚚 Transport Vendor Dashboard", style={'textAlign': 'center'}),

    html.H2("📤 Upload Excel File"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select an Excel file (.xlsx)')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '10px'
        },
        accept=".xlsx",
        multiple=False
    ),

    html.Div(id='output-dash')
])

@app.callback(
    Output('output-dash', 'children'),
    Input('upload-data', 'contents')
)
def update_dashboard(contents):
    if contents is None:
        return html.Div("Please upload an Excel file to view the dashboard.")

    df_records, company_fig, vendor_fig, location_fig, compliance_records = process_excel(contents)

    return html.Div([
        html.H2("📋 Vendor Master Table"),
        dash_table.DataTable(
            data=df_records,
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
        ),

        html.Br(),

        dcc.Graph(figure=company_fig),
        dcc.Graph(figure=vendor_fig),
        dcc.Graph(figure=location_fig),

        html.H2("✅ Compliance Checker (A/c, IFSC, PAN)"),
        dash_table.DataTable(
            data=compliance_records,
            page_size=10,
            style_data_conditional=[
                {
                    'if': {'column_id': 'Compliance', 'filter_query': '{Compliance} = "❌"'},
                    'backgroundColor': '#FFCDD2',
                },
                {
                    'if': {'column_id': 'Compliance', 'filter_query': '{Compliance} = "✅"'},
                    'backgroundColor': '#C8E6C9',
                },
            ]
        )
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)

