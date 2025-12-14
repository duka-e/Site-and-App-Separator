# Site-and-App-Separator

- To access the Streamlit app: https://site-and-app-separator.streamlit.app/
- **To test the tool, please download use the csv file called 'Mixed sites and apps list' in the repo.** 

This is a web application that automatically classifies a mixed list of websites and mobile app identifiers into:

- Website URLs 
- iOS App IDs (numeric)
- App bundle identifiers
- Unknown values (anything that doesn't follow the format of a website or app bundle) 

The tool is designed to assist in digital marketing where it is important to identify the environment (site/app) in which ads are going to run. When planning campaigns, it is common for a Supply Side Platform partner to provide a list of potential sites and apps for running your campaigns. However, it is also common to receive this as a mixed list of site URLs and app IDs & bundles. The aim of this Streamlit tool is to make this separation process more efficient (and save time) by using a Python script as compared to filtering, cleaning, and applying formulas in Excel. After separating each type, the user will be able to download an Excel file containing the different types separated by sheet.

---

## Features

- Upload or paste a dataset containing mixed identifiers
- Cleans the dataset by removing duplicates
- Automatically detects and classifies into Site, App ID, App Bundle, or Unkown:
- Preserves all original columns and adds a classification column
- Simple and interactive Streamlit interface

---

## Classification Logic

The app relies on Pandas to classify the below:

1. **App Store ID**
   - Values containing only digits (e.g. `1454538656`)
2. **Site URL** 
   - Values identified by cross-referencing to a tuple of common top-level domains (TLD) 
3. **App Bundle**
   - Identified as any values that do not end in TLD and after isolating any special cases (labelled as Unknowns) that do not follow the format of an app bundle.
4. **Unknowns**
   - Any values that follow a different naming structure (compared to apps and sites) that will need manual checking and potential confirmation with the Supply Side Platform partner.

---

## Input Format

- Input data must contain two columns named respectively as Name and Value. The Value column corresponds to the mixed list of sites and apps. The name column will provide the names of corresponding app bundles which would have been provided by the Supply Side Platform partner.

---

## Limitation

- The tuple of TLDs is not exhaustive. The consequence of this is that some sites will be classified as an app bundle in the cases where the TLD of that particular site is not present in the tuple. The original tuple contains the most common TLDs however the idea is that the more this tool is used and the results are reviewed, and missing TLDs can be added to the script and this tuple can grow over time.
