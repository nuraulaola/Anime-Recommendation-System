# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
import operator

# Load pickled recommendations and indices
try:
    recommendations = pd.read_pickle("recommendations.pkl")
    top_recommendations_indices = np.load("top_recommendations_indices.pkl")
except FileNotFoundError:
    # Handle the case when the files are not found
    recommendations = pd.DataFrame(columns=["anime_id", "name", "mean_rating"])
    top_recommendations_indices = np.array([])

# Recommendation System Functions
