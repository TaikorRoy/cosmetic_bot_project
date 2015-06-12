# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import os
import shutil
from tutorial.pipelines import TutorialPipeline


def copyfile(destination_dirname):
    source_filename = TutorialPipeline.json_file_name + r".xlsx"
    source_dirname = os.getcwd()
    source_filepath = os.path.join(source_dirname, source_filename)

    destination_filename = source_filename
    destination_filepath = os.path.join(destination_dirname, destination_filename)

    shutil.copyfile(source_filepath, destination_filepath)


