
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    _is_cuda = torch.cuda.is_available()
    print_hi('PyCharm')
    print(torch.__version__)
    print(_is_cuda)
    z0 = torch.cuda.device(0)
    print(z0)

    z1 = torch.cuda.device_count()
    print(z1)

    try:
        z2: str = torch.cuda.get_device_name(0)
        print(z2)
    except :
        print("Cuda - error")

    k=1

    print('---  Torch  ---')
    # torch.device('cuda')  # Default CUDA device
    cuda = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    cuda0 = torch.device('cuda:0')
    cuda2 = torch.device('cuda:2')

    x = torch.tensor([1., 2.], device=cuda)

    # y = torch.tensor([1., 2.]).cuda()
    y = torch.tensor([1., 2.], device=cuda)

    _x0 = torch.cuda.is_available()
    _x1 = torch.cuda.device_count()
    _x2 = torch.cuda.current_device()
    _x3 = torch.cuda.device(0)
    _x4 = torch.cuda.device

    try:
        _x5 = torch.cuda.get_device_name(0)
    except NameError :
        _errorx =1

    print(torch.rand([3, 4]).cuda())
    i=1
