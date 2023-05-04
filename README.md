# ML_nukws
ML-Tool for kws with combining other submodules 

# First step
- Download the [anaconda](https://www.anaconda.com/products/distribution) and install it.
- `git clone https://github.com/OpenNuvoton/ML_nukws.git`
- Use `jupyterLab_env_set.ipynb` in ML_nukws to create the KWS python running environment.
- Download and install Nu-Link, and please choose [KEIL Nu-Link debugger driver installer](https://github.com/OpenNuvoton/Nuvoton_Tools)
---
# Work Flow
 <img src="https://user-images.githubusercontent.com/105192502/202999518-7d4a6384-6cef-4901-b948-b1117baa7bdd.png" width="50%">

# Collect your own KWS audio raw data in `ML_audio_record` folder
- Open `record_mcu.ipynb`.
- This notebook will help you load(flash) a record function *bin to your m460 board and record your voice.
- Plase say your wanted keyword with at least 1(s) gap, and keep collecting raw data until it is enough to train.
- The raw data is saved in raw folder, you can move all files to same Label folder for latter preprocess <ToDo: move/copy to any location you want>.
- (Note:) Also you can use the google's train data set at train step.

# Processing the raw data in `ML_audio_aq` folder
- Open `SoundCrop.ipynb`.
- You can copy the previous Label folder with raw data to `ML_audio_aq` for slicing key word each by each at the same time.
- The finish sliced data are all saved at `dataset\<YOUR_LABEL>` folder.

# Traing/Testing/Converting to Tflite in `ML_kws_tflu` folder
- OPen `train.ipynb`, `test.ipynb`, `convert.ipynb`
- The detail of how to use is description in jupyter notebook.
- (Note:) Recommand to download the google's train data at first time, and move your own train data folders into the same google train data folder.

 
