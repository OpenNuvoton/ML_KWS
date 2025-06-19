#  Copyright (c) 2021 Arm Limited. All rights reserved.
#  SPDX-License-Identifier: Apache-2.0
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Utility script to generate model c file that can be included in the
project directly. This should be called as part of cmake framework
should the models need to be generated at configuration stage.
"""
import datetime
import os
from argparse import ArgumentParser
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import binascii

parser = ArgumentParser()

parser.add_argument("--output_dir", help="Model (.tflite) path", required=True)
parser.add_argument("--template_dir", type=str, help="Template files directory", default='kws_python/templates')
parser.add_argument('-l', '--labels', nargs='+', default=['_silence_', '_unknown_'], dest="labels")
parser.add_argument('--header', action='append', default=[], dest="headers")
parser.add_argument('-ns', '--namespaces', action='append', default=[], dest="namespaces")
parser.add_argument("--license_template", type=str, help="Header template file",
                    default="header_template.txt")
args = parser.parse_args()

env = Environment(loader=FileSystemLoader(args.template_dir),
                  trim_blocks=True,
                  lstrip_blocks=True)


def main(args):
    if not os.path.isdir(args.output_dir):
        raise Exception(f"{args.output_dir} not found")

    # Cpp filename:
    label_filename = "Labels.cpp"
    cpp_label_file = os.path.join(Path(args.output_dir), label_filename)
    print(f"++ Creatting label file: {os.path.basename(cpp_label_file)}")

    
    header_template = env.get_template(args.license_template)

    hdr = header_template.render(script_name=os.path.basename(__file__),
                                 gen_time=datetime.datetime.now(),
                                 year=datetime.datetime.now().year)
    
    labelsSize = len(args.labels)

    env.get_template('Labels.cc.template').stream(common_template_header=hdr,
                                                  labels=args.labels,
                                                  labelsSize=labelsSize,
                                                  additional_headers=args.headers,
                                                  namespaces=args.namespaces).dump(str(cpp_label_file))

if __name__ == '__main__':
    main(args)
