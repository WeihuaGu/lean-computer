import argparse  
import numpy as np  
from PIL import Image  
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt  
  
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['STSong']
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
    return reconstructed_img_svd


# 使用PCA进行降维和重构
def reconstruct_with_pca(img_reshaped, n_components):
    pca = PCA(n_components=n_components)
    img_pca = pca.fit_transform(img_reshaped)
    return img_pca, pca.components_
  
parser = argparse.ArgumentParser(description='Image reconstruction using Truncated SVD')
parser.add_argument('--m', type=int, default=50, help='Number of components to use for reconstruction')
args = parser.parse_args()


# 加载图像  
img = load_image('raw.jpg')  
  
# 设定降维的维度  
n_components = args.m

# 使用SVD重构图像
reconstructed_img_svd = reconstruct_with_svd(img, n_components)

# 使用PCA重构图像
img_pca,pca_components = reconstruct_with_pca(img, n_components)
reconstructed_img_pca = img_pca@pca_components

# 显示原始图像和重构后的图像
fig, axs = plt.subplots(1, 4, figsize=(15, 5))
axs[0].imshow(img, cmap='gray')
axs[0].set_title('原始图片')
axs[0].axis('off')
axs[1].imshow(img_pca, cmap='gray')
axs[1].set_title('pca降维后大小')
axs[1].axis('off')
axs[2].imshow(reconstructed_img_pca, cmap='gray')
axs[2].set_title('pca降维后用主成分矩阵转置还原')
axs[2].axis('off')
axs[3].imshow(reconstructed_img_svd, cmap='gray')
axs[3].set_title('SVD')
axs[3].axis('off')
plt.show()

