# Model Surgery Documentation (`add_breed.py`)

**Role:** Incremental Learning / Model Surgery.

This advanced script allows adding a **new breed** to an existing trained model without retraining from scratch.

## The "Surgery" Process

1.  **Load Old Model**: Loads the existing `pet_classifier.keras`.
2.  **Detect New Classes**: Scans the `ml/data/train` directory to find the new total number of classes ($N_{new}$).
3.  **Create New Architecture**: Instantiates a fresh model with $N_{new}$ output neurons.
4.  **Weight Transfer**:
    - Copies weights layer-by-layer from the old model to the new model for all layers *except* the final output layer.
5.  **Output Layer Surgery**:
    - For the final Dense layer, it creates a new weight matrix of shape `(input_dim, N_new)`.
    - It copies the weights for the *existing* classes into their corresponding positions.
    - It initializes the weights for the *new* class randomly.
6.  **Fine-Tuning**:
    - Compiles the new model.
    - Trains briefly (2 epochs) to let the new weights settle and learn the new breed features.
7.  **Save**: Overwrites the old model with the new, expanded one.

## Usage
Triggered automatically by the backend when a user uploads a ZIP file for a new breed via the `/admin/train` page.
