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
# Nuvoton updated the original code to add the following functions:

"""Functions for converting a TFLite model into a C source file loadable by TensorFlow Lite Micro."""

import argparse


def convert_tflite_to_array(open_file, tflite_path):
    """Write a C style array containing TFLite binary data into an open file.

    Args:
        open_file: Opened file to write to.
        tflite_path: Path to the TFLite to convert.
    """

    open_file.write('#include <cstdint>\n')
    open_file.write('#include <cstddef>\n')
    open_file.write('#include "BufAttributes.h"\n\n')

    model_arr_name = "g_kwsModel"
    open_file.write(f"static const uint8_t {model_arr_name}[] ALIGNMENT_ATTRIBUTE = ")

    _write_tflite_data(open_file, tflite_path)

    # Some extra functions useful for our deployment code.
    open_file.write(f"""

const uint8_t * GetModelPointer()
{{
    return {model_arr_name};
}}

size_t GetModelLen()
{{
    return sizeof({model_arr_name});
}}\n
""")

    # The KWS specify parameter for different model
    open_file.write(f"""
const uint8_t  GetFrameShiftMs()
{{
    return {FLAGS.window_stride_ms};
}}

const uint8_t GetFrameLenMs()
{{
    return {FLAGS.window_size_ms};
}}

const uint8_t GetNumMfccCoeffs()
{{
    return {FLAGS.dct_coefficient_count};
}}\n
""")



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
            line = line[:-2] + '};\n'
            open_file.write(line)
            break


def _model_hex_bytes(tflite_path):
    """Yields bytes from a tflite file."""
    with open(tflite_path, 'rb') as tflite_model:
        byte = tflite_model.read(1)
        while byte != b"":
            yield f'0x{byte.hex()}'
            byte = tflite_model.read(1)


def main():
    with open(FLAGS.output_path, 'w') as f:
        convert_tflite_to_array(f, FLAGS.tflite_path)


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

    FLAGS, _ = parser.parse_known_args()
    main()
