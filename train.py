#!/usr/bin/env python3
import argparse
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator   # ✅ fix
from keras import layers, models
from keras.applications import MobileNetV2, ResNet50
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from utils import ensure_dirs
import json

ensure_dirs()


def build_model(num_classes, base='mobilenet'):
    input_shape = (224,224,3)
    if base == 'resnet':
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    else:
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)

    base_model.trainable = False  # freeze initially
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train(args):
    train_dir = args.train_dir
    val_dir = args.val_dir
    epochs = args.epochs
    batch = args.batch
    base = args.base

    # data generators (basic augmentation)
    if base == 'mobilenet':
        from tensorflow.keras.applications import mobilenet_v2
        preprocessing_function = mobilenet_v2.preprocess_input
    elif base == 'resnet':
        from tensorflow.keras.applications import resnet50
        preprocessing_function = resnet50.preprocess_input
    else:
        preprocessing_function = None

    train_datagen = ImageDataGenerator(rotation_range=20,
                                       width_shift_range=0.1,
                                       height_shift_range=0.1,
                                       shear_range=0.1,
                                       zoom_range=0.1,
                                       horizontal_flip=True,
                                       preprocessing_function=preprocessing_function)
    val_datagen = ImageDataGenerator(preprocessing_function=preprocessing_function)

    train_gen = train_datagen.flow_from_directory(train_dir, target_size=(224,224), batch_size=batch, class_mode='categorical')
    val_gen = val_datagen.flow_from_directory(val_dir, target_size=(224,224), batch_size=batch, class_mode='categorical')

    num_classes = len(train_gen.class_indices)
    model = build_model(num_classes, base=base)

    # callbacks
    os.makedirs('models', exist_ok=True)
    chk = ModelCheckpoint('models/best_model.h5', monitor='val_accuracy', save_best_only=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)

    model.fit(train_gen, epochs=epochs, validation_data=val_gen, callbacks=[chk, reduce_lr])
    # Save class mapping
    with open('models/class_indices.json','w') as f:
        json.dump(train_gen.class_indices, f, indent=2)
    print("Training complete. Model saved to models/best_model.h5")

def parse_args():
    p = argparse.ArgumentParser(description="Train crop disease model")
    p.add_argument('--train_dir', required=True, help='train directory with subfolders per class')
    p.add_argument('--val_dir', required=True, help='validation directory')
    p.add_argument('--epochs', type=int, default=10)
    p.add_argument('--batch', type=int, default=16)
    p.add_argument('--base', type=str, choices=['mobilenet','resnet'], default='mobilenet')
    return p.parse_args()

if __name__ == '__main__':
    args = parse_args()
    train(args)
