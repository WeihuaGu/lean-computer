import argparse  
import numpy as np  
from PIL import Image  
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt  
  
# 加载并处理图像  
def load_image(filename):  
    img = Image.open(filename).convert('L')  # 转换为灰度图像  
    img_array = np.array(img).astype(np.float64)  
    return img_array  
  
# 使用SVD进行降维和重构  
def reconstruct_with_svd(img_array, n_components):  
    # 对图像矩阵进行SVD分解  
    U, S, Vt = np.linalg.svd(img_array, full_matrices=False)  
    S_trunc = np.zeros_like(S)
    S_trunc[:n_components] = S[:n_components]
    reconstructed_img_svd = U.dot(np.diag(S_trunc)).dot(Vt)
    return reconstructed_img_svd.reshape(img_array.shape[0], -1)
    return reconstructed_img  

# 使用PCA进行降维和重构
def reconstruct_with_pca(img_reshaped, n_components):
    pca = PCA(n_components=n_components)
    img_pca = pca.fit_transform(img_reshaped)
    reconstructed_img_pca = pca.inverse_transform(img_pca)
    #return reconstructed_img_pca.reshape(img_reshaped.shape[0], -1)
    return reconstructed_img_pca
  
parser = argparse.ArgumentParser(description='Image reconstruction using Truncated SVD')
parser.add_argument('--m', type=int, default=50, help='Number of components to use for reconstruction')
args = parser.parse_args()


# 加载图像  
img = load_image('raw.jpg')  
  
# 设定降维的维度  
n_components = args.m

# 使用PCA重构图像
reconstructed_img_pca = reconstruct_with_pca(img, n_components)

# 使用SVD重构图像
reconstructed_img_svd = reconstruct_with_svd(img, n_components)

# 显示原始图像和重构后的图像
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
axs[0].imshow(img, cmap='gray')
axs[0].set_title('Original Image')
axs[0].axis('off')
axs[1].imshow(reconstructed_img_pca, cmap='gray')
axs[1].set_title('Reconstructed Image with PCA')
axs[1].axis('off')
axs[2].imshow(reconstructed_img_svd, cmap='gray')
axs[2].set_title('Reconstructed Image with SVD')
axs[2].axis('off')
plt.show()

