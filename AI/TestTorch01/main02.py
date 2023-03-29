
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
    print(torch.__version__)
    print(torch.cuda.is_available())
    z0 = torch.cuda.device(0)
    print(z0)

    z1 = torch.cuda.device_count()
    print(z1)

    z2: str = torch.cuda.get_device_name(0)
    print(z2)
    k=1

    print('---  Torch  ---')
    cuda = torch.device('cuda')     # Default CUDA device
    cuda0 = torch.device('cuda:0')
    cuda2 = torch.device('cuda:2')

    x = torch.tensor([1., 2.], device=cuda0)

    y = torch.tensor([1., 2.]).cuda()

    _x0 = torch.cuda.is_available()
    _x1 = torch.cuda.device_count()
    _x2 = torch.cuda.current_device()
    _x3 = torch.cuda.device(0)
    _x4 = torch.cuda.device
    _x5 = torch.cuda.get_device_name(0)

    print(torch.rand([3, 4]).cuda())
    i=1
