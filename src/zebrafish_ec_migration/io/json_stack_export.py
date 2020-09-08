"""ExcelLocalDataSet loads and saves data to a local Excel file. The
underlying functionality is supported by pandas, so it supports all
allowed pandas options for loading and saving Excel files.
"""
#from os.path import isfile
import os.path
from typing import Any, Union, Dict
import json
import numpy as np

from kedro.io import AbstractDataSet

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class JSONStackDataSet(AbstractDataSet):
    """``ExcelLocalDataSet`` loads and saves data to a local Excel file. The
    underlying functionality is supported by pandas, so it supports all
    allowed pandas options for loading and saving Excel files.

    Example:
    ::

        >>> import pandas as pd
        >>>
        >>> data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5],
        >>>                      'col3': [5, 6]})
        >>> data_set = ExcelLocalDataSet(filepath="test.xlsx",
        >>>                              load_args={'sheet_name':"Sheet1"},
        >>>                              save_args=None)
        >>> data_set.save(data)
        >>> reloaded = data_set.load()
        >>>
        >>> assert data.equals(reloaded)

    """

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._filepath,
                    load_args=self._load_args,
                    save_args=self._save_args)

    def __init__(
        self,
        filepath: str,
        load_args: Dict[str, Any] = None,
        save_args: Dict[str, Any] = None,
    ) -> None:
        """Creates a new instance of ``ExcelLocalDataSet`` pointing to a concrete
        filepath.

        Args:
            engine: The engine used to write to excel files. The default
                          engine is 'xlswriter'.

            filepath: path to an Excel file.

            load_args: Pandas options for loading Excel files.
                Here you can find all available arguments:
                https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_excel.html
                The default_load_arg engine is 'xlrd', all others preserved.

            save_args: Pandas options for saving Excel files.
                Here you can find all available arguments:
                https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_excel.html
                All defaults are preserved.

        """
        self._filepath = filepath
        default_save_args = {"multiFile": True}
        default_load_args = {}

        self._load_args = {**default_load_args, **load_args} \
            if load_args is not None else default_load_args
        self._save_args = {**default_save_args, **save_args} \
            if save_args is not None else default_save_args


    def _load(self): #-> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        with open(self._filepath, 'r') as fp:
            data = json.load(fp)
        return data

    #def _save(self, data: dict) -> None:
    #    #writer = pd.ExcelWriter(self._filepath, engine=self._engine)
    #    #data.to_excel(writer, **self._save_args)
    #    #writer.save()
    #    with open(self._filepath, 'w') as fp:
    #        json.dump(data, fp, cls=NumpyEncoder)
            
            
    def _save(self, data) -> None:

        #if self._mutlifile_mode:

        if not os.path.isdir(self._filepath):
            os.makedirs(self._filepath)

        if isinstance(data, list):
            for index, single_dict in enumerate(data):
                with open(os.path.join(self._filepath, str(index)), 'w') as fp:
                    json.dump(single_dict, fp, cls=NumpyEncoder)
                df.to_csv(
                    os.path.join(self._filepath, str(index)), **self._save_args
                )

        elif isinstance(data, dict):
            for dict_name, single_dict in data.items():
                with open(os.path.join(self._filepath, dict_name), 'w') as fp:
                    json.dump(single_dict, fp, cls=NumpyEncoder)


        else:
            data_type = type(data)
            raise DataSetError(
                (
                    "multiFile is True but data type "
                    "not dict or list. Rather, {}".format(data_type)
                )
            )

    def _exists(self) -> bool:
        return isfile(self._filepath)
