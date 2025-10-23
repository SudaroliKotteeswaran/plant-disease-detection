import tensorflow as tf
from keras import layers, models
import json, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--train_dir', required=True)
parser.add_argument('--val_dir', required=True)
parser.add_argument('--epochs', type=int, default=10)
parser.add_argument('--batch', type=int, default=16)
parser.add_argument('--img_size', type=int, default=224)
parser.add_argument('--save_path', default='models/best_model.h5')
args = parser.parse_args()

os.makedirs(os.path.dirname(args.save_path) or '.', exist_ok=True)

# Load training & validation datasets
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    args.train_dir, image_size=(args.img_size, args.img_size),
    batch_size=args.batch, shuffle=True)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    args.val_dir, image_size=(args.img_size, args.img_size),
    batch_size=args.batch)

# Save class names to JSON
class_names = train_ds.class_names
print("Classes:", class_names)
with open('models/class_indices.json','w') as f:
    json.dump({c:i for i,c in enumerate(class_names)}, f)

# Build model using transfer learning
base = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False,
                                         input_shape=(args.img_size,args.img_size,3))
base.trainable = False

inputs = layers.Input(shape=(args.img_size,args.img_size,3))
x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(class_names), activation='softmax')(x)

model = models.Model(inputs, outputs)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train & save best model
callbacks = [
    tf.keras.callbacks.ModelCheckpoint(args.save_path, monitor='val_accuracy',
                                       save_best_only=True)
]

model.fit(train_ds, validation_data=val_ds, epochs=args.epochs,
          callbacks=callbacks)

print('✅ Training complete! Saved best model to', args.save_path)
