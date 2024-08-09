@echo off


call variables.bat

set vela_argu= %MODEL_SRC_DIR%\%MODEL_SRC_FILE% --accelerator-config=%VELA_ACCEL_CONFIG% --optimise %VELA_OPTIMISE_OPTION% --config %VELA_CONFIG_FILE% --memory-mode=%VELA_MEM_MODE% --system-config=%VELA_SYS_CONFIG% --output-dir=%MODEL_SRC_DIR%
set model_argu= --tflite_path %MODEL_SRC_DIR%\%MODEL_OPTIMISE_FILE% --output_dir %GEN_SRC_DIR% --template_dir %TEMPLATES_DIR% -ns arm -ns app -ns kws -e %EXPR_1% -e %EXPR_2% -e %EXPR_3%

@echo on

Tool\vela\vela-3_10_0.exe %vela_argu%
Tool\tflite2cpp\gen_model_cpp.exe %model_argu%

pause
