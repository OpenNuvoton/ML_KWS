# ML_KWS
ML-Tool for Keyword Spotting, which includes data collection with EVB, training, and conversion.

# 1. First step
- If you haven't installed [NuEdgeWise](https://github.com/OpenNuvoton/NuEdgeWise), please follow these steps to install Python virtual environment and ***choose `NuEdgeWise_env`***.
- Please download and install the Nu-Link driver from the following link [KEIL Nu-Link debugger driver installer](https://github.com/OpenNuvoton/Nuvoton_Tools)
---
# 2. Work Flow
 <img src="https://user-images.githubusercontent.com/105192502/202999518-7d4a6384-6cef-4901-b948-b1117baa7bdd.png" width="50%">

## A. Collect your own KWS audio raw data in `ML_audio_record` folder
- Open `record_mcu.ipynb`.
- This notebook will help you load(flash) a record function *bin to your m460 board and record your voice.
- Please provide a one-second gap between each keyword, and continue collecting raw data until you have enough for training.
- The raw data is saved in raw folder, you can move all files to same Label folder for later preprocessing .
- (Note) You can utilize Google's training dataset during the training step.

- Open `record_mcu.ipynb`.
- This notebook will assist you in loading (flashing) a record function *bin file to your m460 board and recording your voice.
- Please leave at least a 1-second gap between each keyword and continue collecting raw data until you have accumulated enough for training purposes.
- The raw data will be saved in the `raw` folder. You can move all the files to the same label folder for later preprocessing.
- (Note) You can also use Google's training dataset (Can be downloaded at training step) during the training step.

## B. Processing the raw data in `ML_audio_aq` folder
- Open `SoundCrop.ipynb`.
- You can copy the previous label folder with raw data to `ML_audio_aq` for slicing each keyword individually.
- The sliced data will be saved in the `dataset\<YOUR_LABEL>` folder.

## C. Traing/Testing/Converting to Tflite in `ML_kws_tflu` folder
- Open `train.ipynb`, `test.ipynb`, `convert.ipynb`
- The details on how to use it are described in the Jupyter Notebook.
- (Note) It is recommended to download the Google's training data initially and then move your own training data folders into the same Google train data folder.

- Open `train.ipynb`, `test.ipynb`, `convert.ipynb`.
- The instructions on how to use these notebooks are described in the Jupyter Notebooks themselves.
- (Note) It is recommended to download the Google's training data initially and then move your own training data folders into the same Google train data folder.

# 3. Inference code
- This is an example of Keyword Spotting (KWS) using TensorFlow Lite Micro.
- [ML_M460_NuKws_SampleCode](https://github.com/OpenNuvoton/ML_M460_NuKws_SampleCode) 

 
