import os
import sys
import torch


num_classes = 4 #background, method, result, conclusion

pretrained_model_name_or_path = './SciBert/'

num_train_epochs = 10
train_batch_size = 16
valid_batch_size = 8
learning_rate = 1e-5
weight_decay = 0
num_warmup_steps = 100


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
data_dir = os.path.join(sys.path[0], 'dataset')  # dir of dataset
weights_dir = os.path.join(sys.path[0], "weights")  # dir of weights
