# ML_KWS
ML-Tool for Keyword Spotting which including data collecting with EVB, training and converting.

# 1. First step
- If you haven't installed [NuEdgeWise](https://github.com/OpenNuvoton/NuEdgeWise), please follow these steps to install Python virtual environment and ***choose `NuEdgeWise_env`***.
- Download and install the Nu-Link driver. Please choose the [KEIL Nu-Link debugger driver installer](https://github.com/OpenNuvoton/Nuvoton_Tools)
---
# 2. Work Flow
 <img src="https://user-images.githubusercontent.com/105192502/202999518-7d4a6384-6cef-4901-b948-b1117baa7bdd.png" width="50%">

## A. Collect your own KWS audio raw data in `ML_audio_record` folder
- Open `record_mcu.ipynb`.
- This notebook will help you load(flash) a record function *bin to your m460 board and record your voice.
- Plase say your wanted keyword with at least 1(s) gap, and keep collecting raw data until it is enough to train.
- The raw data is saved in raw folder, you can move all files to same Label folder for latter preprocess <ToDo: move/copy to any location you want>.
- (Note:) Also you can use the google's train data set at train step.

- Open `record_mcu.ipynb`.
- This notebook will assist you in loading (flashing) a record function *bin file to your m460 board and recording your voice.
- Please say your desired keyword with at least a 1-second gap and continue collecting raw data until you have enough for training.
- The raw data will be saved in the `raw` folder. You can move all the files to the same label folder for later preprocessing.
- (Note:) You can also use Google's training dataset (Can be downloaded at training step) during the training step.

## B. Processing the raw data in `ML_audio_aq` folder
- Open `SoundCrop.ipynb`.
- You can copy the previous label folder with raw data to `ML_audio_aq` for slicing each keyword individually.
- The sliced data will be saved in the `dataset\<YOUR_LABEL>` folder.

## C. Traing/Testing/Converting to Tflite in `ML_kws_tflu` folder
- OPen `train.ipynb`, `test.ipynb`, `convert.ipynb`
- The detail of how to use is description in jupyter notebook.
- (Note:) Recommand to download the google's train data at first time, and move your own train data folders into the same google train data folder.

- Open `train.ipynb`, `test.ipynb`, `convert.ipynb`.
- The instructions on how to use these notebooks are described in the Jupyter notebooks themselves.
- (Note:) It is recommended to download the Google's training data initially and then move your own training data folders into the same Google train data folder.

# 3. Inference code
- This is kws example with TFlite for MCU.
-[ML_M460_NuKws_SampleCode](https://github.com/OpenNuvoton/ML_M460_NuKws_SampleCode) 

 
