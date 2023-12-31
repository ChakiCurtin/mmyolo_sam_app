import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_images
# SOME LINKS FOR REFERENCE:
# * https://plotly.com/python-api-reference/generated/plotly.express.pie
# * https://plotly.com/python/builtin-colorscales/
# * https://github.com/Delgan/loguru
# * 
st.set_page_config(page_title="Dataset Selector", 
                   initial_sidebar_state="expanded",
                   layout="wide")

# -- ## -- CUSTOM CSS -- ## -- #
# -- [ "Remove the "made with streamlit" at the footer of the page]
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# -- ### - CONSTANTS - ### - #
KIDNEY_RENAL = "Kidney renal clear cell carcinoma"
BREAST_INVASIVE = "Breast invasive carcinoma"
KIDNEY_PAPILLARY = "Kidney renal papillary cell carcinoma"
LUNG_SQUAMOUS = "Lung squamous cell carcinoma"
LUNG_ADENO = "Lung adenocarcinoma"
PROST_ADENO = "Prostate adenocarcinoma"
BLADDER_URO = "Bladder Urothelial Carcinoma"
COLON_ADENO = "Colon adenocarcinoma"
STOMACH_ADENO = "Stomach adenocarcinoma"
# -- ################################ -- #

def dataset_selector(dataset_option: str):
    dataset_dict = {
        "monuseg": monuseg,
        "monusac": monusac,
        "cryonuseg": cryonuseg,
        "tnbc": tnbc,
    }
    return dataset_dict.get(dataset_option)

@st.cache_data
def load_monuseg():
    return pd.DataFrame.from_dict(
        {
        "Patient ID": ["TCGA-A7-A13E-01Z-00-DX1", "TCGA-A7-A13F-01Z-00-DX1", "TCGA-AR-A1AK-01Z-00-DX1", "TCGA-AR-A1AS-01Z-00-DX1",
                       "TCGA-E2-A1B5-01Z-00-DX1", "TCGA-E2-A14V-01Z-00-DX1", "TCGA-B0-5711-01Z-00-DX1", "TCGA-HE-7128-01Z-00-DX1",
                       "TCGA-HE-7129-01Z-00-DX1", "TCGA-HE-7130-01Z-00-DX1","TCGA-B0-5710-01Z-00-DX1","TCGA-B0-5698-01Z-00-DX1",
                       "TCGA-18-5592-01Z-00-DX1","TCGA-38-6178-01Z-00-DX1","TCGA-49-4488-01Z-00-DX1","TCGA-50-5931-01Z-00-DX1",
                       "TCGA-21-5784-01Z-00-DX1","TCGA-21-5786-01Z-00-DX1","TCGA-G9-6336-01Z-00-DX1","TCGA-G9-6348-01Z-00-DX1",
                       "TCGA-G9-6356-01Z-00-DX1","TCGA-G9-6363-01Z-00-DX1","TCGA-CH-5767-01Z-00-DX1","TCGA-G9-6362-01Z-00-DX1",
                       "TCGA-DK-A2I6-01A-01-TS1","TCGA-G2-A2EK-01A-02-TSB","TCGA-AY-A8YK-01A-01-TS1","TCGA-NH-A8F7-01A-01-TS1",
                       "TCGA-KB-A93J-01A-01-TS1","TCGA-RD-A8N9-01A-01-TS1","TCGA-AC-A2FO-01A-01-TS1","TCGA-AO-A0J2-01A-01-BSA",
                       "TCGA-2Z-A9J9-01A-01-TS1","TCGA-GL-6846-01A-01-BS1","TCGA-IZ-8196-01A-01-BS1",
                       ],
        "Organ": ["Breast", "Breast", "Breast", "Breast", "Breast", 
                  "Breast","Kidney", "Kidney", "Kidney", "Kidney",
                  "Kidney","Kidney","Liver","Liver","Liver","Liver","Liver",
                  "Liver","Prostate","Prostate","Prostate","Prostate","Prostate","Prostate",
                  "Bladder","Bladder","Colon","Colon","Stomach","Stomach","Breast","Breast","Kidney","Kidney","Kidney",
                  ],
        "Set": ["train","train","train","train","train","train","train","train","train",
                "train","train","train","train","train","train","train","train","train",
                "train","train","train","train","train","train","train","train","train",
                "train","train","train","test","test","test","test","test",],
        "Num of Organ": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
        "Disease type": [BREAST_INVASIVE,BREAST_INVASIVE,BREAST_INVASIVE,
                         BREAST_INVASIVE,BREAST_INVASIVE,BREAST_INVASIVE,
                         KIDNEY_RENAL,KIDNEY_PAPILLARY,KIDNEY_PAPILLARY,
                         KIDNEY_PAPILLARY,KIDNEY_RENAL,KIDNEY_RENAL,
                         LUNG_SQUAMOUS,LUNG_ADENO,LUNG_ADENO,
                         LUNG_ADENO,LUNG_SQUAMOUS,LUNG_SQUAMOUS,
                         PROST_ADENO,PROST_ADENO,PROST_ADENO,
                         PROST_ADENO,PROST_ADENO,PROST_ADENO,
                         BLADDER_URO,BLADDER_URO,COLON_ADENO,
                         COLON_ADENO,STOMACH_ADENO,STOMACH_ADENO,
                         BREAST_INVASIVE,BREAST_INVASIVE,KIDNEY_PAPILLARY,
                         KIDNEY_PAPILLARY,KIDNEY_PAPILLARY,
                         ],
        }, orient="columns")

def monuseg():
    df = load_monuseg()
    df_mutate = load_monuseg()
    df_mutate.drop(columns='Num of Organ', axis=1, inplace=True)
    cols = st.columns(2)
    url = "https://monuseg.grand-challenge.org/Data/"
    # a quick about section for MoNuSeg:
    cols[0].write("About MoNuSeg: \n\nMoNuSeg is a publicly available Cell Nuceli Segmentation (CNS) dataset containing H&E stained WSIs." +
                  " It contains 51 images, with 37 in the training set and 14 in the test set." +
                  " It provides 30837 annotations, with 24140 in the training set" +
                  " and 6697 in the test set. This is a binary segmentation dataset, so" +
                  " nuclei are all considered to be the same. Every image comes" +
                  " as a 1000 × 1000 pixel region of interest (ROI)." +
                  " All Images come from The Cancer Genome Atlas, which is the world's largest digital slide repository." + 
                  " Originally created for The Grand Challenge, it is a well known dataset for nuclei segmentation." +
                  " Full MoNuSeg dataset download [link](%s)." % url 
                  )
    cols[0].divider()
    #cols[0].checkbox("Use container width", value=True, key="use_container_width")
    cols[0].dataframe(df_mutate, use_container_width=True, hide_index=True,)
    
    #creating pie chart for number of organs
    pie_chart = px.pie(df, 
                       title="Total number of organs covered",
                       values="Num of Organ",
                       names="Organ",
                       hole=0.4,
                       width=700,
                       height=550,
                       color_discrete_sequence=px.colors.sequential.Turbo,
                       #color_discrete_sequence=px.colors.sequential.RdBu,
                       )
    cols[1].plotly_chart(pie_chart)
    cols[1].divider()
    # -- [ Show tiles of images from MoNuSeg ] -- #
    image_files, images_subset = load_images()
    sets = cols[1].multiselect("Dataset Image Select set(s)", images_subset)
    view_images = []
    for image_file in image_files:
        if any(set in image_file for set in sets):
            view_images.append(image_file)
    
    n = 3
    groups = []
    for i in range(0, len(view_images), n):
        groups.append(view_images[i:i+n])

    for group in groups:
        colss = cols[1].columns(n)
        for i, image_file in enumerate(group):
            colss[i].image(image_file)

#TODO[medium]: Finish the rest of the datasets. Find and add information for each
def cryonuseg():
    st.write("CryoNuSeg WIP")

def monusac():
    st.write("MoNuSAC WIP")

def tnbc():
    st.write("TNBC WIP")

def main():
    dataset_option = st.sidebar.selectbox(
        label="Choose Dataset to view:",
        options=('MoNuSeg', 'MoNuSAC', 'CryoNuSeg', 'TNBC'),
        index=0,
        placeholder="Choose a Dataset",
        )
    cols = st.columns(3)
    cols[1].header(f"{dataset_option} Dataset")
    dataset_selector(dataset_option=str(dataset_option).lower())() # makes a function from dict of functions
    st.sidebar.divider()


if __name__ == "__main__":
    main()