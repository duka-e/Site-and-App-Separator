import streamlit as st
import pandas as pd
from io import BytesIO

st.write("A page to be used to separate a mixed list of sites and apps.")
label = "Please ensure the file you upload has two columns named as Name and Value, respectively."
type_file = ["csv", "xlsx"]
uploaded_file = st.file_uploader(label, type=type_file)

if uploaded_file is None:
    st.info("Please upload a file to continue.")
    st.stop()  

#if uploaded_file is not None:
df_file = pd.read_csv(uploaded_file)


st.write('**********************')

# Removing duplicates from the uploaded file and presenting a table of the clean full data to the user.
df_file = df_file.drop_duplicates()
count_full_data = df_file.shape[0]

st.write(f"Uploaded file contains {count_full_data} rows.")
st.write(df_file)


st.write('**********************')
# Identifying all the App IDs
df_file.loc[df_file['Value'].astype(str).str.strip().str.isnumeric(), 'Type'] = 'App ID' 

count_ids = df_file[df_file['Type']=='App ID'].shape[0]
st.write(f"1. Count of app IDs: {count_ids}")
st.dataframe(df_file[df_file['Type']=='App ID'])


st.write('**********************')
#After identifying the App IDs, the remaining values are site URLs and app bundles. All values that have a corresponding Name, are app bundles so these will be assigned as such. Site URLs do not have corresponding names.
df_file.loc[(df_file['Type'].isna()) & (df_file['Name'].notna()), 'Type'] = 'App Bundle'


# However not all app bundles will have a corresponding name. So the remaning values with an unclassified type are site URLs and app bunldes that did not have a corresponding name.

# The below is a tuple of common top level domains. This will be used to identify sites since app bundles will not end with a TLD. 
tlds = ('.com', '.org', '.net', '.edu', '.gov', '.io','.co', '.uk', '.gg', '.nl', '.fr', '.be', '.eu', '.de', '.tv', '.pl', '.ch', '.se', '.sk', '.ie', '.cz', '.ro', '.eus', '.it', '.al', '.at', '.bg', '.dk', '.hu', '.lu', '.gr', '.no', '.pt', '.rs', '.ru', 'si', '.tr', '.ua', '.us', '.hn', '.live', '.vn', '.la', '.es', '.news', '.info', '.pro', '.media', '.fm', '.il', '.fi', '.mx', '.fm', '.lt', '.jp', '.in', '.to', '.hr', '.me', '.lol', '.cat', '.ba', '.ng', '.site', '.ms', '.ca', '.pk', '.video', '.sport', '.scot', '.page', '.ws', '.is', '.cc', '.im', '.lv', '.yt', '.cv', '.biz', '.wiki', '.za', '.nu', '.cl', '.su', '.ee', '.sg', '.id', '.th', '.gl', 'ug', '.ls')

df_file.loc[df_file['Type'].isna(), 'Type'] = df_file['Value'].apply(lambda x: 'Site' if str(x).lower().endswith(tlds) else 'Bundles plus Unknowns')

count_sites = df_file[df_file['Type']=='Site'].shape[0]
st.write(f'2. Count of sites: {count_sites}')
st.dataframe(df_file[df_file['Type']=='Site'])



st.write('**********************')
# The reason why I have used the classification 'Bundles plus Unknowns' is because sometimes values do not follow the URL or app bundle format. Any Values that get labelled as unknown will need to be reviewed manually to decide whether it is a site or app.

# App bundles that follow the reserve-domain naming format will have at least one dot (.) in their name. Any values without a dot, is not following the standard format and is labelled as unknown. 
df_file.loc[(df_file['Type']=='Bundles plus Unknowns') & (~df_file['Value'].str.contains(r'\.')), 'Type'] = 'Unknown'

# After assigning the Unknown values, I can now reassign the remaining app bundles to the category 'App Bundle' so that to bring together this batch of app bundles with the initial batch of app bundles identified by filtering by app name. 
df_file.loc[(df_file['Type']=='Bundles plus Unknowns'), 'Type'] = 'App Bundle'
count_app_bundles = df_file[df_file['Type']=='App Bundle'].shape[0]
st.write(f'3. Count of app bundles: {count_app_bundles}')
st.dataframe(df_file[df_file['Type']=='App Bundle'])



st.write('**********************')
# Presenting the values classified as unknown.
count_unknowns = df_file[df_file['Type']=='Unknown'].shape[0]
st.write(f'4. Count of unknown values: {count_unknowns}')
st.dataframe(df_file[df_file['Type']=='Unknown'])


st.write('**********************')
# This is to export the final dataframe as an excel file where each type is separated into different sheets.
output = BytesIO()

with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    for type_name, group in df_file.groupby("Type"):
        group.to_excel(writer, sheet_name=type_name, index=False)

output.seek(0)

st.write('Download an Excel file with separated sheets for App ID, App Bundle, Site and Unknown values.')
st.download_button(
    label="Download here",
    data=output,
    file_name="data_by_type.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
