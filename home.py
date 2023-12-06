import base64
from io import BufferedReader, BytesIO
import io
from mmengine import Config
from mmseg.apis import init_model, inference_model
from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
import utils 
import registers
from tempfile import NamedTemporaryFile
import cv2
import plotly.express as px
# -0- testing new python package -- #
from st_clickable_images import clickable_images

# -- [ Page settings ] -- #
st.set_page_config(page_title="Home | Image Segmenter", 
                   initial_sidebar_state="expanded",
                   layout="centered",
                   menu_items={
                        'About': " # App made by Chaki Ramesh.\n"
                        "Used Machine learning and Computer vision techniques to create a object detection -> instance segmentation (semantic) pipeline"
                        },
                   )
# ################################################################## #
# -- [ Custom CSS STUFF ] -- #
# -- -- [ allowing hover over image enlargment] -- -- #
st.markdown(
    """
    <style>
    img {
        cursor: pointer;
        transition: all .1s ease-in-out;
    }
    img:hover {
        transform: scale(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# -- [ "Remove the "made with streamlit" at the footer of the page]
hide_streamlit_style = """
            <style>
            MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# ################################################################## #
#@st.cache
@st.cache_resource
def register():
    registers.registerstuff()

def models_selector(chosen_model:str):
    models_dict = {
        "U-Net": unet_processor,
        "Deeplabv3+": deeplab_processor,
        "MMYOLOv8": mmyolo_processor,
        "Yolov8": yolo_processor,
        "MMYOLO -> SAM": process_image_pipeline,
     }
    return models_dict.get(chosen_model)

def show_selector(chosen_model:str):
    models_dict = {
        "U-Net": semantic_show,
        "Deeplabv3+": semantic_show,
        "MMYOLOv8": mmyolo_show,
        "Yolov8": yolo_show,
        "MMYOLO -> SAM": pipeline_show,
     }
    return models_dict.get(chosen_model)
     
def unet_processor(path_img, image, bar):
    config = Path("./models/semantic/unet/unet_test/unet.py")
    pathfile = Path("./models/semantic/unet/unet_test/iter_20000.pth")
    cfg = Config.fromfile(config)
    bar.progress(20)
    model = init_model(cfg, str(pathfile), 'cuda:0')
    bar.progress(30)
    classes = model.dataset_meta['classes']
    palette = model.dataset_meta['palette']
    bar.progress(40)
    pred = process_images(path_img, model, classes, palette)
    bar.progress(100)
    # -- add the mask to current session-- #
    st.session_state.batched_mask = pred

def deeplab_processor(path_img, image, bar):
    config = Path("./models/semantic/deeplab/deeplab_test/deeplab.py")
    pathfile = Path("./models/semantic/deeplab/deeplab_test/iter_20000.pth")
    cfg = Config.fromfile(config)
    bar.progress(20)
    model = init_model(cfg, str(pathfile), 'cuda:0')
    bar.progress(30)
    classes = model.dataset_meta['classes']
    palette = "255,77,255"
    bar.progress(40)
    pred = process_images(path_img, model, classes, palette)
    bar.progress(100)
    # -- add the mask to current session-- #
    st.session_state.batched_mask = pred

def process_images(path_img, model, classes, palette):
    img = cv2.imread(path_img)
    result = inference_model(model, img)
    mask = utils.numpy_from_result(result=result) # Prediction raw
    # - - [ Saving raw image to session state to be used for different applications ] - - #
    st.session_state.pred_mask_raw = mask
    dest = mask_overlay(img, mask, classes, palette)
    # TODO: Add conditional for sample images only to show metrics
    # TODO: Add metrics and overlay and pred_mask_raw to get deleted on image reset
    metrics = generate_metrics_per_img(path_img)
    st.session_state.metrics = metrics
    return dest

def generate_metrics_per_img(img_path:str,):
    gt_path = utils.name_processer(img=img_path)
    gt_path = utils.mask_searcher(gt_path)
    raw_mask:np.ndarray = st.session_state.pred_mask_raw
    f = NamedTemporaryFile(dir='./temp', suffix='.png', delete=True)
    is_success, buffer = cv2.imencode(".png", raw_mask) # Required for encoding binary images to file
    io_buf = io.BytesIO(buffer) # Create a bufferable encoded file
    f.write(io_buf.getbuffer()) # write to file
    df = utils.model_accuracy(ground=Path(gt_path),prediction=Path(f.name))
    # -- [ Get overlay for both gt and pred ] -- #
    overlay =  utils.gt_pred_overlay(ground=Path(gt_path),prediction=Path(f.name))
    st.session_state.overlay = overlay
    return df

def mask_overlay(img, mask, classes, palette):
    dest = img.copy()
    labels = np.unique(mask)

    for label in labels:
        # skipping background (ugly in visualisations)
        if classes[label].lower() in ["background", "bg"]:
            continue
        binary_mask = (mask == label)
        colour_mask = np.zeros_like(img)
        # -- Skipping outline for now
        colour_mask[...] = palette[label]
        dest[binary_mask] = cv2.addWeighted(img, 1 - 0.5, colour_mask, 0.5, 0)[binary_mask]
    return dest 

def mmyolo_processor(path_img, image, bar):
    return "mmyolo"

def yolo_processor(path_img, image, bar):
    return "yolo"

def make_pretty(styler):
    styler.set_caption("Image Metrics")
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
    return styler

def semantic_show(processed_image, og_img,sidebar_option_subheader, side_tab_options, main_col_1):
    sidebar_option_subheader.subheader("Please choose one of the following options:")
    if "mask_check" not in st.session_state:
        st.session_state.mask_check = True
    if "image_check" not in st.session_state:
        st.session_state.image_check = True
    if "overlay_check" not in st.session_state:
        st.session_state.overlay_check = False
    show_mask_checkbox = side_tab_options[2].checkbox("Show Mask", value=st.session_state.mask_check)
    show_image_checkbox = side_tab_options[2].checkbox("Show Image", value=st.session_state.image_check)
    show_overlay_checkbox = side_tab_options[2].checkbox("Show Overlay", value= st.session_state.overlay_check)
    
    # -- [ setting all checkboxes]
    if show_mask_checkbox and not show_image_checkbox and not show_overlay_checkbox:
        show_image = utils.binary_to_bgr(img=st.session_state.pred_mask_raw)
        fig = px.imshow(show_image,height=800,aspect='equal')
    elif not show_mask_checkbox and show_image_checkbox and not show_overlay_checkbox:
        show_image = og_img
        fig = px.imshow(show_image,height=800,aspect='equal')
    elif not show_mask_checkbox and not show_image_checkbox and show_overlay_checkbox:
        show_image = st.session_state.overlay
    elif show_mask_checkbox and show_image_checkbox and not show_overlay_checkbox:
        show_image = st.session_state.batched_mask      
    elif not show_mask_checkbox and show_image_checkbox and show_overlay_checkbox:
        side_tab_options[2].warning("Overlay option has to be the only option toggled. This will show overlay only")
        show_image = st.session_state.overlay     
    elif show_mask_checkbox and not show_image_checkbox and show_overlay_checkbox:
        side_tab_options[2].warning("Overlay option has to be the only option toggled. This will show overlay only")
        show_image = st.session_state.overlay    
    elif show_mask_checkbox and show_image_checkbox and show_overlay_checkbox:
        side_tab_options[2].warning("Overlay option has to be the only option toggled. This will show overlay only")
        show_image = st.session_state.overlay 

    if not show_mask_checkbox and not show_image_checkbox and not show_overlay_checkbox:
        processed_image.empty()
    else:
        if show_overlay_checkbox:
            fig = px.imshow(show_image,height=800,aspect='equal')
            processed_image.plotly_chart(fig,use_container_width=True)
            st.markdown('''
                        <span style="color:#0000FF;font-size:40.5px;font-weight:700"> | Ground Truth | </span> 
                        <span style="color:red;font-size:40.5px;font-weight:700"> | Prediction | </span> 
                        <span style="color:#FF00FF;font-size:40.5px;font-weight:700"> | Overlap | </span> 
                        ''',unsafe_allow_html=True)
        else:
            fig = px.imshow(show_image,height=800,aspect='equal')
            processed_image.plotly_chart(fig,use_container_width=True)
        
    side_tab_options[2].divider()
    # -- [ Get accuracy of the prediction result if ] -- #
    if "metrics" in st.session_state:
        df:pd.DataFrame = st.session_state.metrics
        df.style.set_caption("Hello")
        df.columns = ["metric"]
        df = df.drop("name")
        cell_hover = {  # for row hover use <tr> instead of <td>
            'selector': 'td:hover',
            'props': [('background-color', '#ffffb3')]
        }
        index_names = {
            'selector': '.index_name',
            'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
        }       
        headers = {
            'selector': 'th:not(.index_name)',
            'props': 'background-color: #000066; color: white;'
        }
        df.style.set_table_styles([cell_hover, index_names, headers])
        new_tab = "\u2001Metrics\u2001\u2001"
        if new_tab not in st.session_state.menu_tabs:
            st.session_state.menu_tabs.append(new_tab)
            st.rerun()
            
        side_tab_options[3].dataframe(data=df,use_container_width=True)
        

def mmyolo_show(processed_image, og_img,sidebar_option_subheader, side_tab_options, main_col_1):
    fig = px.imshow(st.session_state.batched_mask,height=800,aspect='equal',)
    processed_image.plotly_chart(fig,use_container_width=True)

def yolo_show(processed_image, og_img,sidebar_option_subheader, side_tab_options, main_col_1):
    fig = px.imshow(st.session_state.batched_mask,height=800,aspect='equal',)
    processed_image.plotly_chart(fig,use_container_width=True)

# TODO: Add multiple models for processing images. 
# Bounding boxes should still be able to be extracted and added. Semantic segmentation methods like UNET and DEEPLAB and
# Current pipeline methods for mmyolo, rtmdet with SAM should be added
def process_image_pipeline(path_img, image, bar):
    config = Path("./models/objdetection/mmyolo/mmyolov8/mmyolov8_config.py")
    pathfile = Path("./models/objdetection/mmyolo/mmyolov8/epoch_800.pth")
    model = utils.mmyolo_init(config=config,pathfile=pathfile)
    predictor = utils.sam_init()
    bar.progress(10)
    # -- Inference detection -- #
    detections = utils.inference_detections(model=model, image=path_img) 
    bar.progress(30)
    # -- process inference to inputs for SAM -- #
    inputs_boxes = utils.input_boxes_sam(detections)
    bar.progress(50)
    # -- get prediction information from SAM -- #
    masks_list = utils.prediction_masks_sam(image=image, predictor=predictor, inputs_boxes=inputs_boxes)
    bar.progress(70)
    # -- process these masks into one image array -- #
    batched_mask = utils.masks_array_sam(masks_list=masks_list)
    bar.progress(90)
    # -- add the mask to current session-- #
    st.session_state.detections = detections
    st.session_state.batched_mask = batched_mask

def pipeline_show(processed_image, og_img,sidebar_option_subheader, side_tab_options, main_col_1):
    sidebar_option_subheader.subheader("Please choose one of the following options:")
    bounding_box_checkbox = side_tab_options.checkbox("Show Bounding Box", value=False)
    show_mask_checkbox = side_tab_options.checkbox("Show Mask", value=True)

    # -- Process the mask and output the overlay -- #
    if "mask_img" not in st.session_state:
        total_image = og_img.copy()
        batched_mask = np.asarray(st.session_state.batched_mask) * 255
        batched_mask = cv2.cvtColor(batched_mask.astype(np.float32), cv2.COLOR_RGBA2RGB)
        total_image_covered = cv2.bitwise_or(total_image, batched_mask.astype(np.uint8))
        # -- Saving mask + img for future ref -- #
        st.session_state.mask_img = total_image_covered
    # -- -------------------------------- -- #
    show_image = og_img
    if bounding_box_checkbox and show_mask_checkbox:
            # -- Show both bounding box and mask on image
            mask_bound_img = utils.show_box_cv(st.session_state.detections, st.session_state.mask_img.copy())
            show_image = mask_bound_img
    if bounding_box_checkbox and not show_mask_checkbox:
            # -- show only bounding box on original image
            orig_bound_img = utils.show_box_cv(st.session_state.detections, og_img.copy())
            show_image = orig_bound_img
    if not bounding_box_checkbox and show_mask_checkbox:
            # -- show only mask on original image
            show_image = st.session_state.mask_img
    if not bounding_box_checkbox and not show_mask_checkbox:
            # -- Just show original image
            show_image = og_img
    processed_image.image(show_image, caption=st.session_state.uploaded_image.name)
    fig = px.imshow(show_image,height=800,aspect='equal',)
    st.plotly_chart(fig,use_container_width=True)

    main_col_1.download_button(label="Download", data=download_image(show_image), file_name=st.session_state.uploaded_image.name, mime="image/png")

def main():
    st.sidebar.title("Single Cell Nuclei Segmentation")
    menu_tabs = [
        "\u2001\u2001Settings\u2001\u2001",
        "\u2001Image Upload\u2001\u2001" ,
        "\u2001\u2001Options\u2001\u2001",
    ]
    if "menu_tabs" not in st.session_state:
        st.session_state.menu_tabs = menu_tabs
    side_tabs = st.sidebar.tabs(st.session_state.menu_tabs)                                 
    
    # -- [ SETTINGS TAB INFO ] -- #
    side_tabs[0].title("Choose Model:")
    model_option = side_tabs[0].selectbox(label="Choose Model Range",
                                options=('Semantic Segmentation', 'Object Detection', 'Pipeline: Object Detection -> Semantic Segmentation',),
                                index=None,
                                placeholder="Choose a Model Type",
                                )
    if model_option is not None:
        overall_model = None
        if model_option == "Semantic Segmentation":
            overall_model = side_tabs[0].radio(label=" ",
                                                      options=["U-Net","Deeplabv3+",],
                                                      captions=["Popular in medical research","Newer and and upgrade over U-Net"])
            side_tabs[0].divider()
            side_tabs[0].warning("Semantic segmentation models do not show bounding boxes around the seperate nuclei, it will only show mask on image.")
            side_tabs[0].warning("The model was trained on the MoNuSeg dataset.")
        elif model_option == "Object Detection":
            overall_model = side_tabs[0].radio(label=" ",
                                                      options=["MMYOLOv8","Yolov8",],
                                                      captions=["OpenMMLab implementation of Yolov8","The original Yolov8"])
            side_tabs[0].divider()
            side_tabs[0].warning("Object detection models do not show mask, only a bounding box around the seperate detected nuceli.")
            side_tabs[0].warning("The model was trained on the MoNuSeg dataset.")
        elif model_option == "Pipeline: Object Detection -> Semantic Segmentation":
            overall_model = side_tabs[0].radio(label=" ",
                                                      options=["MMYOLO -> SAM"],
                                                      captions=["Object detection through MMYOLO with Segment anything model (SAM)"])
            side_tabs[0].divider()
            side_tabs[0].warning("The pipeline will use the chosen object detector for the input bounding boxes which will then be used with the segment anything model (SAM) to produce the mask around the detected nuceli.")
            side_tabs[0].warning("The model was trained on the MoNuSeg dataset.")
            side_tabs[0].warning("This will take a while to process and show.")
        st.session_state.model_option = overall_model

    # -- [ IMAGE UPLOAD TAB INFO ] -- #
    side_tabs[1].header("Upload nuclei image:")
    # -- [ Disable uploader once upload has been done] -- #
    if 'is_uploaded' not in st.session_state:
        st.session_state.is_uploaded = False
    uploaded_image = side_tabs[1].file_uploader("Upload H&E stained image (png)", type=["png"], disabled=st.session_state.is_uploaded)
    side_tabs[1].divider()
    side_tabs[1].header("Or, choose from our sample images:")
    image_files, images_subset = utils.load_images()
    # TODO - Create new function which only takes test images 
    #        from directories of dataset selected. No longer "test" or "train". 
    #        Will become "MoNuSeg", "CryoNuSeg"

    sets = side_tabs[1].multiselect("Dataset Selector", images_subset, key="dataset_multi")
    view_images = []
    for image_file in image_files:
        if any(set in image_file for set in sets):
            view_images.append(image_file)
        else:
            if "image" in st.session_state and uploaded_image is None:
               del st.session_state.image
    images = []
    for img in view_images:
        with open(img, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/png;base64,{encoded}")
    n = 1
    to_show = []
    for i in range(0, int(len(images) / 2.5), n):
        to_show.append(images[i:i+n])

    # TODO: Fix multiselector to show datasets rather than sets in dataset. "MoNuSeg" rather than "test"
    with side_tabs[1]:
        clicked = clickable_images(to_show,
                                titles=[],
                                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                img_style={"margin": "5px", "height": "200px"},
                                key="clickable_img"
                                )
        if clicked > -1 and "dataset_multi" in st.session_state:
            if len(view_images) > 0:
                img = cv2.imread(view_images[clicked])
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                st.session_state.image = (img,view_images[clicked])
                st.write(utils.name_processer(str(view_images[clicked])))
    side_tabs[1].warning("Uploaded image takes priority thus if selecting from sample, please remove uploaded file")

    # TODO - Add multi image input (list of images for processing)
    # -- [ OPTIONS TAB INFO ] -- #
    side_tabs[2].markdown("<h1 style='text-align: center; font-size: 40px'>Options</h1>", unsafe_allow_html=True)
    subheader_text = "Please Process Image for Options"
    sidebar_option_subheader = side_tabs[2].subheader(subheader_text)

    if uploaded_image is not None:
        if 'uploaded_image' not in st.session_state:
            st.session_state.uploaded_image = uploaded_image
        f = NamedTemporaryFile(dir='./temp', suffix='.png', delete=True)
        f.write(uploaded_image.getbuffer())
        img = cv2.imread(f.name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if not st.session_state.is_uploaded:
            st.session_state.is_uploaded = True
            st.rerun()
        # -- Define image for session state -- #
        st.session_state.image = (img,f.name)
        # -- ------------------------------ -- #

    if "image" in st.session_state:
        processed_image = st.empty()
        given_image, img_name = st.session_state.image
        fig = px.imshow(given_image,height=800,)
        processed_image.plotly_chart(fig)
        cols = st.columns(3)
        if cols[2].button('Clear Image', disabled=(uploaded_image is not None)):
            app_rerunner()
            st.rerun()
        # -- Check if button has already been pressed -- #
        if "is_processed" not in st.session_state:
            st.session_state.is_processed = False
        # -- ---------------------------------------- -- #
        if 'process_button' not in st.session_state:
            st.session_state.process_button = False  
        # -- ---------------------------------------- -- #
        if cols[0].button('Process Image', disabled=st.session_state.process_button):
                if "model_option" in st.session_state:
                    if cols[1].button('Stop Processing', disabled=st.session_state.process_button):
                        st.stop()
                    with st.spinner(text='In progress'):
                        bar = st.progress(0)
                        print(img_name)
                        models_selector(st.session_state.model_option)(img_name, given_image, bar)
                        bar.progress(100)
                        st.success('Done')
                        st.session_state.is_processed = True
                else:
                    st.warning("Please Choose a model in the 'Settings' tab on the left (sidebar)")
                    st.stop()
        

        if st.session_state.is_processed:
            st.session_state.process_button = True
            show_selector(st.session_state.model_option)(processed_image=processed_image,
                                                            side_tab_options=side_tabs,
                                                            sidebar_option_subheader=sidebar_option_subheader,
                                                            main_col_1=cols[1],
                                                            og_img=img,
                                                            )
    else:
        app_rerunner()

def app_rerunner():
    st.warning("Please use the sidebar <- to choose the model, upload the image for processing.")
    print("[*] Clearing local variables stored in cache for the image")
    if 'uploaded_image' in st.session_state:
            del st.session_state.uploaded_image
            print("[**] cleared uploaded_image")
    if 'image' in st.session_state:
        del st.session_state.image
        print("[**] cleared image")
    if "is_processed" in st.session_state:
        del st.session_state.is_processed
        print("[**] cleared is_processed")
    if "process_button" in st.session_state:
        del st.session_state.process_button
        print("[**] cleared process_button")
    if "clickable_img" in st.session_state:
        print("[**] deleting clickable image")
        del st.session_state.clickable_img
    if 'detections' in st.session_state:
        del st.session_state.detections
        print("[**] cleared detections")
    if "batched_mask" in st.session_state:
        del st.session_state.batched_mask
        print("[**] cleared batched_mask")
    if "mask_img" in st.session_state:
        del st.session_state.mask_img
        print("[**] cleared mask_img")
    if "processed_mask" in st.session_state:
        del st.session_state.processed_mask

    new_tab = "\u2001Metrics\u2001\u2001"
    if new_tab in st.session_state.menu_tabs:
        st.session_state.menu_tabs.remove(new_tab)

    if st.session_state.is_uploaded:
        del st.session_state.is_uploaded
        print("[**] cleared is_uploaded")
        st.rerun()
    
def download_image(img):
    img = img[:, :, [2, 1, 0]] #numpy.ndarray # from bgr to rgb
    _, img_enco = cv2.imencode(".png", img)
    srt_enco = img_enco.tobytes() #bytes
    img_bytesio = BytesIO(srt_enco) #_io.BytesIO
    img_bufferedreader = BufferedReader(img_bytesio) #_io.BufferedReader
    return img_bufferedreader


if __name__ == "__main__":
    register()
    main()