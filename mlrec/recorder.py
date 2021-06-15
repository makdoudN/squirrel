import pandas as pd
import datetime
import os.path
import atexit
import yaml
import csv
import os

from .utils import display_statistics

try:
    from tensorboardX import SummaryWriter
except ImportError:
    pass


class Recorder:
    """A simple yet general-purpose tracker."""

    def __init__(
        self,
        output_dir: str = "results",
        output_res_fname: str = "progress.csv",
        csv_delimiter: str = ",",
        tb_use: float = True,
        tb_kwargs: dict = dict()
    ):
        self.output_dir = os.path.expanduser(output_dir)
        self.csv_delimiter = csv_delimiter
        self.output_res_fname = output_res_fname
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir)
        # We open the csv because it should be used continually during training.
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
        self._counter = 0

        # Tensorboard.
        self.tb_use = tb_use
        self.tb_kwargs = tb_kwargs
        self.tb_kwargs['log_dir'] = self.output_dir
        self.tb_writer = None
        if self.tb_use:
            self.tb_writer = SummaryWriter(**tb_kwargs)

    def save(self, obj, fname: str):
        """Helper to save an object in the directory of the current run."""
        # TODO: Add support for `json`|`yaml`|`OmegaConf`
        fname = os.path.join(self.output_dir, fname)
        with open(fname, "w") as f:
            yaml.safe_dump(obj, f)

    def write(self, kwargs: dict, add_time: bool = True, display: bool = True):
        if '_count' not in kwargs:
            kwargs.update({'_count': self._counter})
        if add_time:
            current_time = datetime.datetime.now()
            current_time_fmt = datetime.datetime.strftime(current_time, "%d, %H, %M, %S")
            kwargs.update({"_time": current_time_fmt, "_start-time": self.start_time_fmt})
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
        self._external_logger(kwargs)
        if display:
            display_statistics(kwargs)

    def _external_logger(self, kwargs):
        if self.tb_use:
            iters = kwargs['_count']
            for k, v in kwargs.items():
                if not k[0] in ['_']:
                    self.tb_writer.add_scalar(k, v, iters)
