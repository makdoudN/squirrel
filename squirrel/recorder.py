import pandas as pd
import numpy as np
import datetime
import os.path
import atexit
import yaml
import csv
import sys
import os

from typing import List
from .utils import display_statistics


class Recorder:
    """A simple yet general-purpose tracker."""

    def __init__(
        self,
        output_dir: str = "results",
        output_res_fname: str = "progress.csv",
        outpute_config_fname: str = "conf.yaml",
        csv_delimiter: str = ",",
        external_tracker: List[str] = [],
    ):

        self.conf = None
        self.output_dir = os.path.expanduser(output_dir)
        self.csv_delimiter = csv_delimiter
        self.output_res_fname = output_res_fname
        self.outpute_config_fname = outpute_config_fname
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)

        # TODO Add external tracker
        # Add Dictionnary {'str': Class}
        # and at each log -> trigger all external tracker with {params} -> tracker


        # We open the csv because it should be used continually during
        # the training for logging results in constrast to configuration (and potentially other file).
        # `atexit` library is an helper to register callback not to forget to close the file at the
        # end of the script.
        self.output_res_file = open(
            os.path.join(self.output_dir, output_res_fname), "w"
        )
        atexit.register(self.output_res_file.close)
        self.csv_writer = None

        self.start_time = datetime.datetime.now()
        self.start_time_fmt = datetime.datetime.strftime(
            self.start_time, "%d, %H, %M, %S"
        )

    def save_conf(self, conf: dict, cache=True):
        """ Save the configuration file.

        We optionally cache the configuration to allow certain operations.
        For example, we provide a 'make_report' function that mix the results with
        the configuration which is interesting for plotting and diving into the results over multiple runs.
        """
        f_name = os.path.join(self.output_dir, self.outpute_config_fname)
        with open(f_name, "w") as f:
            yaml.safe_dump(conf, f)
        if cache:
            self.conf = conf

    def write(self, kwargs: dict):
        if self.csv_writer is None:
            # We register the key as the header of the csv and assume it
            # will be fixe during the lifetime of the logger.
            self.csv_writer = csv.DictWriter(
                self.output_res_file,
                fieldnames=list(kwargs.keys()),
                delimiter=self.csv_delimiter,
            )
            self.csv_writer.writeheader()
        self.csv_writer.writerow(kwargs)
        self.output_res_file.flush()

    def store(self, kwargs: dict, add_time: bool = True, display: bool = True):
        if add_time:
            current_time = datetime.datetime.now()
            current_time_fmt = datetime.datetime.strftime(
                current_time, "%d, %H, %M, %S"
            )
            kwargs.update(
                {"_time": current_time_fmt, "_start-time": self.start_time_fmt}
            )

        self.write(kwargs)

        if display:
            display_statistics(kwargs)

        return kwargs

    def make_report(self, save: bool = True, fname: str = "report.pkl"):
        if self.conf is None:
            return None
        # TODO: Ensure we have to close the file
        self.output_res_file.close()
        # Merge the configuration file (if provided) and the result
        pro = self.get_progress()
        conf = pd.json_normalize(self.conf)
        conf = pd.concat([conf] * pro.shape[0], ignore_index=True)
        report = pd.concat([pro, conf], 1)
        if save and self.output_dir is not None:
            report.to_pickle(os.path.join(self.output_dir, fname))
        return report

    def get_progress(self):
        with open(os.path.join(self.output_dir, self.output_res_fname), "r") as f:
            df = pd.read_csv(f, delimiter=self.csv_delimiter)
        if "_time" in df:
            df["_time"] = pd.to_datetime(df['_time'], format="%d, %H, %M, %S")
            df["_elapsed_time"] = df["_time"] - df["_time"][0]
        return df


