---
abstract: 'State-of-the-art machine learning systems are vulnerable to small perturbations
  to their input, where _small_ is defined according to a threat model that assigns
  a positive threat to each perturbation. Most prior works define a task-agnostic,
  isotropic, and global threat, like the l_p norm, where the magnitude of the perturbation
  fully determines the degree of the threat and neither the direction of the attack
  nor its position in space matter. However, common corruptions in computer vision,
  such as blur, compression, or occlusions, are not well captured by such treat models.
  This paper proposes a novel threat model called \texttt Projected Displacement (PD)
  to study robustness beyond existing isotropic and global threat models. The proposed
  threat model measures the threat of a perturbation via its alignment with _unsafe
  directions_, defined as directions in the input space along which a perturbation
  of sufficient magnitude changes the ground truth class label. Unsafe directions
  are identified locally for each input based on observed training data. In this way,
  the PD-threat model exhibits anisotropy and locality. The PD-threat model is computationally
  efficient and can be easily integrated into existing robustness pipelines. Experiments
  on Imagenet-1k data indicate that, for any input, the set of perturbations with
  small PD threat includes _safe_ perturbations of large l_p norm that preserve the
  true label, such as noise, blur and compression, while simultaneously excluding
  _unsafe_ perturbations that alter the true label. Unlike perceptual threat models
  based on embeddings of large-vision models, the PD-threat model can be readily computed
  for arbitrary classification tasks without pre-training or finetuning. Further additional
  task information such as sensitivity to image regions or concept hierarchies can
  be easily integrated into the assessment of threat and thus the PD threat model
  presents practitioners a flexible, task-driven threat specification that alleviates
  the limitations of l_p-threat models.

  '
authors:
- admin
- Ambar Pal
- Jeremias Sulam
- Rene Vidal
date: '2025-06-12T00:00:00Z'
doi: https://openaccess.thecvf.com/content/CVPR2025/html/Muthukumar_Disentangling_Safe_and_Unsafe_Image_Corruptions_via_Anisotropy_and_Locality_CVPR_2025_paper.html
featured: true
publication: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
  Recognition (CVPR), 2025
publication_short: CVPR 2025
publication_types:
- '1'
summary: ''
tags:
- robustness
title: Disentangling Safe and Unsafe Image Corruptions via Anisotropy and Locality
url_code: ''
url_dataset: ''
url_pdf: https://openaccess.thecvf.com/content/CVPR2025/papers/Muthukumar_Disentangling_Safe_and_Unsafe_Image_Corruptions_via_Anisotropy_and_Locality_CVPR_2025_paper.pdf
url_poster: https://cvpr.thecvf.com/media/PosterPDFs/CVPR%202025/34023.png?t=1749743425.0418725
url_project: ''
url_slides: ''
url_source: ''
url_supplement: https://openaccess.thecvf.com/content/CVPR2025/supplemental/Muthukumar_Disentangling_Safe_and_CVPR_2025_supplemental.pdf
url_video: https://www.youtube.com/watch?v=LhDQICSDlk8
---