https://socialify.git.ci/makdoudN/squirrel/image?description=1&descriptionEditable=&font=KoHo&forks=1&logo=https%3A%2F%2Fwww.flaticon.com%2Fsvg%2Fstatic%2Ficons%2Fsvg%2F185%2F185724.svg&owner=1&pattern=Diagonal%20Stripes&stargazers=1&theme=Light

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
