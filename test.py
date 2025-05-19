import torch
import numpy as np

print("Torch version:", torch.__version__)
print("NumPy version:", np.__version__)

tensor = torch.tensor([1.0, 2.0, 3.0])
numpy_array = tensor.numpy()
print("Tensor:", tensor)
print("Converted NumPy array:", numpy_array)
