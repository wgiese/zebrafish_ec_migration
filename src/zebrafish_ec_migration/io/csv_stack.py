"""ExcelLocalDataSet loads and saves data to a local Excel file. The
underlying functionality is supported by pandas, so it supports all
allowed pandas options for loading and saving Excel files.
"""
import pandas as pd

from kedro.io import AbstractDataSet
# Copyright 2018-2019 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited (“QuantumBlack”) name and logo
# (either separately or in combination, “QuantumBlack Trademarks”) are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.


"""
``AbstractDataSet`` implementation to save matplotlib objects as image files.
"""

import os.path
from typing import Any, Dict, Optional

from kedro.io import AbstractDataSet, DataSetError #, ExistsMixin


class CSVStackWriter(AbstractDataSet): #, ExistsMixin):
    """
        ``CSVStackWriter`` saves csv
    """

    def _describe(self) -> Dict[str, Any]:
        return dict(
            filepath=self._filepath,
            load_args=self._load_args,
            save_args=self._save_args,
        )

    def __init__(
        self,
        filepath: str,
        load_args: Optional[Dict[str, Any]] = None,
        save_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Creates a new instance of ``MatplotlibWriter``.

        Args:
            filepath: path to a text file.
            load_args: Currently ignored as loading is not supported.
            save_args: multiFile: allows for multiple csv objects
        """
        default_save_args = {"multiFile": True, "index": False}
        default_load_args = {"NamePattern": "unaligned_"}

        self._filepath = filepath
        self._load_args = self._handle_default_args(load_args, default_load_args)
        self._name_pattern = self._load_args.get("NamePattern")
        self._load_args.pop("NamePattern")
        self._save_args = self._handle_default_args(save_args, default_save_args)
        self._save_args.pop("multiFile")
        #self._save_args.pop("index")

    @staticmethod
    def _handle_default_args(user_args: dict, default_args: dict) -> dict:
        return {**default_args, **user_args} if user_args else default_args

    #def _load(self) -> str:
    #    raise DataSetError("Loading not supported for MatplotlibWriter")
    def _load(self):# -> None:
        
        data_set = dict()
        print("In load data!!!")
        for filename in os.listdir(self._filepath):
            if filename.endswith(".csv")and (filename.find(self._name_pattern) > -1):
                print(filename)
            data_set[filename] = pd.read_csv(self._filepath + filename)
        
        print(self._filepath)
        print(self._load_args)
        print(self._name_pattern)
        
        return data_set

    def _save(self, data) -> None:

        #if self._mutlifile_mode:
        print("====save_args====")
        print(self._save_args)
        print("=======")
        print(self)
        if not os.path.isdir(self._filepath):
            os.makedirs(self._filepath)

        if isinstance(data, list):
            for index, df in enumerate(data):
                df.to_csv(
                    os.path.join(self._filepath, str(index)), **self._save_args
                )

        elif isinstance(data, dict):
            for csv_name, df in data.items():
                df.to_csv(
                    os.path.join(self._filepath, csv_name), **self._save_args
                )

        else:
            data_type = type(data)
            raise DataSetError(
                (
                    "multiFile is True but data type "
                    "not dict or list. Rather, {}".format(data_type)
                )
            )

    def _exists(self) -> bool:
        return os.path.isfile(self._filepath)
