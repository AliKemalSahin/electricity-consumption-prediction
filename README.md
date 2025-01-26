# Elektrik Tüketimi Tahmini

Bu depo, elektrik tüketimini tahmin etmek için makine öğrenimi modellerini kullanan bir projeyi içerir. Veri işleme, tahmin, model eğitimi ve uygulama dağıtımı için betikler sunar.

## Özellikler

Model Eğitimi: Elektrik tüketimi verileri üzerinde tahmin modellerini eğitin.

Tahmin Uç Noktaları: 24 saatlik ve 5 günlük tahminler yapın.

Sapma Algılama: Özel betikler kullanarak veri sapmasını izleyin.

Kubernetes Dağıtımı: Uygulamayı Kubernetes'e dağıtmak için YAML konfigürasyonları.

Docker Desteği: Uygulamayı kolayca konteynerleştirin ve dağıtın.

## Proje Yapısı

#### ├── dataset.csv                     # Elektrik tüketimi veri seti
#### ├── Dockerfile                      # Docker konfigürasyon dosyası
#### ├── electricity-deployment.yaml     # Kubernetes deployment konfigürasyonu
#### ├── ingress-electricity-prediction.yaml # Kubernetes ingress konfigürasyonu
#### ├── main.py                         # Ana uygulama betiği
#### ├── train.py                        # Model eğitim betiği
#### ├── request24h.py                   # 24 saatlik tahmin betiği
#### ├── request5d.py                    # 5 günlük tahmin betiği
#### ├── requestDrift.py                 # Sapma algılama betiği
#### ├── requirements.txt                # Python bağımlılıkları
#### ├── saved_models/                   # Kaydedilen modellerin bulunduğu klasör

# Başlangıç

## Gereksinimler

Python 3.8+

Docker

Kubernetes cluster (Kubernetes üzerinde dağıtım yapılacaksa)

# Kurulum

#### Depoyu klonlayın:

git clone https://github.com/your-username/electricity-consumption-prediction.git
cd electricity-consumption-prediction

#### Gerekli Python kütüphanelerini yükleyin:

pip install -r requirements.txt

### Model Eğitimi

#### Sağlanan veri seti ile modeli eğitin:

python train.py

#### Eğitilen model saved_models/ klasörüne kaydedilecektir.

### Uygulamayı Çalıştırma

#### Uygulamayı yerel olarak başlatın:

python main.py

### Tahmin Yapma

#### 24 saatlik tahminler için:

python request24h.py

#### 5 günlük tahminler için:

python request5d.py

#### Sapma algılama için:

python requestDrift.py

### Docker Kullanımı

#### Docker imajını oluşturun:

docker build -t electricity-prediction:latest .

#### Konteyneri çalıştırın:

docker run -p 8000:8000 electricity-prediction:latest

### Kubernetes Dağıtımı

#### Dağıtım konfigürasyonunu uygulayın:

kubectl apply -f electricity-deployment.yaml

#### Ingress konfigürasyonunu uygulayın:

kubectl apply -f ingress-electricity-prediction.yaml

#### Veri Seti

dataset.csv dosyası saatlik elektrik tüketimi verilerini içerir. Model eğitiminden önce veri setinin doğru formatta olduğundan emin olun.
