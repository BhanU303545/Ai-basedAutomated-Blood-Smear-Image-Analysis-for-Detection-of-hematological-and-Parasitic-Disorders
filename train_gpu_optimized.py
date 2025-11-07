import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, WeightedRandomSampler
import torchvision.transforms as transforms
import torchvision.models as models
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from sklearn.metrics import confusion_matrix
from tqdm import tqdm

class BloodSmearTrainer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        
        os.makedirs('models', exist_ok=True)
        
    def setup_data(self):
        base_path = r'C:\Users\SIVA\Desktop\datasets'
        
        train_path = os.path.join(base_path, 'train')
        val_path = os.path.join(base_path, 'val')
        
        if not os.path.exists(train_path):
            print(f"Error: Training path not found: {train_path}")
            return None
        
        print(f"Found training data: {train_path}")
        print(f"Found validation data: {val_path}")
        
        train_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(p=0.3),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.1, contrast=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        val_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.train_dataset = ImageFolder(train_path, transform=train_transform)
        self.val_dataset = ImageFolder(val_path, transform=val_transform)
        
        class_counts = []
        for class_idx in range(len(self.train_dataset.classes)):
            count = sum(1 for _, label in self.train_dataset.samples if label == class_idx)
            class_counts.append(count)
        
        print(f"Classes found: {self.train_dataset.classes}")
        print(f"Class distribution: {class_counts}")
        
        class_weights = 1.0 / torch.tensor(class_counts, dtype=torch.float)
        sample_weights = [class_weights[label] for _, label in self.train_dataset.samples]
        
        sampler = WeightedRandomSampler(sample_weights, len(sample_weights), replacement=True)
        
        batch_size = 16
        num_workers = 2
        
        self.train_loader = DataLoader(
            self.train_dataset, batch_size=batch_size, sampler=sampler, 
            num_workers=num_workers, pin_memory=False
        )
        
        self.val_loader = DataLoader(
            self.val_dataset, batch_size=batch_size, shuffle=False,
            num_workers=num_workers, pin_memory=False
        )
        
        print(f"Training samples: {len(self.train_dataset)}")
        print(f"Validation samples: {len(self.val_dataset)}")
        print(f"Batch size: {batch_size}")
        
        return class_counts
    
    def setup_model(self, class_counts):
        self.model = models.efficientnet_b0(weights='IMAGENET1K_V1')
        
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.2),
            nn.Linear(512, len(self.train_dataset.classes))
        )
        
        self.model = self.model.to(self.device)
        
        class_weights = torch.tensor(class_counts, dtype=torch.float)
        class_weights = 1.0 / class_weights
        class_weights = class_weights / class_weights.sum()
        class_weights = class_weights.to(self.device)
        
        self.criterion = nn.CrossEntropyLoss(weight=class_weights)
        
        self.optimizer = optim.AdamW(self.model.parameters(), lr=1e-4, weight_decay=0.01)
        
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=10, gamma=0.5)
        
    def train_epoch(self, epoch):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc=f'Epoch {epoch:2d}')
        
        for batch_idx, (images, labels) in enumerate(pbar):
            try:
                images, labels = images.to(self.device), labels.to(self.device)
                
                self.optimizer.zero_grad()
                
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.optimizer.step()
                
                running_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
                pbar.set_postfix({
                    'Loss': f'{loss.item():.4f}',
                    'Acc': f'{100.*correct/total:.2f}%',
                })
                
                if batch_idx % 100 == 0 and torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    
            except Exception as e:
                print(f"Error in batch {batch_idx}: {e}")
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                continue
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100.0 * correct / total
        
        return epoch_loss, epoch_acc
    
    def validate(self, epoch):
        self.model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in tqdm(self.val_loader, desc='Validating'):
                try:
                    images, labels = images.to(self.device), labels.to(self.device)
                    
                    outputs = self.model(images)
                    loss = self.criterion(outputs, labels)
                    
                    val_loss += loss.item()
                    _, predicted = torch.max(outputs, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
                    
                    all_preds.extend(predicted.cpu().numpy())
                    all_labels.extend(labels.cpu().numpy())
                    
                except Exception as e:
                    print(f"Validation error: {e}")
                    continue
        
        val_loss /= len(self.val_loader)
        val_acc = 100.0 * correct / total
        
        if epoch % 5 == 0:
            print("Class-wise Validation Accuracy:")
            cm = confusion_matrix(all_labels, all_preds)
            for i, class_name in enumerate(self.train_dataset.classes):
                if i < len(cm):
                    class_correct = cm[i, i]
                    class_total = cm[i].sum()
                    class_acc = 100.0 * class_correct / class_total if class_total > 0 else 0
                    print(f'  {class_name:25}: {class_acc:5.1f}% ({class_correct:3d}/{class_total:3d})')
        
        return val_loss, val_acc, all_preds, all_labels
    
    def train(self, epochs=30):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        class_counts = self.setup_data()
        if class_counts is None:
            return 0.0
        
        self.setup_model(class_counts)
        
        best_acc = 0
        train_losses, val_losses, train_accs, val_accs = [], [], [], []
        
        print(f"Training for {epochs} epochs")
        
        for epoch in range(1, epochs + 1):
            start_time = time.time()
            
            train_loss, train_acc = self.train_epoch(epoch)
            val_loss, val_acc, all_preds, all_labels = self.validate(epoch)
            
            self.scheduler.step()
            
            epoch_time = time.time() - start_time
            
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            train_accs.append(train_acc)
            val_accs.append(val_acc)
            
            print(f'Epoch {epoch:2d}/{epochs}:')
            print(f'  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:6.2f}%')
            print(f'  Val Loss:   {val_loss:.4f}, Val Acc:   {val_acc:6.2f}%')
            print(f'  Time:       {epoch_time:6.2f}s')
            print(f'  Best Acc:   {best_acc:6.2f}%')
            
            if val_acc > best_acc:
                best_acc = val_acc
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'val_acc': val_acc,
                    'class_names': self.train_dataset.classes,
                    'class_distribution': class_counts
                }, 'models/best_model.pth')
                print(f'  New best model saved! Accuracy: {val_acc:.2f}%')
            
            if epoch % 10 == 0:
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'val_acc': val_acc,
                }, f'models/checkpoint_epoch_{epoch}.pth')
                
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        torch.save({
            'epoch': epochs,
            'model_state_dict': self.model.state_dict(),
            'class_names': self.train_dataset.classes,
            'val_acc': val_acc,
            'train_acc': train_acc,
            'class_distribution': class_counts
        }, 'models/final_model.pth')
        
        print(f"Training completed! Best accuracy: {best_acc:.2f}%")
        
        self.plot_results(train_losses, val_losses, train_accs, val_accs)
        
        return best_acc
    
    def plot_results(self, train_losses, val_losses, train_accs, val_accs):
        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(train_losses, label='Train Loss')
        plt.plot(val_losses, label='Val Loss')
        plt.title('Training Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(train_accs, label='Train Accuracy')
        plt.plot(val_accs, label='Val Accuracy')
        plt.title('Training Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('training_results.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    trainer = BloodSmearTrainer()
    best_accuracy = trainer.train(epochs=30)
    
    if best_accuracy > 90:
        print(f"Excellent! Model achieved {best_accuracy:.2f}% accuracy")
    elif best_accuracy > 85:
        print(f"Great! Model achieved {best_accuracy:.2f}% accuracy")
    elif best_accuracy > 80:
        print(f"Good! Model achieved {best_accuracy:.2f}% accuracy")
    else:
        print(f"Needs improvement! Model only achieved {best_accuracy:.2f}% accuracy")