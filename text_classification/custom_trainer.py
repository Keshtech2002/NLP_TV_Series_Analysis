import torch
from torch import nn
from transformers import Trainer 

import torch
import torch.nn as nn
from transformers import Trainer


class CustomTrainer(Trainer):

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")

        # Forward Pass
        outputs = model(**inputs)

        # In Hugging Face outputs, logits are attributes of ModelOutput objects
        logits = (
            outputs.get("logits")
            if isinstance(outputs, dict)
            else outputs.logits
        )
        logits = logits.float()

        # Compute Custom Loss
        loss_fct = nn.CrossEntropyLoss(
            weight=torch.tensor(self.class_weights, dtype=torch.float).to(
                device=self.device
            )
        )

        # Access num_labels via model.config (or self.model.config)
        num_labels = getattr(
            model.config,
            "num_labels",
            getattr(self.model.config, "num_labels", None),
        )

        loss = loss_fct(logits.view(-1, num_labels), labels.view(-1))

        return (loss, outputs) if return_outputs else loss

    def set_class_weights(self, class_weights):
        self.class_weights = class_weights

    def set_device(self, device):
        self.device = device