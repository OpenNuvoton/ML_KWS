# ML_nukws
ML-Tool for Keyword Spotting which including data collecting with EVB, training and converting.

# 1. First step
- If you havn't install [NuEdgeWise](https://github.com/MaxCYCHEN/NuEdgeWise), please follow the steps to install python virtual env and ***choose `tiny_ml_env`***.
- Download and install Nu-Link, and please choose [KEIL Nu-Link debugger driver installer](https://github.com/OpenNuvoton/Nuvoton_Tools)
---
# 2. Work Flow
 <img src="https://user-images.githubusercontent.com/105192502/202999518-7d4a6384-6cef-4901-b948-b1117baa7bdd.png" width="50%">

## A. Collect your own KWS audio raw data in `ML_audio_record` folder
- Open `record_mcu.ipynb`.
- This notebook will help you load(flash) a record function *bin to your m460 board and record your voice.
- Plase say your wanted keyword with at least 1(s) gap, and keep collecting raw data until it is enough to train.
- The raw data is saved in raw folder, you can move all files to same Label folder for latter preprocess <ToDo: move/copy to any location you want>.
- (Note:) Also you can use the google's train data set at train step.

## B. Processing the raw data in `ML_audio_aq` folder
- Open `SoundCrop.ipynb`.
- You can copy the previous Label folder with raw data to `ML_audio_aq` for slicing key word each by each at the same time.
- The finish sliced data are all saved at `dataset\<YOUR_LABEL>` folder.

## C. Traing/Testing/Converting to Tflite in `ML_kws_tflu` folder
- OPen `train.ipynb`, `test.ipynb`, `convert.ipynb`
- The detail of how to use is description in jupyter notebook.
- (Note:) Recommand to download the google's train data at first time, and move your own train data folders into the same google train data folder.

# 3. Inference code
- This is kws example with TFlite for MCU.
-[ML_M460_NuKws_SampleCode](https://github.com/OpenNuvoton/ML_M460_NuKws_SampleCode) 

 
