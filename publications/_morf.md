---
layout: publication
title: "Manifold Oblique Random Forests: Towards Closing the Gap on Convolutional Deep Networks"
year: 2023
venue: "SIAM Journal on Mathematics of Data Science (SIMODS)"
doi: "10.1137/nnnnnnnn"
pdf_url: "https://example.com/morf.pdf"
github: "https://github.com/neurodata/morf"
image: "/publications/images/morf-poster.png"
image_alt: "MORF Research Poster"
contribution: "Extended R package with manifold learning functionality; experimental design and figure generation"
---

## Overview

Manifold Oblique Random Forests (MORF) incorporates manifold learning into the oblique random forest framework, enabling the algorithm to discover lower-dimensional structure in high-dimensional data while maintaining performance competitive with convolutional neural networks on image classification tasks.

## Your Contribution

Building on SPORF, I extended this work by:
- **Package Enhancement**: Implemented manifold learning functionality in the R package
- **Experimental Design**: Designed comprehensive experiments comparing MORF against CNN baselines across multiple datasets
- **Empirical Validation**: Generated data and figures demonstrating the empirical gap-closing between MORF and deep networks
- **Visualization**: Created publication-quality visualizations of results

This work shows how mathematical insights about manifold structure can be translated into practical improvements in tree-based methods.

## Key Findings

- Manifold-aware oblique splits capture structure that axis-aligned splits miss
- MORF achieves CNN-competitive performance on image datasets without convolutions
- The method scales better than deep networks for certain problem classes
- Interpretability is preserved while matching deep learning performance

## Impact

MORF challenges the assumption that deep networks are necessary for high-dimensional structured data, offering an interpretable, computationally efficient alternative.
