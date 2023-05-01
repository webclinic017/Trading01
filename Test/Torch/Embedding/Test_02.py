# https://towardsdatascience.com/the-secret-to-improved-nlp-an-in-depth-look-at-the-nn-embedding-layer-in-pytorch-6e901e193e16

import torch
import torch.nn as nn


if __name__ == '__main__':
  print("==> Embedding 02 <==")
  # Define the embedding layer with 10 vocab size and 50 vector embeddings.
  embedding = nn.Embedding(10, 50)
  pretrained_embeddings = torch.randn(10, 50)  # Example only, not actual pre-trained embeddings
  embedding.weight.data.copy_(pretrained_embeddings)
  print(embedding)
  # print(embedding(torch.LongTensor([0])))
  # # print(embedding.weight)
  # nn.init.normal_(embedding.weight)
  # print(embedding.weight)
  # nn.init.xavier_uniform_(embedding.weight)
  # print(embedding.weight)

  k=1