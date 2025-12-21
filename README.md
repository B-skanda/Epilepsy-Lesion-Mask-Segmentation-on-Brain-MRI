
# Epilepsy-Lesion-Mask-Segmentation-on-Brain-MRI 

This Project is all about Segmenting Lesion Mask from Brain Epilepsy MRI Image. It uses 3D U-Net 
Architecture using Monai Library.


## Step1: Creating a Virtual Environment

#### Open the terminal from VS code

```http
  python -m venv your_environment_name
```
##### A new Environment will be created.

## Step2: Activate your Environment
#### Now type the following command after first step

```http
  your_environment_name\Scripts\Activate
```
##### Your newly created environment gets Activated.

## Step3: Install the dependency
#### Now Follow this step

```http
  pip install monai
```
##### Monai Library will be installed in your Environment.

## Dataset Resource 
##### The Datasets for this following Project is availaible by navigating to this Link. The datas are there in  "The Imaging Database for Epilepsy And Surgery (IDEAS)" from Open Neuro with the size of 3.28 GB. This is an Open Source Platform for validating and sharing BIDS-compliant MRI, PET, MEG, EEG, and iEEG data.

```http
  https://openneuro.org/datasets/ds005602/versions/1.0.0
```
##### After Downloading please run the ``` preprocess.py ``` file to prepare the datasets by creating prepared_ds Folder which contatins imagesTr folder that contains Brain MRI datas and labelsTr folder that contains the corresponding labels of imagesTr. 




