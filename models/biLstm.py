import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Config
LABELS = ["soccer-ball", "y-card", "substitution-in"]
LABEL2IDX = {label: idx for idx, label in enumerate(LABELS)}
FEATURE_NAMES = ["1_ResNET_TF2_PCA512.npy", "2_ResNET_TF2_PCA512.npy"]
MAX_SEQUENCE_LENGTH = 1000 
ROOT_DIR = r"D:\KHÓA LUẬN\video-event-retrievel\data\soccernet"

# Load data
def load_data():
    X, y = [], []
    for competition in os.listdir(ROOT_DIR):
        comp_path = os.path.join(ROOT_DIR, competition)
        if not os.path.isdir(comp_path):
            print(f"[WARNING] {comp_path} is not a directory.")
            continue

        for season in os.listdir(comp_path):
            season_path = os.path.join(comp_path, season)
            if not os.path.isdir(season_path):
                print(f"[WARNING] {season_path} is not a directory.")
                continue

            for game in os.listdir(season_path):
                game_path = os.path.join(season_path, game)
                if not os.path.isdir(game_path):
                    print(f"[WARNING] {game_path} is not a directory.")
                    continue

                label_path = os.path.join(game_path, "Labels.json")
                if not os.path.exists(label_path):
                    print(f"[WARNING] Missing Labels.json in {game_path}")
                    continue

                try:
                    # Load features
                    features = []
                    for fname in FEATURE_NAMES:
                        fpath = os.path.join(game_path, fname)
                        if not os.path.exists(fpath):
                            print(f"[WARNING] Missing feature file {fname} in {game_path}")
                            continue
                        feat = np.load(fpath)
                        features.append(feat)
                    if not features:
                        print(f"[WARNING] No features found in {game_path}")
                        continue

                    feats = np.concatenate(features, axis=0)

                    # Load labels
                    with open(label_path, 'r') as f:
                        labels_json = json.load(f)

                    for label in labels_json.get('annotations', []):
                        category = label["label"]
                        if category in LABEL2IDX:
                            X.append(feats)
                            y.append(LABEL2IDX[category])
                        else:
                            print(f"[WARNING] Unknown label '{category}' in {label_path}")
                except Exception as e:
                    print(f"[ERROR] {game_path}: {e}")
    return X, y

# Prepare data
print("🔄 Loading data...")
X, y = load_data()
if len(X) == 0 or len(y) == 0:
    print("❌ No data loaded. Please check the dataset path and structure.")
    exit()
print(f"✅ Loaded {len(X)} samples.")

# Pad sequences
print("🔄 Padding sequences...")
X = tf.keras.preprocessing.sequence.pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH, padding='post', dtype='float32')
y = to_categorical(y, num_classes=len(LABELS))

# Split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Build model
input_layer = Input(shape=(MAX_SEQUENCE_LENGTH, 512))  # Cập nhật chiều dài đầu vào
x = Bidirectional(LSTM(64, return_sequences=False))(input_layer)
x = Dropout(0.5)(x)
x = Dense(64, activation='relu')(x)
x = Dense(len(LABELS), activation='softmax')(x)

model = Model(inputs=input_layer, outputs=x)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train
print("🚀 Training...")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# Save model
model.save("bilstm_model.h5")
print("✅ Model saved to bilstm_model.h5")

# Evaluate
print("📊 Evaluating model...")
y_pred = model.predict(X_val)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_val, axis=1)

# Classification report
report = classification_report(y_true_classes, y_pred_classes, target_names=LABELS)
print("\n📝 Classification Report:\n")
print(report)