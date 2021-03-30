# Squirrel. 
A simple yet efficient monitoring tools for ML Application.

Example.

```python
from squirrel.recorder import Recorder

conf = dict(lr=1)

logger = Recorder(
  output_dir='outputs',
  output_res_fname='progress.csv',
  outpute_config_fname='config.yaml'
)
logger.save_conf(conf)

for i in range(NUM_EPOCHS):
  loss = loss_fn(model, inputs, target)
  logger.store(loss=loss, epoch=i)

# `./outputs/progress.csv`
# epoch loss
#  0     0.23
#  1     0.19
#  2     0.18
#  ...
# './outputs/config.yaml'
#  lr: 1
```

