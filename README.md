A simple yet efficient monitoring tools for ML Application.

Example.

```python
from squirrel.recorder import Recorder

logger = Recorder(log_dir)
logger.save_conf(params)      # Optionally save the parameters used.

for i in range(EPOCH):
  loss = ...
  logger.store({'loss': loss, 'epoch': i})

```
