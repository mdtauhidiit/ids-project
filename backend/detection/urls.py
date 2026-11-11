from django.urls import path
from .views import RuleDetectionView, MLDetectionView, DLDetectionView, CompareAllView

urlpatterns = [
    path('detect/rule/', RuleDetectionView.as_view(), name='detect-rule'),
    path('detect/ml/', MLDetectionView.as_view(), name='detect-ml'),
    path('detect/dl/', DLDetectionView.as_view(), name='detect-dl'),
    path('detect/compare/', CompareAllView.as_view(), name='detect-compare'),
]