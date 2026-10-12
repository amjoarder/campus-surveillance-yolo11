# Training records

The two submitted detector checkpoints were fine-tuned with the Ultralytics 8.3.116 command-line interface. The training commands, screenshots, saved arguments and epoch histories are retained in this directory. No separate author-written training script was retained.

Both runs used Python 3.10.17, PyTorch 2.6.0+cu124, YOLO11-large, 640-pixel inputs, batch size 16, seed 0, frozen first 20 layers, mixed precision and cosine learning-rate scheduling. The `optimizer=auto` setting selected SGD with learning rate 0.01, momentum 0.9 and weight decay 0.0005, as recorded in the run console.

The object run planned 1,000 epochs with patience 200 and completed 669 epochs; checkpoint selection chose epoch 469. The behavior run planned 1,200 epochs with patience 300 and completed 489 epochs; checkpoint selection chose epoch 189. The selected checkpoints and reported measurements are defined by the retained run records.

Retraining is outside the verification workflow. A reproduction requires the exact authorized dataset exports, a compatible environment and the recorded commands; numerical weights need not be bit-identical across environments.
