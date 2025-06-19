# Copyright © 2020 Arm Ltd. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Functions for converting a TFLite model into a C source file loadable by TensorFlow Lite Micro for m55m1 BSP format."""

import argparse
import subprocess
import os
from pathlib import Path

def convert_tflite_to_array(open_file, tflite_path):
    """Write a C style array containing TFLite binary data into an open file.

    Args:
        open_file: Opened file to write to.
        tflite_path: Path to the TFLite to convert.
    """

    open_file.write(f'#include "BufAttributes.hpp"\n\n')
    open_file.write(f'#include <cstddef>\n')
    open_file.write(f'#include <cstdint>\n\n')

    if (FLAGS.model_type == 'ds_cnn'):
        open_file.write(f'#if defined(MODEL_DS_CNN)\n\n')
    else:
        open_file.write(f'#if defined(MODEL_DNN)\n\n')   

    open_file.write('namespace arm\n{\n')
    open_file.write('namespace app\n{\n')
    open_file.write('namespace kws\n{\n\n')                                  

    open_file.write(f'/* Model parameters for kws */;\n')
    g_FrameLength = int(FLAGS.sample_rate / 1000 * FLAGS.window_size_ms)
    open_file.write(f'extern const int   g_FrameLength    = {g_FrameLength};\n')
    g_FrameStride = int(FLAGS.sample_rate / 1000 * FLAGS.window_stride_ms)
    open_file.write(f'extern const int   g_FrameStride    = {g_FrameStride};\n')
    g_ScoreThreshold = 0.7
    open_file.write(f'extern const float g_ScoreThreshold = {g_ScoreThreshold};\n')
    open_file.write(f"static const uint8_t nn_model[] MODEL_TFLITE_ATTRIBUTE =\n")

    _write_tflite_data(open_file, tflite_path)

    # Some extra functions useful for our deployment code.
    open_file.write(f"""

const uint8_t * GetModelPointer()
{{
    return nn_model;
}}

size_t GetModelLen()
{{
    return sizeof(nn_model);
}}\n
""")
    
    open_file.write('} /* namespace arm */\n')
    open_file.write('} /* namespace app */\n')
    open_file.write('} /* namespace kws */\n\n')
    open_file.write('#endif')
    


def _write_tflite_data(open_file, tflite_path):
    """Write all tflite file binary data to an opened file."""


    read_bytes = _model_hex_bytes(tflite_path)
    line = ' {\n\t'
    i = 1
    while True:
        try:
            el = next(read_bytes)
            line = line + el + ', '
            if i % 20 == 0:
                line = line + '\n\t'
                open_file.write(line)
                line = ''
            i += 1
        except StopIteration:
            line = line[:-2] + '\n};\n\n\n'
            open_file.write(line)
            break


def _model_hex_bytes(tflite_path):
    """Yields bytes from a tflite file."""
    with open(tflite_path, 'rb') as tflite_model:
        byte = tflite_model.read(1)
        while byte != b"":
            yield f'0x{byte.hex()}'
            byte = tflite_model.read(1)

def _model_compile(model_file, output_path):
    """For m55m1 NPU, use vela compiler"""
 
    VELA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'vela')
    vela_exe = os.path.join(VELA_DIR_PATH, 'vela-4_0_1.exe')
    vela_conf_file = os.path.join(VELA_DIR_PATH, 'default_vela.ini')
    vela_conifg_option = '--config='+vela_conf_file

    vela_cmd = [vela_exe, model_file, '--accelerator-config=ethos-u55-256', '--optimise=Performance',
                vela_conifg_option, '--memory-mode=Shared_Sram', '--system-config=Ethos_U55_High_End_Embedded', f'--output-dir={Path(model_file).parent}']

    print(vela_cmd)
    ret = subprocess.run(vela_cmd)

    if ret.returncode == 0:
        print('vela compile done')
    else:
        print('Unable compile failee')
        return False

    return True         

def main():
    _model_compile(FLAGS.tflite_path, Path(FLAGS.tflite_path).parent)

    vela_model_basename = Path(FLAGS.tflite_path).stem
    vela_model_file = os.path.join(Path(FLAGS.tflite_path).parent, vela_model_basename + '_vela.tflite')

    with open(FLAGS.output_path, 'w') as f:
        convert_tflite_to_array(f, vela_model_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tflite_path',
        type=str,
        default='',
        help='Path to tflite file that will be converted.')
    parser.add_argument(
        '--output_path',
        type=str,
        default='',
        help='Path used for the output file.')
    parser.add_argument(
        '--window_size_ms',
        type=float,
        default=30.0,
        help='How long each spectrogram timeslice is',)
    parser.add_argument(
        '--window_stride_ms',
        type=float,
        default=10.0,
        help='How long each spectrogram timeslice is',)
    parser.add_argument(
        '--dct_coefficient_count',
        type=int,
        default=40,
        help='How many bins to use for the MFCC fingerprint',)
    parser.add_argument(
        '--sample_rate',
        type=int,
        default=16000,
        help='16kHZ',)
    parser.add_argument(
        '--clip_duration_ms',
        type=int,
        default=1000,
        help='clip_duration_ms = 1000 (ms) default',)
    parser.add_argument(
        '--model_type',
        type=str,
        default='ds_cnn',
        help='m55m1 only supports ds_cnn now')
    
    FLAGS, _ = parser.parse_known_args()
    main()
