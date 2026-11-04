import torch
from torch import nn

device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
print(f"Using {device} device")

# expected shape of car image 
# (3, 96, 96)
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.network = nn.Sequential(
            nn.Conv2d(3, 16, 3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(16 * 94 * 94, 128),
            nn.ReLU(),
            nn.Linear(128, 5)
        )

    def forward(self, x):
        x = self.network(x)
        return x


model = NeuralNetwork().to(device)

# output a discrete action 
input_image = torch.rand(1, 3, 96, 96, device=device)
logits = model(input_image)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")



# # Save model parameters
# torch.save(model.state_dict(), "model.pth")

# # Recreate architecture
# model = NeuralNetwork()

# # Load saved parameters
# model.load_state_dict(
#     torch.load("model.pth", weights_only=True)
# )